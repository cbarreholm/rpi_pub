# Task 11 — Fix role metadata

## Rules

- `meta-incorrect` — Default metadata values (author, company, license) have not been updated from the role scaffold defaults.
- `schema[meta]` — `min_ansible_version` must be a string, not a float.

## Affected files (32 occurrences across 8 roles)

- `ansible/roles/http_reverse_proxy/meta/main.yml`
- `ansible/roles/mosquitto/meta/main.yml`
- `ansible/roles/mqtt_bridge/meta/main.yml`
- `ansible/roles/os_base/meta/main.yml`
- `ansible/roles/os_base_packages/meta/main.yml`
- `ansible/roles/os_kernel/meta/main.yml`
- `ansible/roles/os_services/meta/main.yml`
- `ansible/roles/zigbee2mqtt/meta/main.yml`

## Issues to fix

| Field | Current | Target |
|-------|---------|--------|
| `author` | `your name` (scaffold default) | Actual author name |
| `company` | `your company` (scaffold default) | Actual value or remove |
| `license` | `license (GPL-2.0-or-later)` (scaffold default) | Actual license or `MIT` |
| `min_ansible_version` | `2.9` (float) | `"2.9"` (string) |

## Actions

Update each `meta/main.yml`:

1. Set `author`, `company`, `license` to appropriate values.
2. Quote `min_ansible_version` as a string: `min_ansible_version: "2.9"`.

```yaml
# Before
galaxy_info:
  author: your name
  company: your company
  license: license (GPL-2.0-or-later)
  min_ansible_version: 2.9

# After
galaxy_info:
  author: cbarreholm
  company: ""
  license: MIT
  min_ansible_version: "2.9"
```

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml 2>&1 | grep -E "(meta-incorrect|schema\[meta\])"
# Expected: no output
```
