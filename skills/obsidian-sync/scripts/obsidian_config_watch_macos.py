#!/usr/bin/env python3
"""Near-real-time macOS watcher for the managed Obsidian configuration set."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import select
import signal
import subprocess
import sys
import time
from collections.abc import Iterable, Iterator
from contextlib import suppress
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import obsidian_sync_macos as sync  # noqa: E402

DEFAULT_DEBOUNCE_SECONDS = 0.75
DEFAULT_RETRY_SECONDS = 5.0
DEFAULT_SYNC_TIMEOUT_SECONDS = 120.0
MAX_CONVERGENCE_PASSES = 3
MIN_OPEN_FILE_SOFT_LIMIT = 1024
STATE_SCHEMA_VERSION = 1
READ_CHUNK_SIZE = 1024 * 1024
SYNC_CONFIG = ""


def ensure_open_file_limit(minimum: int = MIN_OPEN_FILE_SOFT_LIMIT) -> tuple[int, int]:
    """Leave headroom for recursive vnode handles and sync subprocess startup."""
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    target = max(soft, minimum)
    if hard != resource.RLIM_INFINITY:
        target = min(target, hard)
    if target > soft:
        resource.setrlimit(resource.RLIMIT_NOFILE, (target, hard))
        soft = target
    return soft, hard


def managed_roots(config_root: Path) -> list[Path]:
    """Return only paths owned by obsidian-sync, never note data or workspace.json."""
    obsidian = config_root / ".obsidian"
    return [
        *(obsidian / item for item in sync.ITEMS_TO_LINK),
        config_root / ".obsidian.vimrc",
        config_root / ".gdriveignore",
    ]


def configured_watch_roots(
    google_drive_root: Path,
    shared_config_root: Path,
    workspace_vaults: Iterable[Path],
) -> list[Path]:
    """Watch the explicit shared authority, cloud copies, and local links."""
    config_roots = [
        shared_config_root,
        *sync.cloud_vaults(google_drive_root),
        *workspace_vaults,
    ]
    seen: set[str] = set()
    result: list[Path] = []
    for config_root in config_roots:
        for path in managed_roots(config_root):
            key = str(path.expanduser().absolute())
            if key in seen:
                continue
            seen.add(key)
            result.append(path.expanduser().absolute())
    return result


def _hash_token(digest: Any, token: str) -> None:
    encoded = token.encode("utf-8", errors="surrogateescape")
    digest.update(len(encoded).to_bytes(8, "big"))
    digest.update(encoded)


def _hash_file(digest: Any, path: Path) -> None:
    try:
        with path.open("rb") as handle:
            while chunk := handle.read(READ_CHUNK_SIZE):
                digest.update(chunk)
    except OSError as exc:
        _hash_token(digest, f"read-error:{exc.errno}")


def _hash_tree_entry(digest: Any, path: Path, relative: str) -> None:
    try:
        stat_result = path.lstat()
    except OSError as exc:
        _hash_token(digest, f"missing:{relative}:{exc.errno}")
        return

    if path.is_symlink():
        try:
            target = os.readlink(path)
        except OSError as exc:
            target = f"readlink-error:{exc.errno}"
        _hash_token(digest, f"symlink:{relative}:{target}")
        return

    if path.is_dir():
        _hash_token(digest, f"directory:{relative}")
        try:
            children = sorted(
                (child for child in path.iterdir() if child.name not in sync.IGNORED_RUNTIME_NAMES),
                key=lambda item: item.name,
            )
        except OSError as exc:
            _hash_token(digest, f"list-error:{relative}:{exc.errno}")
            return
        for child in children:
            child_relative = f"{relative}/{child.name}" if relative else child.name
            _hash_tree_entry(digest, child, child_relative)
        return

    if path.is_file():
        _hash_token(digest, f"file:{relative}:{stat_result.st_size}")
        _hash_file(digest, path)
        return

    _hash_token(digest, f"other:{relative}:{stat_result.st_mode}")


def content_fingerprint(paths: Iterable[Path]) -> str:
    """Hash names, types, symlink targets, and file bytes, but not timestamps."""
    digest = hashlib.sha256()
    unique_paths = sorted({str(path.absolute()): path.absolute() for path in paths}.items())
    for absolute_name, path in unique_paths:
        _hash_token(digest, f"root:{absolute_name}")
        _hash_tree_entry(digest, path, "")
    return digest.hexdigest()


def load_saved_fingerprint(state_path: Path) -> str | None:
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return None
    if payload.get("schema_version") != STATE_SCHEMA_VERSION:
        return None
    fingerprint = payload.get("fingerprint")
    return fingerprint if isinstance(fingerprint, str) else None


def save_fingerprint(state_path: Path, fingerprint: str) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = state_path.with_name(f".{state_path.name}.{os.getpid()}.tmp")
    payload = {
        "schema_version": STATE_SCHEMA_VERSION,
        "fingerprint": fingerprint,
        "updated_at": int(time.time()),
    }
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.chmod(temporary, 0o600)
    os.replace(temporary, state_path)


def run_sync_if_changed(
    paths: Iterable[Path],
    state_path: Path,
    sync_command: Path,
    sync_timeout_seconds: float,
) -> tuple[bool, str]:
    """Run the existing lock-owning entrypoint only after a content change."""
    path_list = list(paths)
    before = content_fingerprint(path_list)
    previous = load_saved_fingerprint(state_path)
    if before == previous:
        print(f"[NOOP] managed content fingerprint unchanged: {before}", flush=True)
        return True, before

    print(
        f"[SYNC] managed content changed: {previous or 'uninitialized'} -> {before}",
        flush=True,
    )
    current = before
    for pass_number in range(1, MAX_CONVERGENCE_PASSES + 1):
        try:
            completed = subprocess.run(
                [str(sync_command), "--config", SYNC_CONFIG],
                check=False,
                timeout=sync_timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            print(
                f"[ERROR] obsidian-sync exceeded {sync_timeout_seconds:g}s; will retry",
                file=sys.stderr,
                flush=True,
            )
            return False, current
        except OSError as exc:
            print(
                f"[ERROR] unable to execute obsidian-sync: {sync_command} ({exc})",
                file=sys.stderr,
                flush=True,
            )
            return False, current

        if completed.returncode != 0:
            print(
                f"[ERROR] obsidian-sync exited {completed.returncode}; will retry",
                file=sys.stderr,
                flush=True,
            )
            return False, current

        after = content_fingerprint(path_list)
        if after == current:
            save_fingerprint(state_path, after)
            print(f"[READY] managed content converged: {after}", flush=True)
            return True, after
        print(
            f"[SETTLE] sync pass {pass_number} changed managed content; verify once more",
            flush=True,
        )
        current = after

    print(
        f"[ERROR] managed content did not settle after {MAX_CONVERGENCE_PASSES} passes; will retry",
        file=sys.stderr,
        flush=True,
    )
    return False, current


def _nearest_existing_parent(path: Path) -> Path | None:
    candidate = path
    while not candidate.exists(follow_symlinks=False):
        parent = candidate.parent
        if parent == candidate:
            return None
        candidate = parent
    if candidate.is_symlink() or not candidate.is_dir():
        candidate = candidate.parent
    return candidate if candidate.exists() else None


def iter_event_paths(roots: Iterable[Path]) -> Iterator[Path]:
    """Yield each existing node plus parents needed to notice atomic replacements."""
    seen: set[str] = set()

    def emit(path: Path) -> Iterator[Path]:
        key = str(path.absolute())
        if key not in seen:
            seen.add(key)
            yield path

    for root in roots:
        parent = _nearest_existing_parent(root.parent)
        if parent is not None:
            yield from emit(parent)
        if not root.exists(follow_symlinks=False):
            nearest = _nearest_existing_parent(root)
            if nearest is not None:
                yield from emit(nearest)
            continue
        yield from emit(root)
        if root.is_symlink() or not root.is_dir():
            continue
        try:
            descendants = sorted(root.rglob("*"), key=lambda item: str(item))
        except OSError:
            continue
        for descendant in descendants:
            if descendant.name in sync.IGNORED_RUNTIME_NAMES:
                continue
            yield from emit(descendant)


class KqueueManagedPathWatcher:
    """Recursive EVFILT_VNODE watcher rebuilt after each debounced event batch."""

    def __init__(self, roots: Iterable[Path]):
        if not hasattr(select, "kqueue") or not hasattr(select, "KQ_FILTER_VNODE"):
            raise RuntimeError("kqueue EVFILT_VNODE is unavailable on this platform")
        self.roots = list(roots)
        self.queue: select.kqueue | None = None
        self.handles: dict[int, Path] = {}
        self.rebuild()

    def close(self) -> None:
        if self.queue is not None:
            self.queue.close()
            self.queue = None
        for descriptor in list(self.handles):
            with suppress(OSError):
                os.close(descriptor)
        self.handles.clear()

    def rebuild(self) -> None:
        self.close()
        self.queue = select.kqueue()
        events: list[select.kevent] = []
        open_flags = getattr(os, "O_EVTONLY", os.O_RDONLY)
        no_follow = getattr(os, "O_NOFOLLOW", 0)
        note_flags = (
            select.KQ_NOTE_WRITE
            | select.KQ_NOTE_DELETE
            | select.KQ_NOTE_EXTEND
            | select.KQ_NOTE_ATTRIB
            | select.KQ_NOTE_LINK
            | select.KQ_NOTE_RENAME
            | select.KQ_NOTE_REVOKE
        )
        for path in iter_event_paths(self.roots):
            flags = open_flags | (no_follow if path.is_symlink() else 0)
            try:
                descriptor = os.open(path, flags)
            except OSError:
                continue
            self.handles[descriptor] = path
            events.append(
                select.kevent(
                    descriptor,
                    filter=select.KQ_FILTER_VNODE,
                    flags=select.KQ_EV_ADD | select.KQ_EV_CLEAR,
                    fflags=note_flags,
                )
            )
        if events:
            self.queue.control(events, 0, 0)
        print(f"[WATCH] active vnode paths: {len(self.handles)}", flush=True)

    def wait(self, timeout: float | None) -> bool:
        if self.queue is None:
            return False
        events = self.queue.control(None, 256, timeout)
        return bool(events)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Near-real-time watcher for obsidian-sync managed configuration"
    )
    parser.add_argument("--config", required=True, type=Path, help="Same recipient JSON used by sync")
    parser.add_argument(
        "--debounce-seconds",
        type=float,
        default=DEFAULT_DEBOUNCE_SECONDS,
    )
    parser.add_argument(
        "--retry-seconds",
        type=float,
        default=DEFAULT_RETRY_SECONDS,
    )
    parser.add_argument(
        "--sync-timeout-seconds",
        type=float,
        default=DEFAULT_SYNC_TIMEOUT_SECONDS,
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Check the content fingerprint once, synchronize if needed, then exit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.debounce_seconds < 0 or args.retry_seconds <= 0:
        print("[ERROR] debounce must be non-negative and retry must be positive", file=sys.stderr)
        return 2
    if args.sync_timeout_seconds <= 0:
        print("[ERROR] sync timeout must be positive", file=sys.stderr)
        return 2

    global SYNC_CONFIG
    SYNC_CONFIG = str(args.config.resolve())
    try:
        config = sync.load_configuration(args.config)
    except (OSError, ValueError, TypeError) as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 2
    google_drive_root = Path(config["cloud_root"])
    shared_config_root = Path(config["shared_config_root"])
    paths = configured_watch_roots(google_drive_root, shared_config_root, sync.workspace_vaults())
    state_path = Path(config["watch_state_file"])
    sync_command = Path(config["sync_command"])

    print(f"[INFO] managed roots: {len(paths)}", flush=True)
    print(f"[INFO] debounce: {args.debounce_seconds:g}s", flush=True)
    print(f"[INFO] state: {state_path}", flush=True)
    print(f"[INFO] sync entrypoint: {sync_command}", flush=True)

    successful, saved = run_sync_if_changed(
        paths,
        state_path,
        sync_command,
        args.sync_timeout_seconds,
    )
    if args.once:
        return 0 if successful else 1

    stop_requested = False

    def request_stop(_signum: int, _frame: object) -> None:
        nonlocal stop_requested
        stop_requested = True

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)

    soft_limit, hard_limit = ensure_open_file_limit()
    print(f"[INFO] open-file limit: {soft_limit}/{hard_limit}", flush=True)
    watcher = KqueueManagedPathWatcher(paths)
    retry_at = time.monotonic() + args.retry_seconds if not successful else None
    current = content_fingerprint(paths)
    if current != saved:
        print("[RETRY] managed content changed during initial watcher setup", flush=True)
        retry_at = time.monotonic()
    try:
        while not stop_requested:
            timeout = None
            if retry_at is not None:
                timeout = max(0.0, retry_at - time.monotonic())
            changed = watcher.wait(timeout)
            if stop_requested:
                break

            if changed:
                quiet_deadline = time.monotonic() + args.debounce_seconds
                while not stop_requested:
                    remaining = quiet_deadline - time.monotonic()
                    if remaining <= 0:
                        break
                    if watcher.wait(remaining):
                        quiet_deadline = time.monotonic() + args.debounce_seconds

            if not changed and retry_at is not None and time.monotonic() < retry_at:
                continue

            successful, saved = run_sync_if_changed(
                paths,
                state_path,
                sync_command,
                args.sync_timeout_seconds,
            )
            retry_at = None if successful else time.monotonic() + args.retry_seconds
            watcher.rebuild()

            current = content_fingerprint(paths)
            if current != saved:
                print("[RETRY] managed content changed during watcher rebuild", flush=True)
                retry_at = time.monotonic()
    finally:
        watcher.close()

    print("[STOP] Obsidian config watcher stopped", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
