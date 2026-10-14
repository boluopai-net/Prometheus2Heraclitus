#!/usr/bin/env python3
"""Share only explicitly configured Obsidian settings on macOS."""

from __future__ import annotations

import argparse
import fcntl
import filecmp
import json
import os
import shutil
import subprocess
import sys
import time
from collections.abc import Iterable
from contextlib import contextmanager
from pathlib import Path

CONFIG: dict = {}
CLOUD_VAULT_PATHS: tuple[Path, ...] = ()
DEFAULT_WORKSPACE_VAULTS: tuple[Path, ...] = ()
SHARED_CONFIG_DIRNAME = ".obsidian-shared-config"

def load_configuration(config_path: Path) -> dict:
    """No account discovery or host defaults; every target is recipient selected."""
    global CONFIG, CLOUD_VAULT_PATHS, DEFAULT_WORKSPACE_VAULTS
    data = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Configuration must be a JSON object")
    for key in ("cloud_root", "shared_config_root", "source_seed_root", "lock_path",
                "watch_state_file", "sync_command"):
        value = data.get(key)
        if not isinstance(value, str) or not Path(value).is_absolute():
            raise ValueError(f"{key} must be an explicit absolute path")
    for key in ("cloud_vaults", "local_vaults"):
        if not isinstance(data.get(key), list) or any(
            not isinstance(value, str) or not Path(value).is_absolute()
            for value in data[key]
        ):
            raise ValueError(f"{key} must be a list of absolute paths")
    clouds = tuple(Path(value).resolve() for value in data["cloud_vaults"])
    locals_ = tuple(Path(value).resolve() for value in data["local_vaults"])
    targets = (*clouds, *locals_)
    if not targets or len(set(targets)) != len(targets):
        raise ValueError("Choose at least one vault, without duplicate/group overlap")
    authority = Path(data["shared_config_root"]).resolve()
    cloud_root = Path(data["cloud_root"]).resolve()
    for vault in targets:
        if vault == authority or vault in authority.parents or authority in vault.parents:
            raise ValueError("Shared authority and vaults must not contain one another")
        if any(other != vault and other in vault.parents for other in targets):
            raise ValueError("Configured vaults must not contain one another")
    for vault in clouds:
        if cloud_root not in vault.parents:
            raise ValueError("Cloud-copy vaults must be inside cloud_root")
    for vault in locals_:
        if cloud_root == vault or cloud_root in vault.parents:
            raise ValueError("File Provider vaults require cloud-copy mode")
    protected = (authority, *targets, Path(data["source_seed_root"]).resolve())
    for key in ("lock_path", "watch_state_file"):
        state = Path(data[key]).resolve()
        if any(state == path or path in state.parents for path in protected):
            raise ValueError(f"{key} must be outside the managed configuration trees")
    CONFIG = data
    CLOUD_VAULT_PATHS = clouds
    DEFAULT_WORKSPACE_VAULTS = locals_
    return data

DIRECTORY_ITEMS_TO_LINK = ("plugins", "themes", "snippets")
FILE_ITEMS_TO_LINK = (
    "appearance.json",
    "hotkeys.json",
    "app.json",
    "community-plugins.json",
    "core-plugins.json",
)
ITEMS_TO_LINK = (*DIRECTORY_ITEMS_TO_LINK, *FILE_ITEMS_TO_LINK)
IGNORED_RUNTIME_NAMES = (".DS_Store", "Icon\r")


class ProcessLockContended(RuntimeError):
    """Raised when another mutating obsidian-sync process already holds the lock."""


def process_lock_path() -> Path:
    return Path(CONFIG["lock_path"])


@contextmanager
def exclusive_process_lock(lock_path: Path):
    """Serialize mutating runs before they can alter Drive config or vault links."""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as lock_handle:
        try:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ProcessLockContended(lock_path) from exc
        try:
            yield
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def ts() -> int:
    return int(time.time())


