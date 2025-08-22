#!/usr/bin/env bash
set -euo pipefail

# Print the MCP Inspector URL for DevNet DevEnv proxy
# Requires the following env vars (provided by DevEnv):
#   DEVENV_APP_8080_URL, DEVENV_PASSWORD, DEVENV_APP_8081_URL

missing=()
[[ -z "${DEVENV_APP_8080_URL:-}" ]] && missing+=(DEVENV_APP_8080_URL)
[[ -z "${DEVENV_PASSWORD:-}" ]] && missing+=(DEVENV_PASSWORD)
[[ -z "${DEVENV_APP_8081_URL:-}" ]] && missing+=(DEVENV_APP_8081_URL)

if [[ ${#missing[@]} -gt 0 ]]; then
  echo "Missing required environment variables: ${missing[*]}" >&2
  exit 1
fi

url="${DEVENV_APP_8080_URL}?MCP_PROXY_AUTH_TOKEN=${DEVENV_PASSWORD}&MCP_PROXY_FULL_ADDRESS=${DEVENV_APP_8081_URL}"
echo "$url"

