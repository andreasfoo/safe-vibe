---
name: pr-reviewer
description: 自动化代码审查技能。分析 PR 中的所有改动文件，summarize 功能正确性、安全性问题、性能问题，并检查相关函数定义。触发条件：当需要审查 Pull Request、进行代码评审、检查代码改动时使用此技能。
---

# PR 代码审查技能

## 概述

此技能用于自动化审查 PR 中的代码改动，包括：
1. 分析所有改动文件
2. 检查功能正确性
3. 识别安全问题
4. 评估性能影响
5. 验证函数定义

## 工作流程

### Step 1: 获取 PR 改动列表

使用 Git 命令获取 PR 的所有改动文件：

```bash
# 获取 PR 的改动文件列表
git diff --name-only HEAD~1 HEAD

# 或者使用 gh 命令
gh pr view <pr-number> --json files -q '.files[].path'

# 获取具体改动内容
git diff HEAD~1 HEAD -- file.go
```

### Step 2: 逐文件分析

对于每个改动文件：

1. **读取文件内容**
2. **分析改动** (使用 git diff)
3. **识别函数/方法**
4. **检查函数定义**

### Step 3: 分类检查清单

#### 功能正确性
- [ ] 语法正确性
- [ ] API 调用正确
- [ ] 错误处理
- [ ] 边界条件
- [ ] 单元测试覆盖

#### 安全问题
- [ ] SQL 注入
- [ ] 命令注入
- [ ] XSS 跨站脚本
- [ ] 路径遍历
- [ ] 硬编码凭证
- [ ] 弱加密算法
- [ ] 未验证的用户输入

#### 性能问题
- [ ] 循环中的重复计算
- [ ] 内存泄漏风险
- [ ] 数据库 N+1 查询
- [ ] 不必要的副本
- [ ] 锁竞争

### Step 4: 生成报告

将分析结果汇总成 Markdown 报告。

## 输出格式

```markdown
# PR 代码审查报告

## 概述
- PR 标题: xxx
- 改动文件数: N
- 新增代码行数: xxx
- 删除代码行数: xxx

## 文件分析

### 文件 1: path/to/file.go

#### 改动摘要
[文件的主要改动内容]

#### 功能正确性 ✓/⚠️/✗
- [结论]

#### 安全问题 ✓/⚠️/✗
- [发现的问题列表]

#### 性能问题 ✓/⚠️/✗
- [发现的问题列表]

#### 相关函数定义
| 函数名 | 行号 | 说明 |
|--------|------|------|
| FuncName | 45 | 功能描述 |

## 总体评估

| 类别 | 严重程度 |
|------|----------|
| 阻塞问题 | N |
| 建议修改 | N |
| 优化建议 | N |
```

## Go 项目特定检查

### 使用 Gosec 安全扫描

```bash
gosec -exclude=G104 ./changed/...
```

### 使用 Golangci-lint

```bash
golangci-lint run ./changed/...
```

### 编译检查

```bash
go build ./changed/...
go vet ./changed/...
```

## 常见问题模式

### 安全问题模式
| 模式 | 风险 | 推荐修复 |
|------|------|----------|
| `exec.Command(input)` | 命令注入 | 使用参数化命令 |
| `fmt.Sprintf("query %s", input)` | SQL 注入 | 使用参数化查询 |
| `http.Get(userInput)` | SSRF | 验证 URL 域名 |
| `os.Open(userInput)` | 路径遍历 | 使用 filepath.Clean |
| `crypto/md5` | 弱加密 | 使用 crypto/sha256 |

### 性能问题模式
| 模式 | 风险 | 推荐修复 |
|------|------|----------|
| `for _, v := range results { db.Query(v) }` | N+1 查询 | 批量查询 |
| `append(slice, slice2...)` | 内存复制 | 预分配容量 |
| `mutex.Lock(); longOp(); mutex.Unlock()` | 锁竞争 | 缩小锁范围 |

## 参考

- Gosec 规则: https://github.com/securego/gosec
- OWASP: https://owasp.org/www-project-web-security-testing-guide/
- Go 安全最佳实践: https://golang.org/doc/articles/security
