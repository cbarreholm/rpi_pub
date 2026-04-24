# Task 07 — Use FQCN for builtin modules

## Rule

`fqcn[action-core]` — Use fully-qualified collection name for builtin module actions.

## Affected files (106 occurrences)

- `ansible/roles/http_reverse_proxy/handlers/main.yml`
- `ansible/roles/http_reverse_proxy/tasks/main.yml`
- `ansible/roles/http_reverse_proxy/tasks/nginx.yml`
- `ansible/roles/mosquitto/tasks/main.yml`
- `ansible/roles/mqtt_bridge/tasks/main.yml`
- `ansible/roles/os_base/tasks/main.yml`
- `ansible/roles/os_base_packages/tasks/main.yml`
- `ansible/roles/os_kernel/tasks/main.yml`
- `ansible/roles/os_services/handlers/main.yml`
- `ansible/roles/os_services/tasks/autoupdate.yml`
- `ansible/roles/os_services/tasks/fail2ban.yml`
- `ansible/roles/os_services/tasks/firewall.yml`
- `ansible/roles/os_services/tasks/main.yml`
- `ansible/roles/os_services/tasks/rsyslog.yml`
- `ansible/roles/os_services/tasks/ssh.yml`
- `ansible/roles/os_users/tasks/main.yml`
- `ansible/roles/zigbee2mqtt/tasks/main.yml`

## Common module mappings

| Short name | FQCN |
|------------|------|
| `apt` | `ansible.builtin.apt` |
| `apt_key` | `ansible.builtin.apt_key` |
| `apt_repository` | `ansible.builtin.apt_repository` |
| `command` | `ansible.builtin.command` |
| `copy` | `ansible.builtin.copy` |
| `cron` | `ansible.builtin.cron` |
| `debconf` | `ansible.builtin.debconf` |
| `file` | `ansible.builtin.file` |
| `git` | `ansible.builtin.git` |
| `import_tasks` | `ansible.builtin.import_tasks` |
| `include_tasks` | `ansible.builtin.include_tasks` |
| `lineinfile` | `ansible.builtin.lineinfile` |
| `service` | `ansible.builtin.service` |
| `systemd` | `ansible.builtin.systemd` |
| `template` | `ansible.builtin.template` |
| `user` | `ansible.builtin.user` |

## Actions

Prefix each short module name with `ansible.builtin.` throughout all affected files.

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml 2>&1 | grep "fqcn\[action-core\]"
# Expected: no output
```
