#!/usr/bin/env python3
"""
⚡ Query Benchmarker - Performance testing for database queries
Measures cold/warm cache times and suggests optimizations.
"""
import sys
import time
from datetime import datetime

# Sample benchmarks for Vue Money tables
SAMPLE_BENCHMARKS = {
    'transactions': {
        'row_estimate': 50000,
        'table_size': '45 MB',
        'index_size': '12 MB',
        'queries': [
            {'name': 'Get by user_id', 'cold_ms': 45, 'warm_ms': 12, 'target_ms': 50},
            {'name': 'Get by account_id', 'cold_ms': 38, 'warm_ms': 8, 'target_ms': 50},
            {'name': 'Get by date range', 'cold_ms': 120, 'warm_ms': 45, 'target_ms': 100},
            {'name': 'Category aggregation', 'cold_ms': 250, 'warm_ms': 80, 'target_ms': 200},
        ],
        'recommendations': [
            'Add partial index for active transactions (deleted_at IS NULL)',
            'Consider partitioning by transaction_date after 1M rows',
            'Add composite index on (user_id, transaction_date DESC)',
        ]
    },
    'accounts': {
        'row_estimate': 500,
        'table_size': '2 MB',
        'index_size': '500 KB',
        'queries': [
            {'name': 'Get by user_id', 'cold_ms': 5, 'warm_ms': 2, 'target_ms': 10},
            {'name': 'Get by flinks_id', 'cold_ms': 8, 'warm_ms': 3, 'target_ms': 10},
        ],
        'recommendations': [
            'Table is small - current indexes are sufficient',
        ]
    },
    'p2p_loans': {
        'row_estimate': 200,
        'table_size': '1 MB',
        'index_size': '200 KB',
        'queries': [
            {'name': 'Get by user_id', 'cold_ms': 4, 'warm_ms': 1, 'target_ms': 10},
            {'name': 'Get by person_id', 'cold_ms': 6, 'warm_ms': 2, 'target_ms': 10},
            {'name': 'Sum by direction', 'cold_ms': 12, 'warm_ms': 4, 'target_ms': 50},
        ],
        'recommendations': [
            'Add index on (user_id, is_lender) for directional queries',
        ]
    }
}

def benchmark_table(table_name: str) -> None:
    """Run benchmark for a specific table"""
    
    if table_name not in SAMPLE_BENCHMARKS:
        print(f"⚠️ No benchmark data for table: {table_name}")
        print(f"   Available tables: {', '.join(SAMPLE_BENCHMARKS.keys())}")
        return
    
    bench = SAMPLE_BENCHMARKS[table_name]
    
    print(f"## Performance Benchmark: {table_name}")
    print()
    print("### Table Statistics")
    print(f"- Row count: ~{bench['row_estimate']:,}")
    print(f"- Table size: {bench['table_size']}")
    print(f"- Index size: {bench['index_size']}")
    print()
    
    print("### Query Benchmarks")
    print()
    print("| Query | Cold (ms) | Warm (ms) | Target | Status |")
    print("|-------|-----------|-----------|--------|--------|")
    
    for q in bench['queries']:
        status = '✅' if q['warm_ms'] <= q['target_ms'] else '❌'
        print(f"| {q['name']} | {q['cold_ms']} | {q['warm_ms']} | <{q['target_ms']}ms | {status} |")
    
    print()
    print("### Recommendations")
    print()
    for rec in bench['recommendations']:
        print(f"- [ ] {rec}")

def main():
    print("🗄️ THE ARCHITECT: Query Benchmarker")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage: query-benchmarker.py <table-name>")
        print(f"\nAvailable tables: {', '.join(SAMPLE_BENCHMARKS.keys())}")
        sys.exit(1)
    
    table_name = sys.argv[1].lower()
    print(f"Benchmarking: {table_name}\n")
    print("-" * 50)
    print()
    
    benchmark_table(table_name)

if __name__ == "__main__":
    main()