def is_effectively_empty(path: Path) -> bool:
    """Reject empty/default shells before reverse sync."""
    try:
        size = path.stat().st_size
        if size == 0:
            return True
        if path.suffix.lower() == ".json" and size < 4096:
            content = path.read_text(encoding="utf-8", errors="ignore").strip()
            if content in ("{}", "[]", "{ }", "[ ]"):
                return True
        return False
    except Exception:
        return True


def maybe_reverse_sync(
    source: Path, target: Path, dry_run: bool, enable_reverse_sync: bool
) -> None:
    """Admit a newer eligible target file into the shared authority."""
    if not enable_reverse_sync:
        return
    if not source.exists() or not source.is_file():
        return
    if not target.exists() or target.is_symlink() or not target.is_file():
        return

    try:
        if same_file_content(source, target):
            return
        if is_effectively_empty(target):
            print(f"[SKIP] empty/default target, no reverse sync: {target}")
            return

        source_size = source.stat().st_size
        target_size = target.stat().st_size
        if source_size > 0 and target_size < source_size * 0.1:
            print(f"[SKIP] shrink anomaly, no reverse sync: {target}")
            return

        if target.stat().st_mtime > source.stat().st_mtime:
            print(f"[UP] reverse sync to source: {target} -> {source}")
            if not dry_run:
                shutil.copy2(target, source)
    except Exception as exc:
        print(f"[WARN] reverse sync failed: {target} ({exc})")


def same_file_content(left: Path, right: Path) -> bool:
    try:
        return filecmp.cmp(left, right, shallow=False)
    except OSError:
        return False


def copy_regular_file(source: Path, target: Path) -> None:
    """Copy file bytes and basic POSIX metadata without File Provider xattrs."""
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    shutil.copymode(source, target)
    source_stat = source.stat()
    os.utime(target, ns=(source_stat.st_atime_ns, source_stat.st_mtime_ns))


def serialized_symlink_target(source: Path, target: Path) -> bool:
    """Detect a File Provider file whose bytes are the former symlink target."""
    if target.is_symlink() or not target.is_file():
        return False
    try:
        if target.stat().st_size > 4096:
            return False
        raw = target.read_text(encoding="utf-8")
        if not raw or "\n" in raw or "\r" in raw:
            return False
        payload = Path(raw).expanduser()
        if not payload.is_absolute():
            payload = target.parent / payload
        return payload.resolve() == source.resolve()
    except (OSError, UnicodeError):
        return False


def sync_tree(source: Path, target: Path, dry_run: bool) -> int:
    """Add or update source tree entries without deleting target-only recovery data."""
    changes = 0
    for source_path in sorted(source.rglob("*")):
        if source_path.name in IGNORED_RUNTIME_NAMES:
            continue
        relative = source_path.relative_to(source)
        target_path = target / relative
        if source_path.is_symlink():
            print(f"[WARN] skip nested symlink in shared config: {source_path}")
            continue
        if source_path.is_dir():
            if target_path.exists(follow_symlinks=False) and (
                target_path.is_symlink() or not target_path.is_dir()
            ):
                print(f"[WARN] target type conflict, keep unchanged: {target_path}")
                continue
            if not target_path.exists(follow_symlinks=False):
                print(f"[MKDIR] {target_path}")
                changes += 1
                if not dry_run:
                    target_path.mkdir(parents=True)
            continue
        if target_path.exists(follow_symlinks=False) and (
            target_path.is_symlink() or not target_path.is_file()
        ):
            print(f"[WARN] target type conflict, keep unchanged: {target_path}")
            continue
        if target_path.is_file() and same_file_content(source_path, target_path):
            continue
        print(f"[COPY] {source_path} -> {target_path}")
        changes += 1
        if not dry_run:
            copy_regular_file(source_path, target_path)
    return changes


