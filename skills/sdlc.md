# /sdlc

Software Development Lifecycle management.

## Usage

```bash
/sdlc [command] [args]
```

## Quick Start

```bash
# Most common: run individual phases
/sdlc test
/sdlc verify
/sdlc commit
/sdlc pr

# Or use a workflow
/sdlc start quick "Hotfix login bug"
/sdlc next
```

## Key Principle

**Each phase works independently.** No workflow required.

## Available Commands

| Command | Description |
|---------|-------------|
| `/sdlc start <type> [description]` | Start a workflow |
| `/sdlc status` | Show status |
| `/sdlc next` | Next phase |
| `/sdlc skip [phase]` | Skip current phase |
| `/sdlc phase <name>` | Jump to phase |
| `/sdlc end` | End workflow |
| `/archive [scope] [pattern]` | Archive old docs |

### Workflow Types

| Type | Description | Workflow |
|------|-------------|----------|
| `quick` | Small changes | **coding → test → commit → pr** |
| `feature` | New features | understand → research → spec → coding → test → verify → commit → pr |
| `bugfix` | Bug fixes | understand → debug → coding → test → verify → commit → pr |
| `research` | Research | understand → research → doc → END |

### Phase Commands

```bash
/sdlc coding [desc]    # Write code
/sdlc test [type]      # Run tests (lint + unit + e2e)
/sdlc verify [spec]    # Check vs spec
/sdlc commit [msg]     # Commit changes
/sdlc pr [action]      # Create/manage PR
/sdlc understand       # Build context
/sdlc research [topic] # Research solutions
/sdlc spec [name]      # Write spec
/sdlc debug [issue]    # Debug bugs
```

## Workflows

```
QUICK:    coding → test → commit → pr
FEATURE:  understand → research → spec → coding → test → verify → commit → pr
BUGFIX:   understand → debug → coding → test → verify → commit → pr
RESEARCH: understand → research → doc → END
```

## Examples

```bash
# Quick fix - fastest path
/sdlc start quick "Fix typo"
/sdlc next  # goes: coding → test → commit → pr

# Individual phases
/sdlc test lint
/sdlc verify spec/auth.md
/sdlc commit "fix: login bug"

# Jump around
/sdlc phase commit
/sdlc skip verify
```

## State Tracking (Optional)

State stored in `.sdlc/state.json`. Use `/sdlc start` to enable.

```bash
/sdlc status    # Show progress
/sdlc next      # Next phase
/sdlc skip      # Skip current
/sdlc phase X   # Jump to phase
/sdlc end       # End workflow
```

## Quality Checks

| Phase | Checks |
|-------|--------|
| `test` | Lint, typecheck, unit, e2e |
| `verify` | Spec compliance |
| `debug` | Bug analysis |

## Natural Language

```bash
/sdlc start 修复登录bug  # Detects: bugfix
/sdlc start add user api  # Detects: feature
```

## Output Locations

```
docs/
├── spec/       # Specs
├── research/   # Research docs
├── verify/     # Verification reports
└── archive/ # Archived docs

.sdlc/state.json  # Workflow state
```

## Output Format

```
═══ SDLC Status ═══

Workflow: quick
Phase:    coding
Next:     test

Branch: quick/fix-typo
─────────────────────
/sdlc next to continue
```

## Best Practices

1. Use phases independently when you know what you need
2. Use workflows for tracking multi-step tasks
3. Skip freely - you know what you're doing
4. `/sdlc verify` ensures implementation matches spec

## Migration

The SDLC system now includes unified commands that work both standalone and within workflows.

| Old Command | New Command | Notes |
|-------------|-------------|-------|
| `/spec` | `/sdlc spec` | Specification writing |
| `/pr` | `/pr` or `/sdlc pr` | **Standalone available** - no workflow required |
| `/git-commit` | `/commit` or `/sdlc commit` | **Standalone available** - no workflow required |
| `/codereview` | `/sdlc cr` | Code review |

### Key Changes

**`/commit` and `/pr` are now standalone:**
- Use `/commit` or `/pr` anytime without starting an SDLC workflow
- When used in SDLC workflow (`/sdlc commit`, `/sdlc pr`), they include additional checks and state updates
- Single source of truth in `skills/phases/commit.md` and `skills/phases/pr.md`

**Example:**
```bash
# Standalone use (no workflow)
/commit "feat: add user auth"
/pr

# SDLC workflow use (with checks)
/sdlc start quick "Add auth"
/sdlc commit  # Runs pre-commit checks first
/sdlc pr      # Includes review requirements
```
