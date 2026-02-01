# Changelog

All notable changes to The Architect will be documented in this file.

## [1.1.0] - 2026-02-01

### Added - Full CrewAI Implementation
- `src/architect_tools.py` - 7 complete CrewAI tool classes
  - SchemaDesignerTool
  - RLSPolicyGeneratorTool
  - MigrationGeneratorTool
  - QueryOptimizerTool
  - ERDGeneratorTool
  - PerformanceBenchmarkerTool
  - IntegrityCheckerTool
- `src/architect_agent.py` - Full agent runner with ArchitectCrew class
- `config/architect_tasks.yaml` - YAML task configurations
- `examples/transactions_schema.sql` - Complete reference implementation
- `tests/test_architect.py` - pytest test suite (12 tests)
- `scripts/architect.py` - Full CLI with argparse

### Changed
- Factory now delivers COMPLETE agents, not just persona files
- CLI works with or without CrewAI installed

## [1.0.0] - 2026-02-01

### Added
- Initial release with agent persona
- 5 utility scripts
- README, LICENSE, CHANGELOG
