#!/usr/bin/env bash
# Push local.settings.json Values to Azure Function App (Flex Consumption safe).
# Usage: ./scripts/push_app_settings.sh macroboard Macroboard

set -euo pipefail

APP_NAME="${1:-macroboard}"
RESOURCE_GROUP="${2:-Macroboard}"
SETTINGS_FILE="$(cd "$(dirname "$0")/.." && pwd)/local.settings.json"

if [[ ! -f "$SETTINGS_FILE" ]]; then
  echo "ERROR: $SETTINGS_FILE not found"
  exit 1
fi

python3 - <<PY
import json, re, subprocess, sys
path = "$SETTINGS_FILE"
skip = re.compile(r"^(AzureWebJobsStorage|FUNCTIONS_WORKER_RUNTIME|FUNCTIONS_EXTENSION_VERSION)$")
data = json.load(open(path, encoding="utf-8"))
pairs = []
for k, v in data["Values"].items():
    if skip.match(k):
        continue
    if k.startswith("AZURE_SEARCH_") and ("YOUR-" in str(v) or "your_" in str(v)):
        continue
    pairs.append(f"{k}={v}")
cmd = ["az", "functionapp", "config", "appsettings", "set",
       "--resource-group", "$RESOURCE_GROUP", "--name", "$APP_NAME", "--settings"] + pairs
print(f"Pushing {len(pairs)} settings (skips FUNCTIONS_WORKER_RUNTIME)...")
subprocess.check_call(cmd)
PY

echo "Done."
