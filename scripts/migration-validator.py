#!/usr/bin/env python3
"""
🛡️ Migration Validator - Checks migration safety before execution
Follows The Architect's safety protocol.
"""
import sys
import re
from pathlib import Path

# Dangerous operations that require special handling
DANGEROUS_OPS = {
    'DROP TABLE': '🚨 Table deletion - requires full backup',
    'DROP COLUMN': '🚨 Column deletion - use deprecation instead',
    'ALTER COLUMN TYPE': '🚨 Type change - requires table rewrite',
    'TRUNCATE': '🚨 Data truncation - irreversible',
    'RENAME COLUMN': '⚠️ Rename - breaks application code',
    'RENAME TABLE': '⚠️ Rename - breaks application code',
}

# Safe operations
SAFE_OPS = [
    'ADD COLUMN',
    'CREATE TABLE',
    'CREATE INDEX CONCURRENTLY',
    'ADD CONSTRAINT',
]

def validate_migration(file_path: str) -> tuple:
    """Validate migration file and return (is_safe, issues, warnings)"""
    
    path = Path(file_path)
    if not path.exists():
        return False, [f"File not found: {file_path}"], []
    
    content = path.read_text()
    content_upper = content.upper()
    
    issues = []
    warnings = []
    
    # Check for dangerous operations
    for op, description in DANGEROUS_OPS.items():
        if op in content_upper:
            issues.append(f"{description}")
    
    # Check for index creation without CONCURRENTLY
    if 'CREATE INDEX' in content_upper and 'CONCURRENTLY' not in content_upper:
        warnings.append("⚠️ Index creation without CONCURRENTLY - will lock table")
    
    # Check for new tables without RLS
    if 'CREATE TABLE' in content_upper:
        if 'ENABLE ROW LEVEL SECURITY' not in content_upper:
            warnings.append("⚠️ New table without RLS enabled")
        if 'CREATE POLICY' not in content_upper:
            warnings.append("⚠️ New table without RLS policies")
    
    # Check for missing rollback
    if 'ROLLBACK' not in content_upper and '-- DOWN' not in content_upper:
        warnings.append("ℹ️ No rollback plan documented")
    
    is_safe = len(issues) == 0
    
    return is_safe, issues, warnings

def main():
    if len(sys.argv) < 2:
        print("🗄️ THE ARCHITECT: Migration Validator")
        print("=" * 50)
        print("Usage: migration-validator.py <migration-file.sql>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print("🗄️ THE ARCHITECT: Migration Validator")
    print("=" * 50)
    print(f"Validating: {file_path}\n")
    
    is_safe, issues, warnings = validate_migration(file_path)
    
    if issues:
        print("🚨 ISSUES DETECTED (Blocking)")
        for issue in issues:
            print(f"   • {issue}")
        print()
    
    if warnings:
        print("⚠️ WARNINGS")
        for warning in warnings:
            print(f"   • {warning}")
        print()
    
    if is_safe and not warnings:
        print("✅ MIGRATION VALIDATION PASSED")
        print("   Safe to execute (after Guardian review)")
    elif is_safe:
        print("⚠️ MIGRATION APPROVED WITH WARNINGS")
        print("   Review warnings before execution")
    else:
        print("❌ MIGRATION BLOCKED")
        print("   Fix issues before execution")
    
    sys.exit(0 if is_safe else 1)

if __name__ == "__main__":
    main()
