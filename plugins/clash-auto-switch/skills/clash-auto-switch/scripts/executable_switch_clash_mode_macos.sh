#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  echo "Usage: switch_clash_mode_macos.sh tun|system|sys|status [--json]; use clash-tool --config"
  exit 0
fi

MODE="${1:-status}"
JSON_OUTPUT="0"
if [[ "${2:-}" == "--json" || "${1:-}" == "--json" ]]; then
  JSON_OUTPUT="1"
  if [[ "${1:-}" == "--json" ]]; then
    MODE="status"
  fi
fi

: "${RUNTIME_ROOT:?Use clash-tool --config}"
PROFILES_YAML="$RUNTIME_ROOT/profiles.yaml"
CFG="$RUNTIME_ROOT/config.yaml"
VERGE_YAML="$RUNTIME_ROOT/verge.yaml"
SOCK="${CLASH_SOCK:-}"
CONTROLLER_URL="${CLASH_CONTROLLER_URL:-}"
CLASH_APP="${CLASH_APP:-Clash Verge}"
GUARD_BIN="${GUARD_BIN:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DNS_HELPER="${CLASH_MODE_DNS_HELPER:-$SCRIPT_DIR/clash_mode_dns.py}"

usage() {
  echo "Usage: $(basename "$0") tun|system|sys|status [--json]" >&2
}

dns_helper() {
  if [[ ! -f "$DNS_HELPER" ]]; then
    echo "[error] DNS mode helper not found: $DNS_HELPER" >&2
    return 1
  fi
  "${PY_BIN:?Configured Python required}" "$DNS_HELPER" "$@"
}

run_dns_action() {
  if [[ "$JSON_OUTPUT" == "1" ]]; then
    dns_helper "$@" --json >/dev/null
  else
    dns_helper "$@"
  fi
}

api_call() {
  local method="$1"
  local path="$2"
  local body="${3:-}"
  local args=(request "$method" "$path")
  if [[ -n "$body" ]]; then
    args+=(--body "$body")
  fi
  "${PY_BIN:?Configured Python required}" "$SCRIPT_DIR/clash_controller.py" "${args[@]}"
}

controller_available() {
  api_call GET /configs >/dev/null 2>&1
}

current_profile() {
  if [[ ! -f "$PROFILES_YAML" ]]; then
    return 0
  fi
  "${PY_BIN:?Configured Python required}" - "$PROFILES_YAML" <<'PY'
import re
import sys
from pathlib import Path
for line in Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore").splitlines():
    m = re.match(r"^\s*current:\s*([^\s#]+)", line)
    if m:
        print(m.group(1).strip("'\""))
        break
PY
}

controller_selectors() {
  api_call GET /proxies | "${PY_BIN:?Configured Python required}" -c '
import json
import sys
raw = sys.stdin.read()
data = json.loads(raw) if raw.strip() else {}
selectors = {}
for name, payload in data.get("proxies", {}).items():
    if isinstance(payload, dict) and isinstance(payload.get("now"), str):
        selectors[name] = payload["now"]
print(json.dumps(selectors, ensure_ascii=False, sort_keys=True))
'
}

restore_selectors() {
  local selectors_json="$1"
  printf '%s' "$selectors_json" | "${PY_BIN:?Configured Python required}" -c '
import json
import sys
for group, selected in json.loads(sys.stdin.read() or "{}").items():
    print(f"{group}\t{selected}")
' | while IFS=$'\t' read -r group selected; do
    [[ -n "$group" && -n "$selected" ]] || continue
    api_call PUT "/proxies/$("${PY_BIN:?Configured Python required}" -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$group")" "{\"name\":\"$("${PY_BIN:?Configured Python required}" -c 'import json,sys; print(json.dumps(sys.argv[1])[1:-1])' "$selected")\"}" >/dev/null
  done
}

set_verge_ui_state() {
  local tun_enable="$1"
  local sys_enable="$2"
  if [[ ! -f "$VERGE_YAML" ]]; then
    return 0
  fi
  "${PY_BIN:?Configured Python required}" - "$VERGE_YAML" "$tun_enable" "$sys_enable" <<'PY'
import re
import sys
from pathlib import Path
path = Path(sys.argv[1])
tun = sys.argv[2]
system_proxy = sys.argv[3]
raw = path.read_text(encoding="utf-8", errors="ignore")
def upsert(text: str, key: str, val: str) -> str:
    pattern = rf"(?m)^{re.escape(key)}:\s*[^\r\n]*$"
    repl = f"{key}: {val}"
    if re.search(pattern, text):
        return re.sub(pattern, repl, text)
    if not text.endswith("\n"):
        text += "\n"
    return text + repl + "\n"
raw = upsert(raw, "enable_tun_mode", tun)
raw = upsert(raw, "enable_system_proxy", system_proxy)
path.write_text(raw, encoding="utf-8")
PY
}

