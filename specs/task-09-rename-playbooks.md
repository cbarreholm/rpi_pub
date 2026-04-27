# Task 09 — Rename Playbooks

**Type:** Implementation
**Requirements:** §2.8 REQ-PLY-01, REQ-PLY-03 – REQ-PLY-06

## Changes required

### Renames
| Current filename | New filename |
|---|---|
| `ansible/prepPi.yml` | `ansible/prepPiServer.yml` |
| `ansible/prepPiMosquitto.yml` | `ansible/prepMosquitto.yml` |
| `ansible/prepPiHttpReverseProxy.yml` | `ansible/prepHttpReverseProxy.yml` |
| `ansible/prepPiZigbee2Mqtt.yml` | `ansible/prepZigbee2Mqtt.yml` |
| `ansible/prepPiMiFloraServer.yml` | `ansible/prepMiFloraServer.yml` |

### Follow-up updates
After renaming, update all references to the old filenames in:
- `README.md` — usage examples and playbook descriptions
- `AGENTS.md` — "Available playbooks" list

## Notes
- This is a pure rename with no functional changes.
- Verify with `ansible-playbook --syntax-check` after renaming.
