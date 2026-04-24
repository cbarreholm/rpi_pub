# Task 13 — Fix Jinja2 expression spacing

## Rule

`jinja[spacing]` — Jinja2 expressions should have consistent spacing inside the delimiters: one space after `{{` and one space before `}}`.

## Affected files (10 occurrences)

- `ansible/roles/mosquitto/tasks/main.yml`
- `ansible/roles/os_base/tasks/main.yml`
- `ansible/roles/os_kernel/tasks/main.yml`
- `ansible/roles/os_services/tasks/firewall.yml`

## Actions

Add or correct spacing inside Jinja2 delimiters:

```yaml
# Before
"{{variable}}"
"{{ variable}}"
"{{variable }}"

# After
"{{ variable }}"
```

This applies to both task arguments and string values. The fix is purely cosmetic and has no runtime impact.

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml 2>&1 | grep "jinja\[spacing\]"
# Expected: no output
```
