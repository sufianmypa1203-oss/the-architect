# 🗄️ The Architect

**The Database God** - Owns everything under the hood: Supabase schemas, migrations, indexes, RLS policies, edge functions, and data integrity.

> "A database migration is a one-way door. Think twice before you walk through."

## 🚀 Quick Start

1. Copy `AGENT.md` to your project: `.agent/agents/the-architect.md`
2. Add scripts to your project: `cp -r scripts/ .agent/scripts/architect/`
3. Activate with: `/architect` or use any trigger phrase

## ⚡ Commands

| Command | Description |
|---------|-------------|
| `/architect schema <table>` | Generate complete table schema |
| `/architect migrate <change>` | Create migration with safety checklist |
| `/architect optimize <query>` | Analyze and optimize query |
| `/architect erd` | Generate ERD diagram |
| `/architect rls <table>` | Generate RLS policies |
| `/architect benchmark <table>` | Run performance benchmark |
| `/architect integrity-check` | Verify constraints |

## 🧰 Included Scripts

- `schema-visualizer.py` - Generates ERD from database
- `migration-validator.py` - Checks migration safety
- `rls-auditor.py` - Verifies RLS on all tables
- `query-benchmarker.py` - Performance testing
- `index-analyzer.py` - Suggests missing indexes

## 🎯 Core Principles

1. **RLS Mandatory**: Every user table MUST have policies
2. **UUID Primary Keys**: Always use `gen_random_uuid()`
3. **Audit Fields**: Every table needs `created_at`, `updated_at`, `deleted_at`
4. **CONCURRENTLY**: Create indexes without locking
5. **Additive Only**: Never DROP columns - deprecate instead

## 🤝 Collaboration

- **The Guardian**: All migrations pass Guardian audit before execution
- **The Strategist**: Schema design happens in Phase 3 (Solutioning)

## License

MIT
