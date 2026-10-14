#!/usr/bin/env bash
set -euo pipefail
usage() {
  cat <<'EOF'
Usage: setup_obsidian_sync_watch_launchd.sh --dry-run|--apply|--verify|--unload
Required environment: LABEL PROGRAM CONFIG PLIST_DIR STATE_ROOT
PROGRAM must be the installed package wrapper; CONFIG is the recipient JSON.
Default mode previews only. All paths must be explicit absolute paths.
EOF
}
MODE=dry-run
case "${1:---dry-run}" in
  --help|-h) usage; exit 0 ;;
  --dry-run|--apply|--verify|--unload) MODE="${1:---dry-run}"; MODE="${MODE#--}" ;;
  *) usage >&2; exit 2 ;;
esac
[[ $# -le 1 ]] || { usage >&2; exit 2; }
: "${LABEL:?Set a recipient-owned LaunchAgent label}"
: "${PROGRAM:?Set the installed wrapper path}"
: "${CONFIG:?Set the recipient JSON path}"
: "${PLIST_DIR:?Set the recipient LaunchAgents directory}"
: "${STATE_ROOT:?Set an isolated watcher state/log directory}"
[[ "$LABEL" =~ ^[A-Za-z0-9][A-Za-z0-9.-]+$ ]] || exit 2
for target in "$PROGRAM" "$CONFIG" "$PLIST_DIR" "$STATE_ROOT"; do
  [[ "$target" == /* ]] || { echo "Paths must be absolute" >&2; exit 2; }
done
[[ -x "$PROGRAM" && -f "$CONFIG" ]] || { echo "Missing executable or config" >&2; exit 2; }
PLIST_PATH="$PLIST_DIR/$LABEL.plist"
LOG_DIR="$STATE_ROOT/logs"
plist_content() {
  python3 - "$LABEL" "$PROGRAM" "$CONFIG" "$LOG_DIR" <<'PY'
import plistlib, sys
label, program, config, logs = sys.argv[1:]
value = {"Label": label, "ProgramArguments": [program, "--watch", "--config", config],
         "EnvironmentVariables": {"PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"},
         "RunAtLoad": True, "KeepAlive": True, "ThrottleInterval": 10,
         "ProcessType": "Background", "LowPriorityIO": True,
         "SoftResourceLimits": {"NumberOfFiles": 1024},
         "StandardOutPath": logs + "/config-watch.stdout.log",
         "StandardErrorPath": logs + "/config-watch.stderr.log"}
sys.stdout.buffer.write(plistlib.dumps(value))
PY
}
verify() {
  /usr/bin/plutil -lint "$PLIST_PATH"
  /bin/launchctl print "gui/$(id -u)/$LABEL"
}
case "$MODE" in
  dry-run) echo "[DRY-RUN] $PLIST_PATH"; plist_content ;;
  apply)
    task_tmp_dir="$(mktemp -d)"
    trap 'rm -rf "$task_tmp_dir"' EXIT
    plist_content > "$task_tmp_dir/$LABEL.plist"
    /usr/bin/plutil -lint "$task_tmp_dir/$LABEL.plist"
    mkdir -p "$PLIST_DIR" "$LOG_DIR"
    chmod 700 "$STATE_ROOT" "$LOG_DIR"
    /usr/bin/install -m 0644 "$task_tmp_dir/$LABEL.plist" "$PLIST_PATH"
    /bin/launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
    /bin/launchctl enable "gui/$(id -u)/$LABEL"
    /bin/launchctl bootstrap "gui/$(id -u)" "$PLIST_PATH"
    verify ;;
  verify) verify ;;
  unload)
    if /bin/launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
      /bin/launchctl bootout "gui/$(id -u)/$LABEL"
    fi
    rm -f "$PLIST_PATH" ;;
esac
