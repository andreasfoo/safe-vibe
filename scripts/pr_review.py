#!/usr/bin/env python3
"""
PR 代码审查脚本 - 自动分析 PR 改动并生成报告
"""

import subprocess
import sys
import json
import re
from pathlib import Path
from datetime import datetime


def run_cmd(cmd):
    """执行 shell 命令"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), 1


def get_changed_files(base_branch="HEAD~1", head="HEAD"):
    """获取 PR 改动的文件列表"""
    cmd = f"git diff --name-only {base_branch} {head}"
    output, _ = run_cmd(cmd)
    if not output:
        # 如果没有参数，使用 staged 改动
        cmd = "git diff --name-only --staged"
        output, _ = run_cmd(cmd)
    return output.split("\n") if output else []


def get_file_diff(file_path, base_branch="HEAD~1", head="HEAD"):
    """获取单个文件的改动内容"""
    cmd = f"git diff {base_branch} {head} -- {file_path}"
    output, _ = run_cmd(cmd)
    return output


def get_file_content(file_path):
    """读取文件当前内容"""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except:
        return None


def extract_functions(content):
    """提取 Go 文件中的函数定义"""
    if not content:
        return []
    
    # 匹配函数定义 (func name, func (receiver) name)
    patterns = [
        r'func\s+(\w+)\s*\(',
        r'func\s+\((\w+)\s+\*?\w+)\s+(\w+)\s*\(',
    ]
    
    functions = []
    for pattern in patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            functions.append({
                'name': match.group(0).replace('func ', '').replace('(', ''),
                'line': line_num
            })
    
    return functions


def check_security_issues(content):
    """检查安全问题"""
    issues = []
    
    # 硬编码凭证
    if re.search(r'(password|passwd|pwd|secret|token|api_key)\s*[=:]\s*["\']', content, re.IGNORECASE):
        issues.append({
            'severity': 'HIGH',
            'type': '硬编码凭证',
            'description': '发现硬编码的密码或凭证'
        })
    
    # SQL 注入
    if re.search(r'fmt\.Sprintf.*\s*\+\s*\w+|Execute\([^)]*\+\s*', content):
        issues.append({
            'severity': 'HIGH',
            'type': 'SQL 注入风险',
            'description': 'SQL 查询中使用字符串拼接'
        })
    
    # 命令注入
    if re.search(r'exec\.Command\([^,]*\+', content):
        issues.append({
            'severity': 'HIGH',
            'type': '命令注入',
            'description': '使用 exec.Command 时小心字符串拼接'
        })
    
    # 路径遍历
    if re.search(r'os\.Open\([^)]*\+', content) or re.search(r'ioutil\.ReadFile\([^)]*\+', content):
        issues.append({
            'severity': 'MEDIUM',
            'type': '路径遍历',
            'description': '文件操作可能存在路径遍历风险'
        })
    
    # 弱加密
    if re.search(r'crypto/md5|crypto/rc4|crypto/des', content):
        issues.append({
            'severity': 'HIGH',
            'type': '弱加密算法',
            'description': '使用不安全的加密算法'
        })
    
    return issues


def check_performance_issues(content):
    """检查性能问题"""
    issues = []
    
    # N+1 查询模式
    if re.search(r'for\s+.*range.*\{\s*.*\.Query\(', content):
        issues.append({
            'severity': 'MEDIUM',
            'type': 'N+1 查询',
            'description': '循环中执行数据库查询'
        })
    
    # 未释放资源
    if re.search(r'io\.ReadAll\([^)]*\)(?!\s*defer)', content):
        issues.append({
            'severity': 'LOW',
            'type': '资源未释放',
            'description': '读取的资源未显式释放'
        })
    
    return issues


def analyze_file(file_path, base_branch="HEAD~1", head="HEAD"):
    """分析单个文件"""
    content = get_file_content(file_path)
    diff = get_file_diff(file_path, base_branch, head)
    
    if not content and not diff:
        return None
    
    result = {
        'path': file_path,
        'functions': extract_functions(content) if content else [],
        'security_issues': check_security_issues(content) if content else [],
        'performance_issues': check_performance_issues(content) if content else [],
        'line_count': len(content.split('\n')) if content else 0,
        'diff_lines': len(diff.split('\n')) if diff else 0
    }
    
    return result


def generate_report(results, pr_info=None):
    """生成 Markdown 报告"""
    report = []
    report.append("# PR 代码审查报告\n")
    
    if pr_info:
        report.append(f"**PR 标题**: {pr_info.get('title', 'N/A')}\n")
        report.append(f"**PR 链接**: {pr_info.get('url', 'N/A')}\n")
    
    report.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**改动文件数**: {len(results)}\n")
    
    # 统计
    total_security = sum(len(r['security_issues']) for r in results if r)
    total_performance = sum(len(r['performance_issues']) for r in results if r)
    
    report.append(f"\n## 统计概览\n")
    report.append(f"| 类别 | 数量 |\n")
    report.append(f"|------|------|\n")
    report.append(f"| 安全问题 | {total_security} |\n")
    report.append(f"| 性能问题 | {total_performance} |\n")
    
    # 详细分析
    report.append("\n## 文件详细分析\n")
    
    for result in results:
        if not result:
            continue
            
        report.append(f"\n### {result['path']}\n")
        
        # 基本信息
        report.append(f"- 代码行数: {result['line_count']}\n")
        report.append(f"- 改动行数: {result['diff_lines']}\n")
        
        # 安全问题
        if result['security_issues']:
            report.append("\n#### 安全问题 ⚠️\n")
            for issue in result['security_issues']:
                report.append(f"- **{issue['type']}** ({issue['severity']}): {issue['description']}\n")
        else:
            report.append("\n#### 安全问题 ✅\n")
        
        # 性能问题
        if result['performance_issues']:
            report.append("\n#### 性能问题 ⚠️\n")
            for issue in result['performance_issues']:
                report.append(f"- **{issue['type']}**: {issue['description']}\n")
        else:
            report.append("\n#### 性能问题 ✅\n")
        
        # 函数定义
        if result['functions']:
            report.append("\n#### 函数定义\n")
            report.append("| 函数名 | 行号 |\n")
            report.append("|--------|------|\n")
            for func in result['functions'][:10]:  # 限制显示前10个
                report.append(f"| {func['name']} | {func['line']} |\n")
    
    return "\n".join(report)


def main():
    """主函数"""
    print("正在获取 PR 改动文件...")
    
    files = get_changed_files()
    if not files:
        print("未发现改动文件")
        return
    
    print(f"发现 {len(files)} 个改动文件\n")
    
    results = []
    for file_path in files:
        if not file_path:
            continue
        
        print(f"分析: {file_path}")
        result = analyze_file(file_path)
        if result:
            results.append(result)
    
    # 生成报告
    report = generate_report(results)
    print("\n" + "="*50)
    print(report)
    
    # 保存报告
    report_file = "pr_review_report.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n报告已保存到: {report_file}")


if __name__ == "__main__":
    main()
