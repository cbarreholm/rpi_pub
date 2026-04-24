# Task 12 — Prefix variables with role name

## Rule

`var-naming[no-role-prefix]` — Variables defined in a role should be prefixed with the role name to avoid collisions with variables from other roles or the playbook scope.

## Affected files (21 occurrences)

- `ansible/roles/http_reverse_proxy/vars/main.yml`
- `ansible/roles/os_base/tasks/main.yml`
- `ansible/roles/os_base/vars/Debian-10.yml`
- `ansible/roles/os_base/vars/Debian-12.yml`
- `ansible/roles/os_base/vars/main.yml`
- `ansible/roles/os_kernel/tasks/main.yml`
- `ansible/roles/os_services/vars/main.yml`

## Actions

Rename each variable to include the role name as a prefix. Update all references to the variable in the same role's tasks, templates, and handlers.

Naming convention: `<role_name>_<variable_name>`

```yaml
# Role: os_base
# Before
vars/main.yml:
  packages: [...]

tasks/main.yml:
  loop: "{{ packages }}"

# After
vars/main.yml:
  os_base_packages: [...]

tasks/main.yml:
  loop: "{{ os_base_packages }}"
```

Run a grep across each role directory to find all references before renaming:

```bash
grep -r "<variable_name>" ansible/roles/<role>/
```

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml 2>&1 | grep "var-naming\[no-role-prefix\]"
# Expected: no output
```