restart_gui_if_needed() {
  if controller_available; then
    return 0
  fi
  open -a "$CLASH_APP" >/dev/null 2>&1 || true
  local i
  for ((i = 0; i < 30; i++)); do
    if controller_available; then
      return 0
    fi
    sleep 1
  done
  echo "[error] Clash controller unavailable after GUI start" >&2
  return 1
}

verify_preserved() {
  local before_profile="$1"
  local before_selectors="$2"
  local after_profile after_selectors
  after_profile="$(current_profile || true)"
  if [[ -n "$before_profile" && -n "$after_profile" && "$before_profile" != "$after_profile" ]]; then
    echo "[error] active profile changed: $before_profile -> $after_profile" >&2
    return 1
  fi
  after_selectors="$(controller_selectors)"
  if [[ "$before_selectors" != "$after_selectors" ]]; then
    restore_selectors "$before_selectors"
    after_selectors="$(controller_selectors)"
  fi
  if [[ "$before_selectors" != "$after_selectors" ]]; then
    echo "[error] selector preservation failed" >&2
    return 1
  fi
}

set_guard_mode() {
  local desired="$1"
  if [[ -x "$GUARD_BIN" ]]; then
    "$GUARD_BIN" _set-desired-mode "$desired"
    return
  fi
  "${PY_BIN:?Configured Python required}" - "$desired" <<'PY'
import json
import os
import sys
import tempfile
from pathlib import Path
desired = sys.argv[1]
state_dir = Path(os.environ["CLASH_GUARD_MODE_STATE_DIR"])
path = state_dir / "desired_mode.json"
state = {"desired_mode": desired}
state_dir.mkdir(parents=True, exist_ok=True)
with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=state_dir, delete=False) as handle:
    json.dump(state, handle, ensure_ascii=False, indent=2, sort_keys=True)
    handle.write("\n")
    temp = Path(handle.name)
temp.replace(path)
PY
}

show_status() {
  local raw profile selectors system_dns
  profile="$(current_profile || true)"
  selectors="{}"
  if controller_available; then
    raw="$(api_call GET /configs || true)"
    selectors="$(controller_selectors || printf '{}')"
  else
    raw='{}'
  fi
  system_dns="$(dns_helper status --json 2>/dev/null || printf '{"available":false}')"
  if [[ "$JSON_OUTPUT" == "1" ]]; then
    "${PY_BIN:?Configured Python required}" - "$raw" "$profile" "$selectors" "$system_dns" <<'PY'
import json
import sys
configs = json.loads(sys.argv[1] or "{}")
print(json.dumps({
    "tun": configs.get("tun"),
    "dns": configs.get("dns"),
    "mixed-port": configs.get("mixed-port"),
    "profile": sys.argv[2] or None,
    "selectors": json.loads(sys.argv[3] or "{}"),
    "system-dns": json.loads(sys.argv[4] or "{}"),
}, ensure_ascii=False, sort_keys=True))
PY
  else
    "${PY_BIN:?Configured Python required}" - "$raw" "$profile" <<'PY'
import json
import sys
configs = json.loads(sys.argv[1] or "{}")
tun = configs.get("tun", {}).get("enable", "unknown") if isinstance(configs.get("tun"), dict) else "unknown"
if isinstance(tun, bool):
    tun = str(tun).lower()
print(f"tun.enable={tun}")
print(f"mixed-port={configs.get('mixed-port', 'unknown')}")
PY
    dns_helper status || true
  fi
}

apply_clash_mode_runtime() {
  local tun_enable="$1"
  local sys_enable="$2"
  local before_profile="$3"
  local before_selectors="$4"
  set_verge_ui_state "$tun_enable" "$sys_enable" || return
  restart_gui_if_needed || return
  if [[ -z "$before_selectors" ]]; then
    before_selectors="$(controller_selectors)" || return
  fi
  api_call PATCH /configs "{\"tun\":{\"enable\":$tun_enable}}" >/dev/null || return
  verify_tun_state "$tun_enable" || return
  verify_preserved "$before_profile" "$before_selectors" || return
}

