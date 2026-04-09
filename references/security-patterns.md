# Go Security Issue Patterns Reference

## High Risk Patterns

### 1. Command Injection

**Vulnerable Code:**
```go
cmd := exec.Command("sh", "-c", "ls "+userInput)
```

**Secure Fix:**
```go
cmd := exec.Command("ls", userInput)  // Parameterized
```

### 2. SQL Injection

**Vulnerable Code:**
```go
db.Query("SELECT * FROM users WHERE name = '"+username+"'")
```

**Secure Fix:**
```go
db.Query("SELECT * FROM users WHERE name = ?", username)
```

### 3. Hardcoded Credentials

**Vulnerable Code:**
```go
password := "secret123"
apiKey := "sk-xxx"
```

**Secure Fix:**
```go
// Use environment variables
password := os.Getenv("DB_PASSWORD")
// Or use secret management service
```

### 4. Path Traversal

**Vulnerable Code:**
```go
data, _ := ioutil.ReadFile("/data/" + filename)
```

**Secure Fix:**
```go
filename = filepath.Clean(filename)
data, err := ioutil.ReadFile(filepath.Join("/data/", filename))
```

### 5. SSRF (Server-Side Request Forgery)

**Vulnerable Code:**
```go
resp, _ := http.Get(url)  // url from user input
```

**Secure Fix:**
```go
parsedURL, _ := url.Parse(url)
if parsedURL.Hostname() != "allowed.example.com" {
    return errors.New("invalid hostname")
}
```

---

## Medium Risk Patterns

### 6. Weak Encryption

**Vulnerable Code:**
```go
hash := md5.Sum([]byte(data))
```

**Secure Fix:**
```go
hash := sha256.Sum256([]byte(data))
```

### 7. Insecure Random Numbers

**Vulnerable Code:**
```go
rand.Seed(time.Now().UnixNano())
id := rand.Int()
```

**Secure Fix:**
```go
id := strconv.FormatInt(time.Now().UnixNano(), 36) + "-"
```

### 8. Missing Timeout

**Vulnerable Code:**
```go
resp, _ := http.Get(url)
```

**Secure Fix:**
```go
client := &http.Client{Timeout: 30 * time.Second}
resp, err := client.Get(url)
```

### 9. Cookie Security

**Vulnerable Code:**
```go
http.SetCookie(w, &http.Cookie{Name: "session", Value: token})
```

**Secure Fix:**
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

## Performance Issue Patterns

### 10. N+1 Queries

**Vulnerable Code:**
```go
for _, id := range userIDs {
    user := db.QueryRow("SELECT * FROM users WHERE id = ?", id)
    users = append(users, user)
}
```

**Secure Fix:**
```go
ids := strings.Join(userIDs, ",")
rows, _ := db.Query("SELECT * FROM users WHERE id IN ("+ids+")")
```

### 11. Memory Allocation in Loop

**Vulnerable Code:**
```go
var result []string
for _, s := range strs {
    result = append(result, strings.ToUpper(s))
}
```

**Secure Fix:**
```go
result := make([]string, len(strs))
for i, s := range strs {
    result[i] = strings.ToUpper(s)
}
```

### 12. Unnecessary String Conversion

**Vulnerable Code:**
```go
s := strconv.Itoa(i)
```

**Secure Fix:**
```go
// Use strconv.FormatInt or strings.Builder
```
