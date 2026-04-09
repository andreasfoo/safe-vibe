#!/usr/bin/env python3
"""
PR Code Review Script - Automatically analyze PR changes and generate report
"""

import subprocess
import sys
import json
import re
from pathlib import Path
from datetime import datetime


def run_cmd(cmd):
    """Execute shell command"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), 1


def get_changed_files(base_branch="HEAD~1", head="HEAD"):
    """Get list of changed files in PR"""
    cmd = f"git diff --name-only {base_branch} {head}"
    output, _ = run_cmd(cmd)
    if not output:
        # If no args, use staged changes
        cmd = "git diff --name-only --staged"
        output, _ = run_cmd(cmd)
    return output.split("\n") if output else []


def get_file_diff(file_path, base_branch="HEAD~1", head="HEAD"):
    """Get diff content for a single file"""
    cmd = f"git diff {base_branch} {head} -- {file_path}"
    output, _ = run_cmd(cmd)
    return output


def get_file_content(file_path):
    """Read current file content"""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except:
        return None


def extract_functions(content):
    """Extract function definitions from Go file"""
    if not content:
        return []
    
    # Match function definitions (func name, func (receiver) name)
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
    """Check for security issues"""
    issues = []
    
    # Hardcoded credentials
    if re.search(r'(password|passwd|pwd|secret|token|api_key)\s*[=:]\s*["\']', content, re.IGNORECASE):
        issues.append({
            'severity': 'HIGH',
            'type': 'Hardcoded Credentials',
            'description': 'Hardcoded password or credentials found'
        })
    
    # SQL Injection
    if re.search(r'fmt\.Sprintf.*\s*\+\s*\w+|Execute\([^)]*\+\s*', content):
        issues.append({
            'severity': 'HIGH',
            'type': 'SQL Injection Risk',
            'description': 'String concatenation in SQL queries'
        })
    
    # Command Injection
    if re.search(r'exec\.Command\([^,]*\+', content):
        issues.append({
            'severity': 'HIGH',
            'type': 'Command Injection',
            'description': 'Be careful with string concatenation in exec.Command'
        })
    
    # Path Traversal
    if re.search(r'os\.Open\([^)]*\+', content) or re.search(r'ioutil\.ReadFile\([^)]*\+', content):
        issues.append({
            'severity': 'MEDIUM',
            'type': 'Path Traversal',
            'description': 'File operations may have path traversal risk'
        })
    
    # Weak Encryption
    if re.search(r'crypto/md5|crypto/rc4|crypto/des', content):
        issues.append({
            'severity': 'HIGH',
            'type': 'Weak Encryption Algorithm',
            'description': 'Using insecure encryption algorithms'
        })
    
    return issues


def check_performance_issues(content):
    """Check for performance issues"""
    issues = []
    
    # N+1 Query Pattern
    if re.search(r'for\s+.*range.*\{\s*.*\.Query\(', content):
        issues.append({
            'severity': 'MEDIUM',
            'type': 'N+1 Query',
            'description': 'Database queries inside loop'
        })
    
    # Unreleased Resources
    if re.search(r'io\.ReadAll\([^)]*\)(?!\s*defer)', content):
        issues.append({
            'severity': 'LOW',
            'type': 'Resource Not Released',
            'description': 'Read resources not explicitly released'
        })
    
    return issues


def analyze_file(file_path, base_branch="HEAD~1", head="HEAD"):
    """Analyze a single file"""
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
    """Generate Markdown report"""
    report = []
    report.append("# PR Code Review Report\n")
    
    if pr_info:
        report.append(f"**PR Title**: {pr_info.get('title', 'N/A')}\n")
        report.append(f"**PR URL**: {pr_info.get('url', 'N/A')}\n")
    
    report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**Changed Files**: {len(results)}\n")
    
    # Statistics
    total_security = sum(len(r['security_issues']) for r in results if r)
    total_performance = sum(len(r['performance_issues']) for r in results if r)
    
    report.append(f"\n## Summary\n")
    report.append(f"| Category | Count |\n")
    report.append(f"|----------|-------|\n")
    report.append(f"| Security Issues | {total_security} |\n")
    report.append(f"| Performance Issues | {total_performance} |\n")
    
    # Detailed Analysis
    report.append("\n## File Details\n")
    
    for result in results:
        if not result:
            continue
            
        report.append(f"\n### {result['path']}\n")
        
        # Basic Info
        report.append(f"- Lines of Code: {result['line_count']}\n")
        report.append(f"- Changed Lines: {result['diff_lines']}\n")
        
        # Security Issues
        if result['security_issues']:
            report.append("\n#### Security Issues ⚠️\n")
            for issue in result['security_issues']:
                report.append(f"- **{issue['type']}** ({issue['severity']}): {issue['description']}\n")
        else:
            report.append("\n#### Security Issues ✅\n")
        
        # Performance Issues
        if result['performance_issues']:
            report.append("\n#### Performance Issues ⚠️\n")
            for issue in result['performance_issues']:
                report.append(f"- **{issue['type']}**: {issue['description']}\n")
        else:
            report.append("\n#### Performance Issues ✅\n")
        
        # Function Definitions
        if result['functions']:
            report.append("\n#### Function Definitions\n")
            report.append("| Function Name | Line Number |\n")
            report.append("|---------------|-------------|\n")
            for func in result['functions'][:10]:  # Limit to first 10
                report.append(f"| {func['name']} | {func['line']} |\n")
    
    return "\n".join(report)


def main():
    """Main function"""
    print("Fetching PR changed files...")
    
    files = get_changed_files()
    if not files:
        print("No changed files found")
        return
    
    print(f"Found {len(files)} changed files\n")
    
    results = []
    for file_path in files:
        if not file_path:
            continue
        
        print(f"Analyzing: {file_path}")
        result = analyze_file(file_path)
        if result:
            results.append(result)
    
    # Generate Report
    report = generate_report(results)
    print("\n" + "="*50)
    print(report)
    
    # Save Report
    report_file = "pr_review_report.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved to: {report_file}")


if __name__ == "__main__":
    main()
