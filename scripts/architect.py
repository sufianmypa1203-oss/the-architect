#!/usr/bin/env python3
"""
🗄️ The Architect CLI
Usage:
  architect schema <table>
  architect migrate <description>
  architect optimize "<query>"
  architect erd
  architect rls <table>
  architect benchmark <table>
  architect integrity-check
"""
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


def main():
    parser = argparse.ArgumentParser(
        description="🗄️ The Architect - Database God CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  architect schema transactions
  architect migrate "add notes column to users"
  architect optimize "SELECT * FROM transactions WHERE user_id = $1"
  architect rls transactions
  architect erd
  architect benchmark transactions
  architect integrity-check
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # schema
    schema_p = subparsers.add_parser('schema', help='Generate complete schema')
    schema_p.add_argument('table', help='Table name')
    schema_p.add_argument('--purpose', '-p', default='', help='Table purpose')
    
    # migrate
    migrate_p = subparsers.add_parser('migrate', help='Create safe migration')
    migrate_p.add_argument('description', help='Migration description')
    
    # optimize
    optimize_p = subparsers.add_parser('optimize', help='Optimize SQL query')
    optimize_p.add_argument('query', help='SQL query to optimize')
    
    # erd
    subparsers.add_parser('erd', help='Generate ERD diagram')
    
    # rls
    rls_p = subparsers.add_parser('rls', help='Generate RLS policies')
    rls_p.add_argument('table', help='Table name')
    
    # benchmark
    bench_p = subparsers.add_parser('benchmark', help='Run performance benchmark')
    bench_p.add_argument('table', help='Table name')
    
    # integrity-check
    subparsers.add_parser('integrity-check', help='Check database integrity')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        from architect_agent import ArchitectCommands
        commands = ArchitectCommands()
    except ImportError:
        # Fallback to direct tool usage if CrewAI not installed
        print("⚠️ CrewAI not installed. Using direct tool access.\n")
        from architect_tools import (
            SchemaDesignerTool, RLSPolicyGeneratorTool,
            QueryOptimizerTool, PerformanceBenchmarkerTool,
            IntegrityCheckerTool, ERDGeneratorTool
        )
        
        if args.command == 'schema':
            tool = SchemaDesignerTool()
            result = tool._run(args.table, args.purpose or f"{args.table} data", [])
        elif args.command == 'rls':
            tool = RLSPolicyGeneratorTool()
            result = tool._run(args.table)
        elif args.command == 'optimize':
            tool = QueryOptimizerTool()
            result = tool._run(args.query)
        elif args.command == 'benchmark':
            tool = PerformanceBenchmarkerTool()
            result = tool._run(args.table)
        elif args.command == 'integrity-check':
            tool = IntegrityCheckerTool()
            result = tool._run()
        elif args.command == 'erd':
            tool = ERDGeneratorTool()
            result = tool._run([])
        else:
            result = f"Command '{args.command}' requires CrewAI"
        
        print(result)
        return
    
    # Full CrewAI execution
    if args.command == 'schema':
        result = commands.schema(args.table, args.purpose)
    elif args.command == 'migrate':
        result = commands.migrate(args.description)
    elif args.command == 'optimize':
        result = commands.optimize(args.query)
    elif args.command == 'erd':
        result = commands.erd()
    elif args.command == 'rls':
        result = commands.rls(args.table)
    elif args.command == 'benchmark':
        result = commands.benchmark(args.table)
    elif args.command == 'integrity-check':
        result = commands.integrity_check()
    
    print(result)


if __name__ == '__main__':
    main()
