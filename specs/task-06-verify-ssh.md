# Task 06 — Verify SSH Hardening

**Type:** Verification
**Requirements:** §1.6 REQ-SSH-01 – REQ-SSH-08

## What to verify

File: `ansible/roles/os_services/tasks/ssh.yml`

### REQ-SSH-01 — Key-only authentication
Confirm `lineinfile` tasks set:
- `PasswordAuthentication no`
- `PermitEmptyPasswords no`
- `UsePAM no`

### REQ-SSH-02 — No root login
Confirm a `lineinfile` task sets `PermitRootLogin no`.

### REQ-SSH-03 — Restricted to ssh-users group
Confirm a `lineinfile` task sets `AllowGroups ssh-users`.

### REQ-SSH-04 — IPv4 only
Confirm a `lineinfile` task sets `AddressFamily inet` and `ListenAddress 0.0.0.0`.

### REQ-SSH-05 — Forwarding disabled
Confirm `lineinfile` tasks set:
- `AllowTcpForwarding no`
- `AllowAgentForwarding no`
- `X11Forwarding no`

### REQ-SSH-06 — Restricted algorithms
Confirm `lineinfile` tasks set:
- `Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com`
- `MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com`
- `KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group14-sha256`

### REQ-SSH-07 — Limited auth attempts and sessions
Confirm `lineinfile` tasks set:
- `MaxAuthTries 3`
- `MaxSessions 2`
- `ClientAliveCountMax 2`
- `LoginGraceTime 30`

### REQ-SSH-08 — VERBOSE log level
Confirm a `lineinfile` task sets `LogLevel VERBOSE`.

## Pass criteria
All checks pass with no code changes required.
Any gap must be noted and a follow-up task created.
