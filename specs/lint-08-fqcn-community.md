# Task 08 — Use FQCN for community modules

## Rule

`fqcn[action]` — Use fully-qualified collection name for community module actions.

## Affected files (19 occurrences)

- `ansible/roles/mqtt_bridge/tasks/main.yml`
- `ansible/roles/os_base/tasks/main.yml`
- `ansible/roles/os_services/tasks/firewall.yml`
- `ansible/roles/zigbee2mqtt/tasks/main.yml`

## Common module mappings

| Short name | FQCN |
|------------|------|
| `ufw` | `community.general.ufw` |

Review each file for any other short community module names and apply the appropriate FQCN.

## Actions

Prefix community module names with their collection namespace throughout all affected files.

Note: the `community.general` collection must be present. Verify with:

```bash
ansible-galaxy collection list | grep community.general
```

If missing, install it:

```bash
ansible-galaxy collection install community.general
```

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml 2>&1 | grep "fqcn\[action\]"
# Expected: no output
```
