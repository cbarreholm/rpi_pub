# Task 06 — Fix miscellaneous YAML formatting

## Rules

- `yaml[indentation]` — Wrong indentation level.
- `yaml[empty-lines]` — Too many blank lines.
- `yaml[comments]` — Comment formatting (missing space after `#`).

## Affected files

| File | Rules |
|------|-------|
| `ansible/roles/mqtt_bridge/tasks/main.yml` | `yaml[indentation]` |
| `ansible/roles/os_kernel/tasks/main.yml` | `yaml[indentation]` |
| `ansible/roles/zigbee2mqtt/tasks/main.yml` | `yaml[indentation]` |
| `ansible/roles/http_reverse_proxy/vars/main.yml` | `yaml[empty-lines]`, `yaml[comments]` |
| `ansible/roles/os_base/tasks/main.yml` | `yaml[empty-lines]` |
| `ansible/roles/os_base_packages/tasks/main.yml` | `yaml[empty-lines]` |
| `ansible/roles/os_services/tasks/fail2ban.yml` | `yaml[empty-lines]` |
| `ansible/roles/os_services/tasks/firewall.yml` | `yaml[empty-lines]` |
| `ansible/roles/os_services/tasks/rsyslog.yml` | `yaml[comments]` |
| `ansible/roles/os_services/tasks/ssh.yml` | `yaml[comments]` |
| `ansible/roles/zigbee2mqtt/vars/main.yml` | `yaml[empty-lines]` |

## Actions

- **Indentation**: fix task module argument indentation to use consistent 2-space indent (module key at column 4, args at column 6).
- **Empty lines**: reduce consecutive blank lines to a maximum of 1.
- **Comments**: ensure inline/standalone comments have a space after `#` (e.g. `# comment` not `#comment`).

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml 2>&1 | grep -E "yaml\[(indentation|empty-lines|comments)\]"
# Expected: no output
```
