# Task 14 — Fix miscellaneous task issues

## Rules

- `no-free-form` — Avoid free-form module invocation; use the full key/value syntax instead.
- `command-instead-of-shell` — Use `ansible.builtin.command` instead of `ansible.builtin.shell` when no shell features (pipes, redirects, etc.) are needed.
- `latest[git]` — Avoid using `version: HEAD` or equivalent in `ansible.builtin.git`; pin to a specific tag or commit for reproducibility.

## Affected files (3 occurrences)

| File | Rule |
|------|------|
| `ansible/roles/os_base/tasks/main.yml` | `no-free-form` |
| `ansible/roles/http_reverse_proxy/tasks/nginx.yml` | `command-instead-of-shell` |
| `ansible/roles/zigbee2mqtt/tasks/main.yml` | `latest[git]` |

## Actions

### no-free-form

Convert free-form module calls to key/value syntax:

```yaml
# Before
- name: Run command
  ansible.builtin.command: echo hello

# After
- name: Run command
  ansible.builtin.command:
    cmd: echo hello
```

### command-instead-of-shell

Replace `ansible.builtin.shell` with `ansible.builtin.command` where the command does not use shell features:

```yaml
# Before
- name: Check nginx config
  ansible.builtin.shell: nginx -t

# After
- name: Check nginx config
  ansible.builtin.command: nginx -t
```

If the task genuinely requires shell features (pipes, `&&`, variable expansion, etc.), add a `# noqa: command-instead-of-shell` comment with justification.

### latest[git]

Pin the `version:` in git tasks to a specific tag or commit SHA instead of a moving target:

```yaml
# Before
- name: Clone repository
  ansible.builtin.git:
    repo: https://github.com/example/repo.git
    dest: /opt/app
    version: HEAD

# After
- name: Clone repository
  ansible.builtin.git:
    repo: https://github.com/example/repo.git
    dest: /opt/app
    version: "v1.2.3"  # pin to a release tag
```

## Verification

```bash
ansible-lint ansible/prepPi.yml ansible/prepPiMosquitto.yml ansible/prepPiZigbee2Mqtt.yml ansible/prepPiHttpReverseProxy.yml ansible/prepPiMiFloraServer.yml 2>&1 | grep -E "(no-free-form|command-instead-of-shell|latest\[git\])"
# Expected: no output
```
