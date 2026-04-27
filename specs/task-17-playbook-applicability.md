# Task 17 — Document Playbook Applicability in README

**Type:** Implementation
**Requirements:** §2.8 REQ-PLY-07 – REQ-PLY-10

## Background
After the renames in task 09, several playbooks are platform-agnostic while others
require specific hardware. The README must clearly document which playbooks can be
used on which targets so operators don't attempt to run hardware-dependent playbooks
on unsuitable hosts.

## Changes required

File: `README.md`

### 1. Add a Playbooks reference table
Add a section (or update the existing Features/Usage section) with a table:

| Playbook | Target group | Hardware requirement |
|---|---|---|
| `prepPiServer.yml` | `pi_server` | Raspberry Pi |
| `prepGenericHwServer.yml` | `generic_server` | Any Debian x86/ARM |
| `prepMosquitto.yml` | any | None |
| `prepHttpReverseProxy.yml` | any | None |
| `prepZigbee2Mqtt.yml` | any | Zigbee USB adapter |
| `prepMiFloraServer.yml` | any | Bluetooth hardware |

### 2. Update usage examples
Replace any references to old playbook names with the new names from task 09.

### 3. Update AGENTS.md
File: `AGENTS.md`

Update the "Available playbooks" list to reflect the new names:
```
prepPiServer.yml, prepGenericHwServer.yml, prepMosquitto.yml,
prepHttpReverseProxy.yml, prepZigbee2Mqtt.yml, prepMiFloraServer.yml
```

## Notes
- This task has no code changes — documentation only.
- Should be done after task 09 (renames) is complete.
