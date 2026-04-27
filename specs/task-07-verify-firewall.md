# Task 07 — Verify Firewall

**Type:** Verification
**Requirements:** §1.7 REQ-FW-01 – REQ-FW-10

## What to verify

File: `ansible/roles/os_services/tasks/firewall.yml`

### REQ-FW-01 — Default deny all
Confirm `ufw` tasks set:
- `default: deny` with `direction: incoming`
- `default: deny` with `direction: outgoing`

### REQ-FW-02 — SSH with rate limiting
Confirm a `ufw` task sets `rule: limit` for the `ssh` port.

### REQ-FW-03 — Configurable inbound HTTP
Confirm a `ufw` task allows inbound TCP on `firewall_inbound_http_port`
with a `when: firewall_inbound_http_port | length > 0` guard.

### REQ-FW-04 — Configurable inbound HTTPS
Confirm a `ufw` task allows inbound TCP on `firewall_inbound_https_port`
with a `when: firewall_inbound_https_port | length > 0` guard.

### REQ-FW-05 — Configurable inbound MQTT
Confirm a `ufw` task allows inbound TCP on `firewall_inbound_mqtt_port`
with a `when: firewall_inbound_mqtt_port | length > 0` guard.

### REQ-FW-06 — Outbound DNS
Confirm `ufw` tasks allow outbound DNS (UDP and TCP port 53) looping over
`firewall_outbound_dns_ips`.

### REQ-FW-07 — Outbound HTTP for APT
Confirm a `ufw` task allows outbound HTTP looping over `config_firewall_apt_update_ips`.

### REQ-FW-08 — Outbound NTP
Confirm a `ufw` task allows outbound UDP NTP looping over `config_firewall_ntp_ips`.

### REQ-FW-09 — Outbound HTTPS for Let's Encrypt
Confirm a `ufw` task allows outbound HTTPS looping over `config_firewall_letsencrypt_ips`.

### REQ-FW-10 — Configurable outbound upstream
Confirm a `ufw` task allows outbound TCP to `firewall_outbound_upstream_ip` on
`firewall_outbound_upstream_port` with a guard for non-empty, non-loopback IP.

## Pass criteria
All checks pass with no code changes required.
Any gap must be noted and a follow-up task created.
