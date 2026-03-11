# /pr

/pr creates and manages pull requests with proper title, description, and review process. Works standalone or within SDLC workflows.

**Purpose**: Create and manage pull requests for code integration

## Usage

```
/pr [base-branch]
```

**Arguments:**
- `base-branch` (optional): The base branch to compare against (default: `main`)

**Actions:**
- No argument: Create a new PR
- `status` - Check PR status
- `merge` - Merge PR (when ready)

**Examples:**
- `/pr` - Create a new pull request against main
- `/pr develop` - Create PR against develop branch
- `/pr status` - Check current PR status
- `/pr merge` - Merge the PR when approved

**Standalone Use:**
```bash
# Use anytime without SDLC workflow
/pr
/pr develop
```

**SDLC Workflow Use:**
```bash
# Part of SDLC workflow - includes review requirements
/sdlc pr
/sdlc pr status
/sdlc pr merge
```

## Commit Style Pattern

The project uses conventional commits with lowercase prefixes:

- `bugfix:` - Bug fixes
- `feat:` - New features
- `command:` - Command-related changes
- `chore:` - Chores/maintenance
- `mv:` - File/directory moves
- `doc:` - Documentation changes
- `perf:` - Performance improvements

## PR Generation Process

### 1. Fetch and Update Remote Base Branch

```bash
git fetch origin <base-branch>  # default: origin/main
```

Ensures PR diff is accurate against latest remote code.

### 2. Get Commit History and Full Diff Together

```bash
git log <base-branch>..HEAD --oneline    # Commit history - intent
git diff <base-branch>..HEAD             # Full diff - reality
git diff <base-branch>..HEAD --stat      # Changed files summary
```

**Why both?** Commit messages tell *why* changes were made, diff shows *what* actually changed. Read together as a unified view.

### 3. Write PR Title

- Follow commit message style: `[prefix]: [brief description]`
- Use lowercase, keep under 72 characters
- If multiple commit types, use dominant one or `feat:`

### 4. Write PR Description

- Start with brief summary (1-2 sentences)
- Categorize into **Major** (core functionality, significant features) and **Minor** (small improvements, docs)
- Use `-` for bullet points, keep concise
- Optionally include commit title in parentheses

### 5. Test Plan (Optional)

- Add checklist with `- [ ]` for unchecked items
- Focus on critical paths and edge cases

## PR Output Format

```markdown
## Summary
[1-2 sentence summary of what this PR does and why]

### Major: *(optional title)*
- [Change description]
- [Change description]

### Minor: *(optional title)*
- [Change description]

## Test Plan
- [ ] [Test case 1]
- [ ] [Test case 2]
```

## PR Examples

**Input commits:**
```
feat: add user authentication
feat: add login form with validation
bugfix: fix token validation edge cases
chore: update dependencies
```

**Output PR:**
```
feat: add user authentication

## Summary
Add complete user authentication flow with JWT token management.

### Major: Authentication
- Add login form component with validation *(feat: add login form with validation)*
- Implement JWT token generation and validation
- Fix token validation edge cases *(bugfix: fix token validation)*

### Minor: Cleanup
- Update dependencies to latest versions
```

## Create PR

Using GitHub CLI:
```bash
gh pr create --title "feat(auth): add JWT authentication" --body "..."
```

## Merge PR

```bash
gh pr merge --merge --delete-branch
```

## SDLC Mode Features

When used in SDLC workflow (`/sdlc pr`):

### Enhanced PR Status Check

```
━━━ Pull Request Status ━━━

PR: #45 - feat(auth): add JWT authentication
Branch: feature/user-auth → main
Status: Ready for review

━━━ Checks ━━━
✓ CI/CD Pipeline: Passing
  - Lint: ✓
  - Type Check: ✓
  - Unit Tests: ✓ (45/45)
  - Integration Tests: ✓ (12/12)
  - E2E Tests: ✓ (8/8)

✓ Code Coverage: 87% (target: 80%)
✓ Security Scan: No vulnerabilities

━━━ Review Status ━━━
Required reviewers: 2
✓ @alice - Approved
✓ @bob - Approved

━━━ Action ━━━
Ready to merge! Use `/sdlc pr merge` to complete.
```

### Merge Requirements (SDLC Mode)

**Required:**
- All CI/CD checks passing
- Code coverage threshold met
- Security scan clean
- Minimum approvals received
- No merge conflicts

### Enhanced Description Template (SDLC Mode)

```markdown
## Overview
[Brief description]

## Changes
- [Change 1]
- [Change 2]

## Type of Change
- [ ] Bug fix / New feature / Breaking change / Refactor / Documentation

## Testing
- [ ] Unit / Integration / E2E tests added
- [ ] All tests passing

## Documentation
- [ ] Spec linked
- [ ] API docs updated
- [ ] README updated (if needed)

## Related
- Spec: `docs/spec/YYYYMMDD-title.md`
- Test Report: `docs/test/YYYYMMDD-title-test-report.md`
- Verification: `docs/verify/YYYYMMDD-title-verification.md`
```

## Best Practices

### PR Hygiene
- **Keep PRs focused**: One feature or fix per PR
- **Keep PRs small**: Easier to review and merge
- **Use draft PRs**: For work in progress
- **Reference issues**: Link to related issue numbers

### Tips
- **Always fetch remote base branch first** - Ensures accurate diff
- **Read commits and diff together** - Unified view prevents fragmentation
- Group related commits logically
- If many unrelated commits, suggest splitting
- Use file paths from `git diff --stat` to be specific

## Completion Conditions

### For PR Creation
- [ ] PR title follows format
- [ ] PR description complete with template
- [ ] All related documents linked (SDLC only)
- [ ] PR created successfully

### For PR Merge
- [ ] All required approvals received (SDLC only)
- [ ] All checks passing (SDLC only)
- [ ] No merge conflicts
- [ ] PR merged successfully
- [ ] Branch deleted (if applicable)
- [ ] PR logged to documentation (SDLC only)

## State Integration

- **Updates**: `sdlc.phase` = `pr`
- **Creates**: Pull request
- **Creates**: PR log in `docs/pr/` (SDLC only)
- **Requires**: `commit` phase completed (SDLC only)
- **Next**: After merge, workflow complete (SDLC only)

## Related Skills

- `/commit` - Prerequisite: commits must exist to create PR
- `/git` - Low-level git operations (branch, checkout, merge)
- `/sdlc cr` - (SDLC only) Code review that happens before PR review
- `/sdlc test` - (SDLC only) Tests that must pass for PR checks
