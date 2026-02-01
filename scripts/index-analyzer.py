#!/usr/bin/env python3
"""
📊 Index Analyzer - Suggests missing indexes for common queries
Analyzes query patterns and recommends optimal indexes.
"""
import sys
import re

# Common query patterns and their index recommendations
QUERY_PATTERNS = {
    'user_lookup': {
        'pattern': r'WHERE\s+user_id\s*=',
        'description': 'User-based lookup',
        'index': 'CREATE INDEX CONCURRENTLY idx_{table}_user_id ON {table}(user_id);',
    },
    'date_range': {
        'pattern': r'WHERE.*(?:created_at|updated_at|transaction_date)\s*(?:>|<|BETWEEN)',
        'description': 'Date range query',
        'index': 'CREATE INDEX CONCURRENTLY idx_{table}_date ON {table}({date_col} DESC);',
    },
    'order_by_date': {
        'pattern': r'ORDER BY\s+(?:created_at|updated_at|transaction_date)',
        'description': 'Ordered by date',
        'index': 'CREATE INDEX CONCURRENTLY idx_{table}_date ON {table}({date_col} DESC);',
    },
    'foreign_key': {
        'pattern': r'WHERE\s+\w+_id\s*=',
        'description': 'Foreign key lookup',
        'index': 'CREATE INDEX CONCURRENTLY idx_{table}_{fk} ON {table}({fk});',
    },
}

def analyze_query(query: str, table_name: str = 'TABLE') -> list:
    """Analyze query and return index recommendations"""
    
    recommendations = []
    query_upper = query.upper()
    
    # Check for SELECT *
    if 'SELECT *' in query_upper:
        recommendations.append({
            'issue': 'SELECT * fetches all columns',
            'suggestion': 'Select only needed columns for better performance',
        })
    
    # Check for missing WHERE
    if 'WHERE' not in query_upper and 'LIMIT' not in query_upper:
        recommendations.append({
            'issue': 'No WHERE clause',
            'suggestion': 'Add WHERE clause or LIMIT to avoid full table scan',
        })
    
    # Check patterns
    for name, pattern_info in QUERY_PATTERNS.items():
        if re.search(pattern_info['pattern'], query_upper, re.IGNORECASE):
            recommendations.append({
                'issue': pattern_info['description'] + ' detected',
                'suggestion': pattern_info['index'].format(table=table_name, date_col='created_at', fk='column_id'),
            })
    
    return recommendations

def main():
    print("🗄️ THE ARCHITECT: Index Analyzer")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage: index-analyzer.py \"<sql-query>\"")
        print("\nExample:")
        print('  index-analyzer.py "SELECT * FROM transactions WHERE user_id = $1"')
        sys.exit(1)
    
    query = sys.argv[1]
    
    print(f"Analyzing query:\n{query}\n")
    print("-" * 50)
    
    recommendations = analyze_query(query, 'transactions')
    
    if not recommendations:
        print("✅ Query looks optimized!")
    else:
        print("📋 Recommendations:\n")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. Issue: {rec['issue']}")
            print(f"   Fix: {rec['suggestion']}")
            print()

if __name__ == "__main__":
    main()
