# Task 02 — Fix task naming issues

## Rules

- `name[missing]` — Tasks must have a name.
- `name[casing]` — Task names should start with an uppercase letter.
- `name[template]` — Task names should not use Jinja2 templating as the sole content.

## Affected files

| File | Rules |
|------|-------|
| `ansible/roles/http_reverse_proxy/tasks/main.yml` | `name[missing]` |
| `ansible/roles/os_services/tasks/main.yml` | `name[missing]` |
| `ansible/roles/os_base/tasks/main.yml` | `name[casing]`, `name[template]` |
| `ansible/roles/http_reverse_proxy/tasks/nginx.yml` | `name[template]` |
| `ansible/roles/os_users/tasks/main.yml` | `name[template]` |

## Actions

- Add `name:` fields to any tasks that are missing them.
- Capitalize the first word of any task names that start lowercase.
- Replace bare Jinja2 template names with descriptive static strings (the variable value can remain in the task body).

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml 2>&1 | grep -E "^(ansible/|  ).*name\["
# Expected: no output
```