verify_tun_state() {
  local expected="$1" current attempt
  for ((attempt = 0; attempt < 20; attempt++)); do
    current="$(api_call GET /configs | "${PY_BIN:?Configured Python required}" -c 'import json,sys; print(str(json.load(sys.stdin)["tun"]["enable"]).lower())')" || return
    [[ "$current" == "$expected" ]] && return 0
    sleep 0.2
  done
  echo "[error] TUN state did not converge to $expected" >&2
  return 1
}

complete_mode_transition() {
  local desired="$1"
  local tun_enable="$2"
  local sys_enable="$3"
  local before_profile="$4" before_selectors="$5" checkpoint="$6" port="$7"

  # Restore the exact pre-TUN DNS state before disabling TUN. The restore
  # snapshot remains until controller/UI/guard convergence succeeds.
  if [[ "$desired" == "system" ]]; then
    run_dns_action prepare-system || return
  fi

  # Establish and verify actual service proxies before disabling TUN. Verge's
  # persisted preference alone does not update macOS while its GUI is running.
  if [[ "$desired" == "system" ]]; then
    dns_helper set-proxy --checkpoint "$checkpoint" --enabled true --port "$port" >&2 || return
  fi
  apply_clash_mode_runtime "$tun_enable" "$sys_enable" "$before_profile" "$before_selectors" || return

  # Install the managed DNS only after the TUN route and Mihomo DNS endpoint
  # have been verified by the helper.
  if [[ "$desired" == "tun" ]]; then
    run_dns_action apply-tun || return
    dns_helper set-proxy --checkpoint "$checkpoint" --enabled false --port "$port" >&2 || return
  fi

  set_guard_mode "$desired" || return
  if [[ "$desired" == "system" ]]; then
    run_dns_action commit-system || return
  fi
}

switch_mode() {
  local desired="$1" tun_enable="$2" sys_enable="$3"
  local before_profile before_selectors before_tun port checkpoint transaction_dir before_configs
  restart_gui_if_needed || return
  before_profile="$(current_profile)" || return
  before_selectors="$(controller_selectors)" || return
  before_configs="$(api_call GET /configs)" || return
  before_tun="$(printf '%s' "$before_configs" | "${PY_BIN:?Configured Python required}" -c 'import json,sys; print(str(json.load(sys.stdin)["tun"]["enable"]).lower())')" || return
  port="$(printf '%s' "$before_configs" | "${PY_BIN:?Configured Python required}" -c 'import json,sys; print(json.load(sys.stdin)["mixed-port"])')" || return
  transaction_dir="$(mktemp -d "${TMPDIR:-/tmp}/clash-mode.XXXXXX")" || return
  checkpoint="$transaction_dir/before.json"
  export CLASH_MODE_VERGE_FILE="$VERGE_YAML"
  export CLASH_MODE_GUARD_FILE="${CLASH_GUARD_MODE_STATE_DIR:?Configured mode state directory required}/desired_mode.json"
  if ! dns_helper checkpoint --checkpoint "$checkpoint" >&2; then
    rm -rf "$transaction_dir"
    return 1
  fi

  if ! complete_mode_transition "$desired" "$tun_enable" "$sys_enable" "$before_profile" "$before_selectors" "$checkpoint" "$port"; then
    echo "[warning] mode transition failed; restoring prior runtime and network state" >&2
    local restored=1
    if [[ "$before_tun" == "true" ]]; then
      api_call PATCH /configs '{"tun":{"enable":true}}' >/dev/null && verify_tun_state true || restored=0
    fi
    dns_helper restore-transition --checkpoint "$checkpoint" >&2 || restored=0
    if [[ "$before_tun" == "false" ]]; then
      api_call PATCH /configs '{"tun":{"enable":false}}' >/dev/null && verify_tun_state false || restored=0
    fi
    restore_selectors "$before_selectors" && verify_preserved "$before_profile" "$before_selectors" || restored=0
    if [[ "$restored" == "1" ]]; then
      rm -rf "$transaction_dir"
      echo "[ok] prior mode and network state restored" >&2
    else
      echo "[error] incomplete rollback; retained recovery checkpoint: $checkpoint" >&2
    fi
    return 1
  fi
  rm -rf "$transaction_dir"

  if [[ "$JSON_OUTPUT" == "1" ]]; then
    show_status
  else
    echo "[ok] mode=$desired tun.enable=$tun_enable"
    show_status
  fi
}

case "$MODE" in
  tun)
    switch_mode tun true false
    ;;
  system|sys)
    switch_mode system false true
    ;;
  status)
    show_status
    ;;
  -h|--help)
    usage
    ;;
  *)
    usage
    exit 2
    ;;
esac
