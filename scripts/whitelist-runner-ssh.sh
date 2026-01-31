#!/usr/bin/env bash
set -e

ACTION="${1:?Usage: $0 add|remove}"
: "${RUNNER_IP:?RUNNER_IP is required}"
: "${SSH_WHITELIST_PROVIDER:?SSH_WHITELIST_PROVIDER is required}"

case "$ACTION" in
  add)
    case "$SSH_WHITELIST_PROVIDER" in
      cpanel)
        : "${CPANEL_SERVER:?CPANEL_SERVER is required}"
        : "${CPANEL_USERNAME:?CPANEL_USERNAME is required}"
        : "${CPANEL_API_TOKEN:?CPANEL_API_TOKEN is required}"
        resp=$(curl -sS -k -w '\n%{http_code}' -H "Authorization: whm ${CPANEL_USERNAME}:${CPANEL_API_TOKEN}" \
          "https://${CPANEL_SERVER}:2087/json-api/create_cphulk_record?list_name=white&ip=${RUNNER_IP}")
        code=$(echo "$resp" | tail -n1)
        body=$(echo "$resp" | sed '$d')
        echo "$body" | grep -qE '"result"\s*:\s*1' && [ "$code" = "200" ] || (echo "Failed to add ${RUNNER_IP} to cPHulk whitelist (HTTP ${code})" && exit 1)
        ;;
      *)
        echo "Unknown SSH_WHITELIST_PROVIDER: ${SSH_WHITELIST_PROVIDER}"
        exit 1
        ;;
    esac
    ;;
  remove)
    case "$SSH_WHITELIST_PROVIDER" in
      cpanel)
        : "${CPANEL_SERVER:?CPANEL_SERVER is required}"
        : "${CPANEL_USERNAME:?CPANEL_USERNAME is required}"
        : "${CPANEL_API_TOKEN:?CPANEL_API_TOKEN is required}"
        curl -sS -k -H "Authorization: whm ${CPANEL_USERNAME}:${CPANEL_API_TOKEN}" \
          "https://${CPANEL_SERVER}:2087/json-api/delete_cphulk_record?list_name=white&ip=${RUNNER_IP}" >/dev/null || true
        ;;
      *)
        echo "Unknown SSH_WHITELIST_PROVIDER: ${SSH_WHITELIST_PROVIDER}"
        exit 1
        ;;
    esac
    ;;
  *)
    echo "Usage: $0 add|remove"
    exit 1
    ;;
esac
