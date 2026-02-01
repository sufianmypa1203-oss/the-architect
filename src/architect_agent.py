"""
🗄️ The Architect - CrewAI Agent Runner
Main agent implementation with all tasks.
"""
from crewai import Agent, Task, Crew, Process
from typing import List, Dict
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from architect_tools import (
    SchemaDesignerTool,
    RLSPolicyGeneratorTool,
    MigrationGeneratorTool,
    QueryOptimizerTool,
    ERDGeneratorTool,
    PerformanceBenchmarkerTool,
    IntegrityCheckerTool
)


# Initialize tools
schema_designer = SchemaDesignerTool()
rls_generator = RLSPolicyGeneratorTool()
migration_generator = MigrationGeneratorTool()
query_optimizer = QueryOptimizerTool()
erd_generator = ERDGeneratorTool()
performance_benchmarker = PerformanceBenchmarkerTool()
integrity_checker = IntegrityCheckerTool()


def create_architect_agent() -> Agent:
    """Creates The Architect agent"""
    return Agent(
        role="Principal Database Engineer & Supabase Specialist",
        goal="Ensure the data layer is bulletproof, scalable, fast, and secure",
        backstory="""You are The Architect, a principal-level database engineer who has 
        built and scaled production databases serving millions of users. You believe 
        'A database migration is a one-way door. Think twice before you walk through.'
        You are technical, precise, and never hand-wave complexity. You speak in SQL, 
        think in relationships, and breathe performance optimization.""",
        tools=[
            schema_designer,
            rls_generator,
            migration_generator,
            query_optimizer,
            erd_generator,
            performance_benchmarker,
            integrity_checker
        ],
        verbose=True,
        allow_delegation=True,
        memory=True,
        max_iter=25
    )


def create_schema_task(agent: Agent, table_name: str, purpose: str) -> Task:
    """Create schema design task"""
    return Task(
        description=f"""Design a production-ready schema for table: {table_name}
        Purpose: {purpose}
        
        Requirements:
        1. UUID primary key with gen_random_uuid()
        2. Appropriate data types (DECIMAL for money, TIMESTAMPTZ for timestamps)
        3. Foreign keys with ON DELETE clause
        4. Audit fields (created_at, updated_at, deleted_at)
        5. Strategic indexes for query patterns
        6. RLS policies for user isolation
        
        Output complete, copy-paste ready SQL.""",
        expected_output="Complete CREATE TABLE SQL with constraints, indexes, and RLS",
        agent=agent
    )


def create_migration_task(agent: Agent, description: str) -> Task:
    """Create migration generation task"""
    return Task(
        description=f"""Generate a safe database migration for: {description}
        
        Requirements:
        1. Include UP and DOWN migrations
        2. Add safety checklist
        3. Analyze for risks
        4. Verify migration is additive
        5. Require Guardian approval
        
        Migrations MUST be reversible.""",
        expected_output="Migration file with safety checklist and rollback plan",
        agent=agent
    )


def create_optimization_task(agent: Agent, query: str) -> Task:
    """Create query optimization task"""
    return Task(
        description=f"""Optimize this SQL query for performance:
        
        {query}
        
        Requirements:
        1. Identify issues (SELECT *, missing indexes, N+1)
        2. Recommend specific indexes
        3. Provide optimized query version
        4. Estimate performance improvement""",
        expected_output="Query optimization report with recommendations",
        agent=agent
    )


def create_rls_task(agent: Agent, table_name: str) -> Task:
    """Create RLS policy generation task"""
    return Task(
        description=f"""Generate comprehensive RLS policies for: {table_name}
        
        Requirements:
        1. Enable RLS on table
        2. Policies for SELECT, INSERT, UPDATE, DELETE
        3. User isolation pattern (auth.uid() = user_id)
        4. Service role bypass for background jobs
        5. Grant appropriate permissions""",
        expected_output="Complete RLS policy SQL",
        agent=agent
    )


class ArchitectCrew:
    """The Architect Crew - manages agent and tasks"""
    
    def __init__(self):
        self.agent = create_architect_agent()
    
    def design_schema(self, table_name: str, purpose: str) -> str:
        """Design a complete table schema"""
        task = create_schema_task(self.agent, table_name, purpose)
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        return crew.kickoff()
    
    def generate_migration(self, description: str) -> str:
        """Generate a safe migration"""
        task = create_migration_task(self.agent, description)
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        return crew.kickoff()
    
    def optimize_query(self, query: str) -> str:
        """Optimize a SQL query"""
        task = create_optimization_task(self.agent, query)
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        return crew.kickoff()
    
    def generate_rls(self, table_name: str) -> str:
        """Generate RLS policies"""
        task = create_rls_task(self.agent, table_name)
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        return crew.kickoff()
    
    def generate_erd(self, tables: List[Dict]) -> str:
        """Generate ERD diagram"""
        return erd_generator._run(tables)
    
    def run_benchmark(self, table_name: str) -> str:
        """Run performance benchmark"""
        return performance_benchmarker._run(table_name)
    
    def check_integrity(self) -> str:
        """Check database integrity"""
        return integrity_checker._run()


# CLI Commands
class ArchitectCommands:
    """CLI command handlers"""
    
    def __init__(self):
        self.crew = ArchitectCrew()
    
    def schema(self, table_name: str, purpose: str = ""):
        """Generate complete schema"""
        print(f"🗄️ Designing schema for: {table_name}")
        return self.crew.design_schema(table_name, purpose or f"{table_name} data")
    
    def migrate(self, description: str):
        """Generate migration"""
        print(f"🔄 Creating migration: {description}")
        return self.crew.generate_migration(description)
    
    def optimize(self, query: str):
        """Optimize query"""
        print("⚡ Analyzing query performance...")
        return self.crew.optimize_query(query)
    
    def rls(self, table_name: str):
        """Generate RLS policies"""
        print(f"🔒 Generating RLS policies for: {table_name}")
        return self.crew.generate_rls(table_name)
    
    def erd(self):
        """Generate ERD"""
        print("📊 Generating ERD...")
        # Vue Money tables
        tables = [
            {'name': 'users', 'columns': [{'name': 'id', 'type': 'UUID'}]},
            {'name': 'accounts', 'columns': [{'name': 'id', 'type': 'UUID'}, {'name': 'user_id', 'type': 'UUID'}]},
            {'name': 'transactions', 'columns': [{'name': 'id', 'type': 'UUID'}, {'name': 'account_id', 'type': 'UUID'}]},
        ]
        return self.crew.generate_erd(tables)
    
    def benchmark(self, table_name: str):
        """Run benchmark"""
        print(f"⏱️ Benchmarking: {table_name}")
        return self.crew.run_benchmark(table_name)
    
    def integrity_check(self):
        """Check integrity"""
        print("🔍 Running integrity checks...")
        return self.crew.check_integrity()


if __name__ == "__main__":
    # Quick test
    commands = ArchitectCommands()
    print(commands.integrity_check())
