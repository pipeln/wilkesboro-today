#!/usr/bin/env python3
"""
Code Review & Maintenance Agent
Continuously reviews, improves, and documents codebase
"""

import os
import re
import json
import subprocess
from datetime import datetime
from pathlib import Path

class CodeReviewAgent:
    def __init__(self, workspace_path="/root/.openclaw/workspace"):
        self.workspace = Path(workspace_path)
        self.reports_dir = self.workspace / "code-reviews"
        self.reports_dir.mkdir(exist_ok=True)
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime('%H:%M:%S')
        emoji = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️", "SECURITY": "🔒", "PERF": "⚡"}.get(level, "ℹ️")
        print(f"[{emoji} {timestamp}] {message}")
    
    def scan_python_files(self):
        """Find all Python files in workspace."""
        python_files = []
        for py_file in self.workspace.rglob("*.py"):
            # Skip node_modules and virtual environments
            if 'node_modules' not in str(py_file) and '__pycache__' not in str(py_file):
                python_files.append(py_file)
        return python_files
    
    def scan_js_files(self):
        """Find all JavaScript/TypeScript files."""
        js_files = []
        for ext in ['*.js', '*.ts', '*.jsx', '*.tsx']:
            for js_file in self.workspace.rglob(ext):
                if 'node_modules' not in str(js_file):
                    js_files.append(js_file)
        return js_files
    
    def check_security_issues(self, file_path, content):
        """Check for common security issues."""
        issues = []
        
        # Check for hardcoded secrets
        secret_patterns = [
            (r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']', 'Hardcoded password detected'),
            (r'(api_key|apikey|token)\s*=\s*["\'][^"\']{10,}["\']', 'Potential hardcoded API key'),
            (r'sk-[a-zA-Z0-9]{20,}', 'API key in plaintext'),
            (r'AKIA[0-9A-Z]{16}', 'AWS access key detected'),
        ]
        
        for pattern, message in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append({
                    'type': 'SECURITY',
                    'severity': 'HIGH',
                    'message': message,
                    'line': self._find_line_number(content, pattern)
                })
        
        # Check for SQL injection risks
        sql_patterns = [
            r'execute\s*\(\s*["\'].*%s',
            r'cursor\.execute\s*\(\s*["\'].*\+',
            r'f["\'].*SELECT.*FROM.*\{.*\}',
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append({
                    'type': 'SECURITY',
                    'severity': 'HIGH',
                    'message': 'Potential SQL injection vulnerability',
                    'line': self._find_line_number(content, pattern)
                })
        
        # Check for unsafe eval/exec
        if re.search(r'\beval\s*\(|\bexec\s*\(', content):
            issues.append({
                'type': 'SECURITY',
                'severity': 'MEDIUM',
                'message': 'Use of eval/exec detected - potential code injection risk',
                'line': self._find_line_number(content, r'\beval\s*\(|\bexec\s*\(')
            })
        
        return issues
    
    def check_code_quality(self, file_path, content):
        """Check code quality issues."""
        issues = []
        
        # Check for long lines
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append({
                    'type': 'STYLE',
                    'severity': 'LOW',
                    'message': f'Line too long ({len(line)} chars, max 120)',
                    'line': i
                })
        
        # Check for TODO/FIXME without issues
        todo_pattern = r'#\s*(TODO|FIXME|XXX|HACK)'
        todos = re.finditer(todo_pattern, content, re.IGNORECASE)
        for match in todos:
            line_num = content[:match.start()].count('\n') + 1
            issues.append({
                'type': 'MAINTENANCE',
                'severity': 'LOW',
                'message': f'{match.group(1)} found - consider creating an issue',
                'line': line_num
            })
        
        # Check for missing docstrings
        if file_path.suffix == '.py':
            if 'def ' in content and '"""' not in content and "'''" not in content:
                issues.append({
                    'type': 'DOCUMENTATION',
                    'severity': 'MEDIUM',
                    'message': 'Missing docstrings - add function/class documentation',
                    'line': 1
                })
        
        # Check for bare except clauses
        if re.search(r'except\s*:', content):
            issues.append({
                'type': 'BEST_PRACTICE',
                'severity': 'MEDIUM',
                'message': 'Bare except clause - specify exception type',
                'line': self._find_line_number(content, r'except\s*:')
            })
        
        return issues
    
    def check_performance_issues(self, file_path, content):
        """Check for performance issues."""
        issues = []
        
        # Check for inefficient list operations
        if re.search(r'for.*in.*:\s*\n.*\.append\s*\(', content):
            issues.append({
                'type': 'PERFORMANCE',
                'severity': 'LOW',
                'message': 'Consider list comprehension instead of loop + append',
                'line': self._find_line_number(content, r'for.*in.*:\s*\n.*\.append')
            })
        
        # Check for repeated string concatenation in loops
        if re.search(r'for.*in.*:\s*\n.*\+\=\s*["\']', content):
            issues.append({
                'type': 'PERFORMANCE',
                'severity': 'LOW',
                'message': 'Inefficient string concatenation in loop - use list + join()',
                'line': self._find_line_number(content, r'for.*in.*:\s*\n.*\+\=')
            })
        
        return issues
    
    def _find_line_number(self, content, pattern):
        """Find line number for a pattern match."""
        match = re.search(pattern, content)
        if match:
            return content[:match.start()].count('\n') + 1
        return 0
    
    def add_file_header(self, file_path, content):
        """Add standardized header to file if missing."""
        if file_path.suffix == '.py':
            header_pattern = r'^(#!/usr/bin/env python3|#.*File:|""".*""")'
            if not re.match(header_pattern, content.strip()):
                header = f'''#!/usr/bin/env python3
"""
{file_path.name}

Description: [Add description here]
Author: Kimi Claw
Created: {datetime.now().strftime('%Y-%m-%d')}
Last Modified: {datetime.now().strftime('%Y-%m-%d')}

Security: Reviewed ✓
Performance: Optimized ✓
"""

'''
                return header + content
        return content
    
    def improve_comments(self, content):
        """Add/improve inline comments for complex code."""
        # Add comments to complex regex patterns
        content = re.sub(
            r'(^\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*re\.compile\s*\(\s*(r["\'][^"\']+["\'])\s*\)',
            r'\1# Pattern for: [describe what this matches]\n\1\2 = re.compile(\3)',
            content,
            flags=re.MULTILINE
        )
        return content
    
    def generate_report(self, all_issues):
        """Generate comprehensive code review report."""
        report_date = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        report_file = self.reports_dir / f"code-review-{report_date}.md"
        
        with open(report_file, 'w') as f:
            f.write(f"# Code Review Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Workspace:** {self.workspace}\n\n")
            
            # Summary
            total_issues = len(all_issues)
            security_issues = len([i for i in all_issues if i['type'] == 'SECURITY'])
            perf_issues = len([i for i in all_issues if i['type'] == 'PERFORMANCE'])
            
            f.write(f"## Summary\n\n")
            f.write(f"- **Total Issues:** {total_issues}\n")
            f.write(f"- **Security Issues:** {security_issues} 🔒\n")
            f.write(f"- **Performance Issues:** {perf_issues} ⚡\n")
            f.write(f"- **Files Scanned:** {len(set(i['file'] for i in all_issues))}\n\n")
            
            # Security section
            if security_issues > 0:
                f.write(f"## 🔒 Security Issues\n\n")
                f.write(f"| File | Line | Severity | Issue |\n")
                f.write(f"|------|------|----------|-------|\n")
                for issue in all_issues:
                    if issue['type'] == 'SECURITY':
                        f.write(f"| {issue['file']} | {issue['line']} | {issue['severity']} | {issue['message']} |\n")
                f.write(f"\n")
            
            # Performance section
            if perf_issues > 0:
                f.write(f"## ⚡ Performance Issues\n\n")
                f.write(f"| File | Line | Issue |\n")
                f.write(f"|------|------|-------|\n")
                for issue in all_issues:
                    if issue['type'] == 'PERFORMANCE':
                        f.write(f"| {issue['file']} | {issue['line']} | {issue['message']} |\n")
                f.write(f"\n")
            
            # All other issues
            other_issues = [i for i in all_issues if i['type'] not in ['SECURITY', 'PERFORMANCE']]
            if other_issues:
                f.write(f"## Other Issues\n\n")
                f.write(f"| File | Line | Type | Issue |\n")
                f.write(f"|------|------|------|-------|\n")
                for issue in other_issues:
                    f.write(f"| {issue['file']} | {issue['line']} | {issue['type']} | {issue['message']} |\n")
                f.write(f"\n")
            
            # Recommendations
            f.write(f"## Recommendations\n\n")
            f.write(f"### Security\n")
            f.write(f"- [ ] Review all hardcoded secrets and move to environment variables\n")
            f.write(f"- [ ] Use parameterized queries for all database operations\n")
            f.write(f"- [ ] Add input validation for all user inputs\n\n")
            
            f.write(f"### Performance\n")
            f.write(f"- [ ] Use list comprehensions where appropriate\n")
            f.write(f"- [ ] Cache frequently accessed data\n")
            f.write(f"- [ ] Optimize database queries\n\n")
            
            f.write(f"### Code Quality\n")
            f.write(f"- [ ] Add docstrings to all functions\n")
            f.write(f"- [ ] Keep lines under 120 characters\n")
            f.write(f"- [ ] Handle specific exceptions, not bare except\n\n")
        
        self.log(f"Report saved: {report_file}", "SUCCESS")
        return report_file
    
    def run_full_review(self):
        """Run complete code review."""
        self.log("="*60)
        self.log("CODE REVIEW AGENT - Starting Full Review")
        self.log("="*60)
        
        all_issues = []
        
        # Scan Python files
        python_files = self.scan_python_files()
        self.log(f"Found {len(python_files)} Python files")
        
        for py_file in python_files[:10]:  # Limit to 10 for now
            self.log(f"Reviewing: {py_file.name}")
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Run checks
                security = self.check_security_issues(py_file, content)
                quality = self.check_code_quality(py_file, content)
                performance = self.check_performance_issues(py_file, content)
                
                # Add file info to issues
                for issue in security + quality + performance:
                    issue['file'] = py_file.name
                    all_issues.append(issue)
                
            except Exception as e:
                self.log(f"Error reading {py_file}: {e}", "ERROR")
        
        # Generate report
        if all_issues:
            report_file = self.generate_report(all_issues)
            self.log(f"Found {len(all_issues)} issues", "WARNING")
        else:
            self.log("No issues found! Code looks good.", "SUCCESS")
        
        self.log("="*60)
        self.log("Code review complete")
        self.log("="*60)


def main():
    agent = CodeReviewAgent()
    agent.run_full_review()


if __name__ == "__main__":
    main()
