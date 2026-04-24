# Task 03 — Replace yes/no with true/false

## Rule

`yaml[truthy]` — Truthy value should be one of `[false, true]`.

## Affected files (134 occurrences)

- `ansible/prepPi.yml`
- `ansible/prepPiHttpReverseProxy.yml`
- `ansible/prepPiMiFloraServer.yml`
- `ansible/prepPiMosquitto.yml`
- `ansible/prepPiZigbee2Mqtt.yml`
- `ansible/roles/http_reverse_proxy/handlers/main.yml`
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
- `ansible/roles/os_services/tasks/rsyslog.yml`
- `ansible/roles/os_services/tasks/ssh.yml`
- `ansible/roles/os_users/tasks/main.yml`
- `ansible/roles/zigbee2mqtt/tasks/main.yml`

## Actions

Replace all bare `yes` and `no` YAML values with `true` and `false` respectively. This applies to fields such as `become:`, `enabled:`, `state:` (where boolean), etc.

```yaml
# Before
become: yes
notify: restart service

# After
become: true
notify: restart service
```

Note: do not replace `yes`/`no` inside quoted strings or when they are not YAML booleans (e.g. `state: present` is unaffected).

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml 2>&1 | grep "yaml\[truthy\]"
# Expected: no output
```
