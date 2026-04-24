# Task 01 — Add names to all plays

## Rule

`name[play]` — All plays should be named.

## Affected files

- `ansible/prepPi.yml`
- `ansible/prepPiMosquitto.yml`
- `ansible/prepPiZigbee2Mqtt.yml`
- `ansible/prepPiHttpReverseProxy.yml`
- `ansible/prepPiMiFloraServer.yml`

## Issues to fix

Each playbook's top-level play block is missing a `name:` field.

## Actions

Add a descriptive `name:` to the play entry in each playbook. Example:

```yaml
# Before
- hosts: all
  become: yes

# After
- name: Prepare base Raspberry Pi configuration
  hosts: all
  become: true
```

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml --rules-dir '' -R -r name
# Expected: no name[play] violations
```
