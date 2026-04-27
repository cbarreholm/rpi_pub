# Task 10 — Add generic_server Inventory Group and Create prepGenericHwServer.yml

**Type:** Implementation
**Requirements:** §2.1 REQ-PLT-01, §2.8 REQ-PLY-02

## Changes required

### 1. Update inventory
File: `ansible/inventory.yaml`

Add a `generic_server` host group alongside the existing `pi_server` group.
Per-host variables must support at minimum:
- `ansible_user` — the initial connection user (e.g. `debian`)
- `ansible_host` — IP or hostname

Example structure:
```yaml
generic_server:
  hosts:
    my-vps:
      ansible_host: 1.2.3.4
      ansible_user: debian
```

### 2. Create prepGenericHwServer.yml
File: `ansible/prepGenericHwServer.yml`

Create a new top-level playbook targeting `generic_server` hosts.
Include the same roles as `prepPiServer.yml` — the platform gating introduced in
tasks 11–15 will ensure RPi-specific tasks are skipped automatically:

```yaml
- hosts: generic_server
  gather_facts: true
  roles:
    - { role: os_users }
    - { role: os_base }
    - { role: os_kernel }
    - { role: os_base_packages }
    - { role: os_services }
```

## Dependencies
Tasks 11–15 must be completed for this playbook to run correctly on generic hosts.

## Verification
Run syntax check:
```
ansible-playbook --syntax-check -i ansible/inventory.yaml \
  -e @ansible/secrets/secrets_file.enc \
  --vault-password-file ansible/secrets/vault_password_file \
  ansible/prepGenericHwServer.yml
```
