# Task 10 — Add changed_when to command tasks

## Rule

`no-changed-when` — Commands should not change things if nothing needs doing. Tasks using `command` or `shell` must declare `changed_when` to avoid falsely reporting changes on every run.

## Affected files (5 occurrences)

- `ansible/roles/http_reverse_proxy/tasks/nginx.yml`
- `ansible/roles/mosquitto/tasks/main.yml`
- `ansible/roles/mqtt_bridge/tasks/main.yml`
- `ansible/roles/zigbee2mqtt/tasks/main.yml`

## Actions

For each `command`/`shell` task, add an appropriate `changed_when` condition. Common patterns:

```yaml
# Task that is effectively read-only / idempotent — never reports changed
- name: Verify configuration syntax
  ansible.builtin.command: nginx -t
  changed_when: false

# Task whose output indicates a change
- name: Install npm dependencies
  ansible.builtin.command: npm install
  args:
    chdir: /opt/app
  register: npm_result
  changed_when: "'added' in npm_result.stdout"
```

Review each flagged task individually to choose the most accurate condition. If the command is truly side-effect-free (e.g. a check or query), use `changed_when: false`.

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml 2>&1 | grep "no-changed-when"
# Expected: no output
```
