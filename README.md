# 🗄️ The Architect

**The Database God** - Complete CrewAI agent for Supabase/PostgreSQL mastery.

> "A database migration is a one-way door. Think twice before you walk through."

## 🚀 Quick Start

### Installation
```bash
# Install dependencies
pip install crewai psycopg2-binary

# Clone the agent
git clone https://github.com/sufianmypa1203-oss/the-architect.git
cd the-architect

# Run CLI
python scripts/architect.py --help
```

### Usage
```bash
# Design a table schema
python scripts/architect.py schema transactions

# Generate RLS policies
python scripts/architect.py rls transactions

# Create a migration
python scripts/architect.py migrate "add notes column to users"

# Optimize a query
python scripts/architect.py optimize "SELECT * FROM transactions WHERE user_id = $1"

# Generate ERD
python scripts/architect.py erd

# Run benchmark
python scripts/architect.py benchmark transactions

# Check integrity
python scripts/architect.py integrity-check
```

## 📦 What's Included

```
the-architect/
├── AGENT.md              # Full agent persona
├── README.md             # This file
├── src/
│   ├── architect_tools.py    # 7 CrewAI tools
│   └── architect_agent.py    # Agent runner
├── scripts/
│   ├── architect.py          # CLI entry point
│   ├── schema-visualizer.py  # ERD generation
│   ├── migration-validator.py # Safety checks
│   ├── rls-auditor.py        # RLS verification
│   ├── query-benchmarker.py  # Performance testing
│   └── index-analyzer.py     # Index recommendations
├── config/
│   └── architect_tasks.yaml  # Task configurations
├── examples/
│   └── transactions_schema.sql # Reference implementation
└── tests/
    └── test_architect.py     # pytest test suite
```

## 🧰 CrewAI Tools

| Tool | Description |
|------|-------------|
| `SchemaDesignerTool` | Generates production-ready table schemas |
| `RLSPolicyGeneratorTool` | Creates Row Level Security policies |
| `MigrationGeneratorTool` | Builds safe migrations with checklists |
| `QueryOptimizerTool` | Analyzes and optimizes SQL queries |
| `ERDGeneratorTool` | Creates Mermaid ERD diagrams |
| `PerformanceBenchmarkerTool` | Runs performance benchmarks |
| `IntegrityCheckerTool` | Validates database integrity |

## 🎯 Core Principles

1. **RLS Mandatory** - Every user table must have policies
2. **UUID Primary Keys** - Always `gen_random_uuid()`
3. **Audit Fields** - `created_at`, `updated_at`, `deleted_at`
4. **CONCURRENTLY** - Create indexes without locking
5. **Additive Only** - Never DROP columns

## 🧪 Running Tests
```bash
cd the-architect
pytest tests/ -v
```

## 🤝 Agent Collaboration

- **The Guardian**: Reviews migrations before execution
- **The Strategist**: Coordinates schema design during planning

## License

MIT