def merge_newer_tree(source: Path, target: Path, dry_run: bool) -> int:
    """Merge new or newer regular files into the shared directory authority."""
    changes = 0
    for source_path in sorted(source.rglob("*")):
        if source_path.name in IGNORED_RUNTIME_NAMES:
            continue
        relative = source_path.relative_to(source)
        target_path = target / relative
        if source_path.is_symlink():
            continue
        if source_path.is_dir():
            if target_path.exists(follow_symlinks=False) and not target_path.is_dir():
                print(f"[WARN] reverse-sync type conflict, keep shared config: {target_path}")
                continue
            if not target_path.exists(follow_symlinks=False):
                print(f"[UP] create shared directory: {source_path} -> {target_path}")
                changes += 1
                if not dry_run:
                    target_path.mkdir(parents=True)
            continue
        if target_path.exists(follow_symlinks=False) and not target_path.is_file():
            print(f"[WARN] reverse-sync type conflict, keep shared config: {target_path}")
            continue
        should_copy = not target_path.exists(follow_symlinks=False)
        if target_path.is_file():
            should_copy = (
                source_path.stat().st_mtime_ns > target_path.stat().st_mtime_ns
                and not same_file_content(source_path, target_path)
            )
        if not should_copy:
            continue
        print(f"[UP] reverse sync to shared config: {source_path} -> {target_path}")
        changes += 1
        if not dry_run:
            copy_regular_file(source_path, target_path)
    return changes


def replace_with_real_copy(source: Path, target: Path, dry_run: bool) -> None:
    if target.exists(follow_symlinks=False):
        backup = next_available_backup_path(target)
        print(f"[MOVE] {target} -> {backup}")
        if not dry_run:
            target.rename(backup)
    print(f"[COPY] {source} -> {target}")
    if dry_run:
        return
    if source.is_dir():
        target.mkdir(parents=True)
        sync_tree(source, target, dry_run=False)
    else:
        copy_regular_file(source, target)


def ensure_cloud_copy(
    source: Path,
    target: Path,
    dry_run: bool = False,
    enable_reverse_sync: bool = False,
) -> None:
    """Keep a real File Provider-safe copy of one shared config item."""
    if not source.exists():
        print(f"[SKIP] source missing: {source}")
        return

    target_exists = target.exists(follow_symlinks=False)
    correct_type = (
        target_exists
        and not target.is_symlink()
        and ((source.is_dir() and target.is_dir()) or (source.is_file() and target.is_file()))
    )
    if not correct_type or serialized_symlink_target(source, target):
        replace_with_real_copy(source, target, dry_run)
        return

    if source.is_dir():
        if enable_reverse_sync:
            merge_newer_tree(target, source, dry_run)
        changes = sync_tree(source, target, dry_run)
        if changes == 0:
            print(f"[OK] real directory: {target}")
        return

    if enable_reverse_sync:
        maybe_reverse_sync(source, target, dry_run, enable_reverse_sync=True)
    if same_file_content(source, target):
        print(f"[OK] real file: {target}")
        return
    if not enable_reverse_sync:
        replace_with_real_copy(source, target, dry_run)
        return
    print(f"[COPY] {source} -> {target}")
    if not dry_run:
        copy_regular_file(source, target)


def ensure_symlink(
    source: Path,
    target: Path,
    dry_run: bool = False,
    enable_reverse_sync: bool = False,
) -> None:
    if not source.exists():
        print(f"[SKIP] source missing: {source}")
        return

    if target.exists(follow_symlinks=False) and target.is_symlink():
        try:
            if target.resolve() == source.resolve():
                print(f"[OK] keep: {target} -> {source}")
                return
        except Exception:
            pass

    if target.exists(follow_symlinks=False) and not target.is_symlink() and target.is_file():
        maybe_reverse_sync(
            source,
            target,
            dry_run=dry_run,
            enable_reverse_sync=enable_reverse_sync,
        )

    if target.exists(follow_symlinks=False):
        backup = next_available_backup_path(target)
        print(f"[MOVE] {target} -> {backup}")
        if not dry_run:
            target.rename(backup)

    print(f"[LINK] {target} -> {source}")
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(source, target_is_directory=source.is_dir())


