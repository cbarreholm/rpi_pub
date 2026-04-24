# Task 09 — Set explicit file permissions

## Rule

`risky-file-permissions` — File permissions unset or incorrect. Tasks using `copy`, `template`, `file`, or similar modules that create or modify files should set an explicit `mode:`.

## Affected files (29 occurrences)

- `ansible/roles/mosquitto/tasks/main.yml`
- `ansible/roles/mqtt_bridge/tasks/main.yml`
- `ansible/roles/os_base/tasks/main.yml`
- `ansible/roles/os_kernel/tasks/main.yml`
- `ansible/roles/zigbee2mqtt/tasks/main.yml`

## Actions

Add an explicit `mode:` to each flagged task. Choose the appropriate permission based on the file type:

| File type | Recommended mode |
|-----------|-----------------|
| Configuration file (root-owned) | `"0640"` or `"0644"` |
| Configuration file (world-readable) | `"0644"` |
| Directory | `"0755"` or `"0750"` |
| Executable / script | `"0755"` |
| Secret / credential file | `"0600"` |

Use quoted octal strings (e.g. `"0644"`) to avoid YAML interpreting them as integers.

```yaml
# Example
- name: Copy configuration file
  ansible.builtin.copy:
    src: mosquitto.conf
    dest: /etc/mosquitto/mosquitto.conf
    owner: mosquitto
    group: mosquitto
    mode: "0640"
```

Review each task individually — the correct mode depends on the sensitivity and intended audience of the file.

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml 2>&1 | grep "risky-file-permissions"
# Expected: no output
```
