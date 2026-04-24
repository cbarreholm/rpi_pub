# Task 04 — Remove trailing whitespace

## Rule

`yaml[trailing-spaces]` — No trailing spaces allowed.

## Affected files (120 occurrences)

- `ansible/roles/http_reverse_proxy/meta/main.yml`
- `ansible/roles/http_reverse_proxy/tasks/nginx.yml`
- `ansible/roles/mosquitto/meta/main.yml`
- `ansible/roles/mosquitto/tasks/main.yml`
- `ansible/roles/mqtt_bridge/meta/main.yml`
- `ansible/roles/mqtt_bridge/tasks/main.yml`
- `ansible/roles/os_base/meta/main.yml`
- `ansible/roles/os_base/tasks/main.yml`
- `ansible/roles/os_base_packages/meta/main.yml`
- `ansible/roles/os_base_packages/tasks/main.yml`
- `ansible/roles/os_kernel/meta/main.yml`
- `ansible/roles/os_kernel/tasks/main.yml`
- `ansible/roles/os_services/meta/main.yml`
- `ansible/roles/os_services/tasks/autoupdate.yml`
- `ansible/roles/os_services/tasks/fail2ban.yml`
- `ansible/roles/os_services/tasks/firewall.yml`
- `ansible/roles/os_services/tasks/rsyslog.yml`
- `ansible/roles/os_services/tasks/ssh.yml`
- `ansible/roles/os_services/vars/main.yml`
- `ansible/roles/os_users/tasks/main.yml`
- `ansible/roles/zigbee2mqtt/meta/main.yml`
- `ansible/roles/zigbee2mqtt/tasks/main.yml`

## Actions

Strip trailing whitespace from all lines in the affected files. This is a mechanical change with no semantic impact.

Can be done in bulk:

```bash
sed -i 's/[[:space:]]*$//' <file>
```

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml 2>&1 | grep "yaml\[trailing-spaces\]"
# Expected: no output
```
