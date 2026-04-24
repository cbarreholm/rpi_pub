
## Commands
- Syntax check: `ansible-playbook --syntax-check -i ansible/inventory.yaml ansible/<playbook>.yml`
- Dry run: `ansible-playbook --check -i ansible/inventory.yaml ansible/<playbook>.yml`
- Run playbook: `ansible-playbook -i ansible/inventory.yaml ansible/<playbook>.yml`
- Lint: `ansible-lint ansible/<playbook>.yml`
- Validate inventory: `ansible-inventory -i ansible/inventory.yaml --list`
- Encrypt secret: `ansible-vault encrypt_string --vault-password-file ansible/secrets/vault_password_file`

Available playbooks: `prepPi.yml`, `prepPiMosquitto.yml`, `prepPiZigbee2Mqtt.yml`, `prepPiHttpReverseProxy.yml`, `prepPiMiFloraServer.yml`

## Project Structure
- `specs/` – requirements (`requirements.md`) and project overview (`project.md`)
- `plans/` – implementation plans
- `design/` – design documents
- `memory/` – project memory and learned context across sessions

## Process
 - Always write tests before implementing functionality.
 - Always ask before adding dependencies.
 - Always ask before modifying existing tests.
 - Never change a test to make it pass.
 - README.md is a living artifact — update it whenever requirements or design decisions change.
 - Always verify .gitignore covers any sensitive files before committing.
