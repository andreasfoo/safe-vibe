---
name: pr-reviewer
description: Automated Pull Request code review skill. Analyzes all changed files in a PR, summarizes functionality correctness, security issues, and performance concerns. Also checks related function definitions. Trigger: when reviewing Pull Requests, conducting code reviews, or checking code changes.
---

# PR Code Review Skill

## Overview

This skill automatically reviews PR code changes including:
1. Analyze all changed files
2. Check functionality correctness
3. Identify security issues
4. Evaluate performance impact
5. Verify function definitions

## Workflow

### Step 1: Get PR Changed Files

Use Git commands to get all changed files in the PR:

```bash
# Get list of changed files
git diff --name-only HEAD~1 HEAD

# Or use gh command
gh pr view <pr-number> --json files -q '.files[].path'

# Get specific diff
git diff HEAD~1 HEAD -- file.go
```

### Step 2: Analyze Files One by One

For each changed file:

1. **Read file content**
2. **Analyze changes** (using git diff)
3. **Identify functions/methods**
4. **Check function definitions**

### Step 3: Checklist Analysis

#### Functionality Correctness
- [ ] Syntax correctness
- [ ] API calls are correct
- [ ] Error handling
- [ ] Boundary conditions
- [ ] Unit test coverage

#### Security Issues
- [ ] SQL injection
- [ ] Command injection
- [ ] XSS (Cross-Site Scripting)
- [ ] Path traversal
- [ ] Hardcoded credentials
- [ ] Weak encryption algorithms
- [ ] Unvalidated user input

#### Performance Issues
- [ ] Repeated calculations in loops
- [ ] Memory leak risks
- [ ] Database N+1 queries
- [ ] Unnecessary copies
- [ ] Lock contention

### Step 4: Generate Report

Compile analysis results into a Markdown report.

## Output Format

```markdown
# PR Code Review Report

## Overview
- PR Title: xxx
- Changed Files: N
- Lines Added: xxx
- Lines Deleted: xxx

## File Analysis

### File 1: path/to/file.go

#### Change Summary
[Main changes in the file]

#### Functionality Correctness ✓/⚠️/✗
- [conclusion]

#### Security Issues ✓/⚠️/✗
- [list of issues found]

#### Performance Issues ✓/⚠️/✗
- [list of issues found]

#### Related Function Definitions
| Function Name | Line | Description |
|---------------|------|--------------|
| FuncName | 45 | Function description |

## Overall Assessment

| Category | Count |
|----------|-------|
| Blocking Issues | N |
| Suggested Changes | N |
| Optimization Suggestions | N |
```

## Go Project Specific Checks

### Use Gosec for Security Scanning

```bash
gosec -exclude=G104 ./changed/...
```

### Use Golangci-lint

```bash
golangci-lint run ./changed/...
```

### Compilation Checks

```bash
go build ./changed/...
go vet ./changed/...
```

## Common Issue Patterns

### Security Issue Patterns
| Pattern | Risk | Recommended Fix |
|---------|------|----------------|
| `exec.Command(input)` | Command Injection | Use parameterized commands |
| `fmt.Sprintf("query %s", input)` | SQL Injection | Use parameterized queries |
| `http.Get(userInput)` | SSRF | Validate URL domain |
| `os.Open(userInput)` | Path Traversal | Use filepath.Clean |
| `crypto/md5` | Weak Encryption | Use crypto/sha256 |

### Performance Issue Patterns
| Pattern | Risk | Recommended Fix |
|---------|------|----------------|
| `for _, v := range results { db.Query(v) }` | N+1 Queries | Batch queries |
| `append(slice, slice2...)` | Memory Copy | Pre-allocate capacity |
| `mutex.Lock(); longOp(); mutex.Unlock()` | Lock Contention | Reduce lock scope |

## References

- Gosec Rules: https://github.com/securego/gosec
- OWASP: https://owasp.org/www-project-web-security-testing-guide/
- Go Security Best Practices: https://golang.org/doc/articles/security
