# Go 安全问题模式参考

## 高风险模式

### 1. 命令注入

**危险代码:**
```go
cmd := exec.Command("sh", "-c", "ls "+userInput)
```

**安全修复:**
```go
cmd := exec.Command("ls", userInput)  // 参数化
```

### 2. SQL 注入

**危险代码:**
```go
db.Query("SELECT * FROM users WHERE name = '"+username+"'")
```

**安全修复:**
```go
db.Query("SELECT * FROM users WHERE name = ?", username)
```

### 3. 硬编码凭证

**危险代码:**
```go
password := "secret123"
apiKey := "sk-xxx"
```

**安全修复:**
```go
// 使用环境变量
password := os.Getenv("DB_PASSWORD")
// 或使用密钥管理服务
```

### 4. 路径遍历

**危险代码:**
```go
data, _ := ioutil.ReadFile("/data/" + filename)
```

**安全修复:**
```go
filename = filepath.Clean(filename)
data, err := ioutil.ReadFile(filepath.Join("/data/", filename))
```

### 5. SSRF (服务器端请求伪造)

**危险代码:**
```go
resp, _ := http.Get(url)  // url from user input
```

**安全修复:**
```go
parsedURL, _ := url.Parse(url)
if parsedURL.Hostname() != "allowed.example.com" {
    return errors.New("invalid hostname")
}
```

---

## 中等风险模式

### 6. 弱加密

**危险代码:**
```go
hash := md5.Sum([]byte(data))
```

**安全修复:**
```go
hash := sha256.Sum256([]byte(data))
```

### 7. 不安全的随机数

**危险代码:**
```go
rand.Seed(time.Now().UnixNano())
id := rand.Int()
```

**安全修复:**
```go
id := strconv.FormatInt(time.Now().UnixNano(), 36) + "-"
```

### 8. 缺少超时

**危险代码:**
```go
resp, _ := http.Get(url)
```

**安全修复:**
```go
client := &http.Client{Timeout: 30 * time.Second}
resp, err := client.Get(url)
```

### 9. Cookie 安全

**危险代码:**
```go
http.SetCookie(w, &http.Cookie{Name: "session", Value: token})
```

**安全修复:**
```go
http.SetCookie(w, &http.Cookie{
    Name:     "session",
    Value:    token,
    Secure:   true,
    HttpOnly: true,
    SameSite: http.SameSiteStrictMode,
})
```

---

## 性能问题模式

### 10. N+1 查询

**危险代码:**
```go
for _, id := range userIDs {
    user := db.QueryRow("SELECT * FROM users WHERE id = ?", id)
    users = append(users, user)
}
```

**安全修复:**
```go
ids := strings.Join(userIDs, ",")
rows, _ := db.Query("SELECT * FROM users WHERE id IN ("+ids+")")
```

### 11. 循环中分配内存

**危险代码:**
```go
var result []string
for _, s := range strs {
    result = append(result, strings.ToUpper(s))
}
```

**安全修复:**
```go
result := make([]string, len(strs))
for i, s := range strs {
    result[i] = strings.ToUpper(s)
}
```

### 12. 不必要的字符串转换

**危险代码:**
```go
s := strconv.Itoa(i)
```

**安全修复:**
```go
// 使用 strconv.FormatInt 或 strings.Builder
```
