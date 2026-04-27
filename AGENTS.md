
## Commands
- Syntax check: `ansible-playbook --syntax-check -i ansible/inventory.yaml -e @ansible/secrets/secrets_file.enc --vault-password-file ansible/secrets/vault_password_file ansible/<playbook>.yml`
- Dry run: `ansible-playbook --check -i ansible/inventory.yaml -e @ansible/secrets/secrets_file.enc --vault-password-file ansible/secrets/vault_password_file ansible/<playbook>.yml`
- Run playbook: `ansible-playbook -i ansible/inventory.yaml -e @ansible/secrets/secrets_file.enc --vault-password-file ansible/secrets/vault_password_file ansible/<playbook>.yml`
- Lint: `ansible-lint ansible/<playbook>.yml`
- Validate inventory: `ansible-inventory -i ansible/inventory.yaml --list`
- Encrypt secret: `ansible-vault encrypt_string --vault-password-file ansible/secrets/vault_password_file`

Available playbooks: `prepPiServer.yml`, `prepMosquitto.yml`, `prepZigbee2Mqtt.yml`, `prepHttpReverseProxy.yml`, `prepMiFloraServer.yml`

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
 - Run tasks in plans sequentially, tracking progress in task table in the applicable plan file. Instructing user to clear context inbetween tasks for focus. 


## Workflow definitions

### Implementation Workflow (per session)
Alias used in prompt: "Implement now"
1. Read specs/project.md → plans/implementation-plan.md → pick next task → read its spec
2. Read memory/learnings.md if it exists
3. Write tests first, then implement, then verify
4. Lint
5. Mark task done in plans/implementation-plan.md
6. Update memory/learnings.md with anything future tasks need
7. Suggest commit message and as user to commit
8. Stop after one task