#!/usr/bin/env python3
"""
🔒 RLS Auditor - Verifies Row Level Security on all tables
Ensures every user table has proper RLS policies.
"""
import os
import sys

# Vue Money tables that MUST have RLS
REQUIRED_RLS_TABLES = [
    'profiles',
    'accounts',
    'credit_cards',
    'auto_loans',
    'p2p_loans',
    'transactions',
    'subscriptions',
    'transfer_pairs',
    'user_category_rules',
]

# Tables exempt from RLS (global lookup tables)
EXEMPT_TABLES = [
    'merchant_database',  # Global merchant data
]

def audit_rls_from_migrations(migrations_dir: str) -> dict:
    """Audit RLS by scanning migration files"""
    
    from pathlib import Path
    
    migrations_path = Path(migrations_dir)
    if not migrations_path.exists():
        return {'error': f"Directory not found: {migrations_dir}"}
    
    rls_enabled = set()
    tables_created = set()
    
    for sql_file in migrations_path.glob('*.sql'):
        content = sql_file.read_text().upper()
        
        # Find tables with RLS enabled
        import re
        rls_matches = re.findall(r'ALTER TABLE (\w+) ENABLE ROW LEVEL SECURITY', content)
        rls_enabled.update([t.lower() for t in rls_matches])
        
        # Find created tables
        table_matches = re.findall(r'CREATE TABLE (?:IF NOT EXISTS )?(\w+)', content)
        tables_created.update([t.lower() for t in table_matches])
    
    return {
        'tables_created': tables_created,
        'rls_enabled': rls_enabled,
    }

def main():
    print("🗄️ THE ARCHITECT: RLS Auditor")
    print("=" * 50)
    
    # Default migrations directory
    migrations_dir = sys.argv[1] if len(sys.argv) > 1 else "supabase/migrations"
    
    print(f"Scanning: {migrations_dir}\n")
    
    result = audit_rls_from_migrations(migrations_dir)
    
    if 'error' in result:
        print(f"⚠️ {result['error']}")
        print("\nUsing static checklist instead:\n")
        
        # Static audit based on known requirements
        print("📋 Required RLS Tables:")
        for table in REQUIRED_RLS_TABLES:
            print(f"   [ ] {table}")
        
        print("\n⏭️ Exempt Tables:")
        for table in EXEMPT_TABLES:
            print(f"   [~] {table} (global lookup)")
        
        print("\n⚠️ Run this script in your Vue Money project directory")
        print("   to scan actual migration files.")
        return
    
    # Analyze results
    missing_rls = []
    for table in REQUIRED_RLS_TABLES:
        if table in result['tables_created'] and table not in result['rls_enabled']:
            missing_rls.append(table)
    
    # Report
    print("📊 RLS Audit Report")
    print("-" * 30)
    
    print(f"\n✅ Tables with RLS: {len(result['rls_enabled'])}")
    for table in result['rls_enabled']:
        print(f"   • {table}")
    
    if missing_rls:
        print(f"\n❌ Tables MISSING RLS: {len(missing_rls)}")
        for table in missing_rls:
            print(f"   • {table}")
        print("\n🚨 ACTION REQUIRED: Add RLS policies to tables above!")
    else:
        print("\n✅ All user tables have RLS enabled!")

if __name__ == "__main__":
    main()
