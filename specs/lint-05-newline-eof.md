# Task 05 — Add missing newline at end of files

## Rule

`yaml[new-line-at-end-of-file]` — File must end with a newline character.

## Affected files (33 occurrences)

- `ansible/roles/http_reverse_proxy/defaults/main.yml`
- `ansible/roles/http_reverse_proxy/meta/main.yml`
- `ansible/roles/mosquitto/defaults/main.yml`
- `ansible/roles/mosquitto/handlers/main.yml`
- `ansible/roles/mosquitto/meta/main.yml`
- `ansible/roles/mqtt_bridge/defaults/main.yml`
- `ansible/roles/mqtt_bridge/handlers/main.yml`
- `ansible/roles/mqtt_bridge/meta/main.yml`
- `ansible/roles/os_base/defaults/main.yml`
- `ansible/roles/os_base/handlers/main.yml`
- `ansible/roles/os_base/meta/main.yml`
- `ansible/roles/os_base/vars/Debian-10.yml`
- `ansible/roles/os_base/vars/Debian-12.yml`
- `ansible/roles/os_base_packages/defaults/main.yml`
- `ansible/roles/os_base_packages/handlers/main.yml`
- `ansible/roles/os_base_packages/meta/main.yml`
- `ansible/roles/os_base_packages/vars/main.yml`
- `ansible/roles/os_kernel/defaults/main.yml`
- `ansible/roles/os_kernel/handlers/main.yml`
- `ansible/roles/os_kernel/meta/main.yml`
- `ansible/roles/os_kernel/tasks/main.yml`
- `ansible/roles/os_kernel/vars/main.yml`
- `ansible/roles/os_services/defaults/main.yml`
- `ansible/roles/os_services/handlers/main.yml`
- `ansible/roles/os_services/meta/main.yml`
- `ansible/roles/os_services/tasks/rsyslog.yml`
- `ansible/roles/os_services/tasks/ssh.yml`
- `ansible/roles/os_services/vars/main.yml`
- `ansible/roles/os_users/defaults/main.yml`
- `ansible/roles/os_users/handlers/main.yml`
- `ansible/roles/zigbee2mqtt/defaults/main.yml`
- `ansible/roles/zigbee2mqtt/handlers/main.yml`
- `ansible/roles/zigbee2mqtt/meta/main.yml`

## Actions

Ensure each file ends with exactly one newline. Can be done with:

```bash
# Check: file does not end with newline if this has output
tail -c1 <file> | xxd

# Fix
echo "" >> <file>
# or
sed -i -e '$a\' <file>
```

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml 2>&1 | grep "yaml\[new-line-at-end-of-file\]"
# Expected: no output
```
