# Lint Plan

## Workflow

The workflow is to work through each task one at a time with a clear context for focus. Review the proposed actions, decide whether to execute them manually or by agent, then verify the issue is resolved.

Run syntax check as a final verification before finishing.

Mark the task done in this file when verification is done to track progress. Suggest a commit message.

Then remind me to clear the context before proceeding with next task. 

Suggest the following sample prompt to trigger the workflow:
> Read plans/lint-plan.md and follow the workflow described to address the findings.

## Tasks

| Task | Rule(s) | Description | Spec | Occurrences |
|------|---------|-------------|------|-------------|
| [x] 01 | `name[play]` | Add names to all plays | [lint-01-play-names.md](../specs/lint-01-play-names.md) | 5 |
| [x] 02 | `name[missing]` `name[casing]` `name[template]` | Fix task naming issues | [lint-02-task-names.md](../specs/lint-02-task-names.md) | 14 |
| [x] 03 | `yaml[truthy]` | Replace `yes`/`no` with `true`/`false` | [lint-03-truthy-values.md](../specs/lint-03-truthy-values.md) | 134 |
| [x] 04 | `yaml[trailing-spaces]` | Remove trailing whitespace | [lint-04-trailing-spaces.md](../specs/lint-04-trailing-spaces.md) | 120 |
| [x] 05 | `yaml[new-line-at-end-of-file]` | Add missing newline at end of files | [lint-05-newline-eof.md](../specs/lint-05-newline-eof.md) | 33 |
| [ ] 06 | `yaml[indentation]` `yaml[empty-lines]` `yaml[comments]` | Fix miscellaneous YAML formatting | [lint-06-yaml-formatting.md](../specs/lint-06-yaml-formatting.md) | 16 |
| [ ] 07 | `fqcn[action-core]` | Use FQCN for builtin modules | [lint-07-fqcn-builtin.md](../specs/lint-07-fqcn-builtin.md) | 106 |
| [ ] 08 | `fqcn[action]` | Use FQCN for community modules | [lint-08-fqcn-community.md](../specs/lint-08-fqcn-community.md) | 19 |
| [ ] 09 | `risky-file-permissions` | Set explicit file permissions | [lint-09-file-permissions.md](../specs/lint-09-file-permissions.md) | 29 |
| [ ] 10 | `no-changed-when` | Add `changed_when` to command tasks | [lint-10-changed-when.md](../specs/lint-10-changed-when.md) | 5 |
| [ ] 11 | `meta-incorrect` `schema[meta]` | Fix role metadata | [lint-11-role-metadata.md](../specs/lint-11-role-metadata.md) | 32 |
| [ ] 12 | `var-naming[no-role-prefix]` | Prefix variables with role name | [lint-12-var-naming.md](../specs/lint-12-var-naming.md) | 21 |
| [ ] 13 | `jinja[spacing]` | Fix Jinja2 expression spacing | [lint-13-jinja-spacing.md](../specs/lint-13-jinja-spacing.md) | 10 |
| [ ] 14 | `no-free-form` `command-instead-of-shell` `latest[git]` | Fix miscellaneous task issues | [lint-14-misc-tasks.md](../specs/lint-14-misc-tasks.md) | 3 |