def next_available_backup_path(target: Path) -> Path:
    """Return a backup name that cannot replace an existing recovery artifact."""
    base = target.parent / f"{target.name}.bak.{ts()}"
    candidate = base
    index = 1
    while candidate.exists(follow_symlinks=False):
        candidate = target.parent / f"{base.name}.{index}"
        index += 1
    return candidate


def parse_vault_file(path: Path) -> list[Path]:
    result: list[Path] = []
    if not path.exists():
        return result
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        result.append(Path(line).expanduser())
    return result


def uniq_paths(paths: Iterable[Path]) -> list[Path]:
    seen = set()
    result: list[Path] = []
    for p in paths:
        r = p.expanduser().resolve() if p.exists() else p.expanduser()
        key = str(r)
        if key in seen:
            continue
        seen.add(key)
        result.append(r)
    return result


def cloud_vaults(google_drive_root: Path) -> list[Path]:
    return list(CLOUD_VAULT_PATHS)


def workspace_vaults() -> list[Path]:
    return list(DEFAULT_WORKSPACE_VAULTS)


def configured_vaults(google_drive_root: Path) -> list[Path]:
    """Return the explicit vault groups without recursive discovery."""
    return [*cloud_vaults(google_drive_root), *workspace_vaults()]


def discover_vaults(google_drive_root: Path) -> list[Path]:
    """Select only explicit vaults; never scan nested paths."""
    return [path for path in configured_vaults(google_drive_root) if path.is_dir()]


def check_default_vaults(google_drive_root: Path, shared_config_root: Path | None = None) -> bool:
    shared_config_root = shared_config_root or google_drive_root / SHARED_CONFIG_DIRNAME
    valid = True
    shared_valid = validate_shared_config(shared_config_root)
    valid = shared_valid and valid
    for vault in cloud_vaults(google_drive_root):
        if vault.is_dir():
            print(f"[OK] cloud vault: {vault}")
            if shared_valid and not validate_cloud_vault_config(shared_config_root, vault):
                valid = False
        else:
            print(f"[ERROR] cloud vault missing: {vault}")
            valid = False
    for vault in workspace_vaults():
        if vault.is_dir():
            print(f"[OK] workspace vault: {vault}")
            if shared_valid and not validate_workspace_vault_config(shared_config_root, vault):
                valid = False
        else:
            print(f"[ERROR] workspace vault missing: {vault}")
            valid = False
    return preflight_workspace_vaults(workspace_vaults()) and valid


def config_paths(root: Path) -> list[Path]:
    return [
        root / ".obsidian",
        root / ".obsidian.vimrc",
        root / ".gdriveignore",
    ]


def managed_item_pairs(shared_config_root: Path, vault: Path) -> list[tuple[Path, Path]]:
    central_obsidian, central_vimrc, central_gdriveignore = config_paths(shared_config_root)
    target_obsidian = vault / ".obsidian"
    return [
        *((central_obsidian / item, target_obsidian / item) for item in ITEMS_TO_LINK),
        (central_vimrc, vault / ".obsidian.vimrc"),
        (central_gdriveignore, vault / ".gdriveignore"),
    ]


def validate_cloud_vault_config(shared_config_root: Path, vault: Path) -> bool:
    valid = True
    for source, target in managed_item_pairs(shared_config_root, vault):
        expected = "directory" if source.is_dir() else "file"
        correct = (
            not target.is_symlink()
            and (
                (expected == "directory" and target.is_dir())
                or (expected == "file" and target.is_file())
            )
            and not serialized_symlink_target(source, target)
        )
        if correct:
            continue
        valid = False
        observed = (
            "missing"
            if not target.exists(follow_symlinks=False)
            else "symlink"
            if target.is_symlink()
            else "directory"
            if target.is_dir()
            else "serialized symlink"
            if serialized_symlink_target(source, target)
            else "file"
            if target.is_file()
            else "other"
        )
        print(f"[ERROR] cloud managed path must be a real {expected}: {target} (found {observed})")
    return valid


def validate_workspace_vault_config(shared_config_root: Path, vault: Path) -> bool:
    valid = True
    for source, target in managed_item_pairs(shared_config_root, vault):
        correct = False
        if target.is_symlink():
            try:
                correct = target.resolve() == source.resolve()
            except OSError:
                correct = False
        if correct:
            continue
        valid = False
        print(f"[ERROR] workspace managed path must link to {source}: {target}")
    return valid


def is_cloud_vault(vault: Path, google_drive_root: Path) -> bool:
    return vault.resolve() in CLOUD_VAULT_PATHS


def repo_seed_paths(repo_root: Path) -> list[Path]:
    return config_paths(repo_root)


def tracked_managed_paths(vault: Path) -> list[Path]:
    """Return managed paths tracked by a repository rooted at this exact vault."""
    try:
        root = subprocess.run(
            ["git", "-C", str(vault), "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return []
    if root.returncode != 0 or Path(root.stdout.strip()).resolve() != vault.resolve():
        return []

    tracked = subprocess.run(
        [
            "git",
            "-C",
            str(vault),
            "ls-files",
            "-z",
            "--",
            *(f".obsidian/{item}" for item in ITEMS_TO_LINK),
            ".obsidian.vimrc",
            ".gdriveignore",
        ],
        check=False,
        capture_output=True,
    )
    if tracked.returncode != 0:
        return []
    return [vault / relative for relative in tracked.stdout.decode().split("\0") if relative]


def preflight_workspace_vaults(vaults: Iterable[Path]) -> bool:
    workspace_roots = {path.resolve() for path in workspace_vaults()}
    valid = True
    for vault in vaults:
        if vault.resolve() not in workspace_roots:
            continue
        tracked = tracked_managed_paths(vault)
        if not tracked:
            continue
        valid = False
        print(
            f"[ERROR] migration-required: tracked managed Obsidian paths in workspace vault: {vault}"
        )
        for path in tracked:
            print(f"[ERROR] tracked managed path: {path}")
        print("[HINT] untrack and ignore those managed paths in that repository before linking")
    return valid


def copy_missing(source: Path, target: Path, dry_run: bool) -> None:
    """Seed cloud-shared config without replacing existing cloud/runtime content."""
    if source.is_dir():
        if not target.exists(follow_symlinks=False):
            print(f"[SEED] {source} -> {target}")
            if not dry_run:
                shutil.copytree(source, target)
            return
        if not target.is_dir() or target.is_symlink():
            print(f"[KEEP] existing non-directory shared target: {target}")
            return
        for child in source.iterdir():
            copy_missing(child, target / child.name, dry_run)
        return

    if target.exists(follow_symlinks=False):
        print(f"[KEEP] existing shared config: {target}")
        return
    print(f"[SEED] {source} -> {target}")
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def bootstrap_shared_config(repo_root: Path, shared_config_root: Path, dry_run: bool) -> bool:
    seeds = repo_seed_paths(repo_root)
    missing = [path for path in seeds if not path.exists()]
    if missing:
        for path in missing:
            print(f"[ERROR] missing repository seed: {path}")
        return False
    for source, target in zip(seeds, config_paths(shared_config_root), strict=True):
        copy_missing(source, target, dry_run)
    return True


def validate_shared_config(shared_config_root: Path) -> bool:
    expected_paths = [
        (shared_config_root / ".obsidian", "directory"),
        *((shared_config_root / name, "file") for name in (".obsidian.vimrc", ".gdriveignore")),
        *(
            (shared_config_root / ".obsidian" / name, "directory")
            for name in DIRECTORY_ITEMS_TO_LINK
        ),
        *((shared_config_root / ".obsidian" / name, "file") for name in FILE_ITEMS_TO_LINK),
    ]
    valid = True
    for path, expected_type in expected_paths:
        actual_type = (
            "directory"
            if path.is_dir() and not path.is_symlink()
            else "file"
            if path.is_file() and not path.is_symlink()
            else None
        )
        if actual_type == expected_type:
            continue
        valid = False
        observed = (
            "missing"
            if not path.exists(follow_symlinks=False)
            else "symlink"
            if path.is_symlink()
            else actual_type or "other"
        )
        print(f"[ERROR] shared cloud config must be a {expected_type}: {path} (found {observed})")
    if valid:
        return True
    print("[HINT] run obsidian-sync --bootstrap-shared-config after reviewing --dry-run")
    return False


def synchronize_vaults(
    args: argparse.Namespace,
    repo_root: Path,
    google_drive_root: Path,
    shared_config_root: Path,
    vaults: list[Path],
) -> int:
    if args.bootstrap_shared_config:
        if not bootstrap_shared_config(repo_root, shared_config_root, args.dry_run):
            return 1
        if args.dry_run:
            print("[DONE] shared cloud config bootstrap preview completed")
            return 0
    if not validate_shared_config(shared_config_root):
        return 1

    print(f"[INFO] Google Drive root: {google_drive_root}")
    print(f"[INFO] shared cloud config: {shared_config_root}")
    for vault in cloud_vaults(google_drive_root):
        if not vault.is_dir():
            print(f"[SKIP] cloud vault missing: {vault}")
    for vault in workspace_vaults():
        if not vault.is_dir():
            print(f"[SKIP] workspace vault missing: {vault}")
    print(f"[INFO] vault count: {len(vaults)}")

    for vault in vaults:
        if not vault.exists():
            print(f"[SKIP] vault missing: {vault}")
            continue

        cloud_mode = is_cloud_vault(vault, google_drive_root)
        mode = "real-copy" if cloud_mode else "symlink"
        print(f"[VAULT] {vault} ({mode})")
        target_obsidian = vault / ".obsidian"
        if not target_obsidian.exists():
            print(f"[MKDIR] {target_obsidian}")
            if not args.dry_run:
                target_obsidian.mkdir(parents=True, exist_ok=True)

        for source, target in managed_item_pairs(shared_config_root, vault):
            ensure = ensure_cloud_copy if cloud_mode else ensure_symlink
            ensure(
                source,
                target,
                dry_run=args.dry_run,
                enable_reverse_sync=not args.disable_reverse_sync,
            )

    print("[DONE] Obsidian configuration synchronized")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path, help="Recipient JSON configuration")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--print-config", "--print-defaults", dest="print_defaults", action="store_true")
    parser.add_argument("--check", "--check-defaults", dest="check_defaults", action="store_true")
    parser.add_argument("--bootstrap-shared-config", action="store_true",
                        help="Copy missing seed items only; preserve shared authority")
    parser.add_argument("--disable-reverse-sync", action="store_true")
    args = parser.parse_args()
    try:
        config = load_configuration(args.config)
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))
    google_drive_root = Path(config["cloud_root"])
    shared_config_root = Path(config["shared_config_root"])
    repo_root = Path(config["source_seed_root"])
    vaults = configured_vaults(google_drive_root)
    if args.print_defaults:
        print(json.dumps(config, indent=2))
        return 0
    if args.check_defaults:
        return 0 if check_default_vaults(google_drive_root, shared_config_root) else 1
    missing = [path for path in vaults if not path.is_dir()]
    if missing:
        for path in missing:
            print(f"[ERROR] configured vault missing: {path}", file=sys.stderr)
        return 1
    if not preflight_workspace_vaults(vaults):
        return 1
    if args.dry_run:
        return synchronize_vaults(args, repo_root, google_drive_root, shared_config_root, vaults)
    lock_path = process_lock_path()
    try:
        with exclusive_process_lock(lock_path):
            print(f"[LOCK] acquired exclusive process lock: {lock_path}")
            return synchronize_vaults(args, repo_root, google_drive_root, shared_config_root, vaults)
    except ProcessLockContended:
        print(f"[ERROR] another process holds the exclusive lock: {lock_path}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
