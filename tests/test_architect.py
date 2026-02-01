"""
🗄️ The Architect - Test Suite
Validates all tools and agent functionality.
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from architect_tools import (
    SchemaDesignerTool,
    RLSPolicyGeneratorTool,
    MigrationGeneratorTool,
    QueryOptimizerTool
)


class TestSchemaDesigner:
    """Tests for SchemaDesignerTool"""
    
    def test_includes_audit_fields(self):
        """Schemas must include audit fields"""
        tool = SchemaDesignerTool()
        result = tool._run(
            table_name="test_table",
            purpose="Test table",
            columns=[{'name': 'name', 'type': 'TEXT'}]
        )
        
        assert 'created_at TIMESTAMPTZ' in result
        assert 'updated_at TIMESTAMPTZ' in result
        assert 'deleted_at TIMESTAMPTZ' in result
    
    def test_uses_uuid_primary_key(self):
        """Schemas must use UUID primary keys"""
        tool = SchemaDesignerTool()
        result = tool._run(
            table_name="test_table",
            purpose="Test",
            columns=[]
        )
        
        assert 'id UUID PRIMARY KEY' in result
        assert 'gen_random_uuid()' in result
    
    def test_includes_table_comment(self):
        """Schemas must include table documentation"""
        tool = SchemaDesignerTool()
        result = tool._run(
            table_name="my_table",
            purpose="Stores user data",
            columns=[]
        )
        
        assert 'COMMENT ON TABLE my_table' in result


class TestRLSPolicyGenerator:
    """Tests for RLSPolicyGeneratorTool"""
    
    def test_includes_all_crud_policies(self):
        """RLS must cover all CRUD operations"""
        tool = RLSPolicyGeneratorTool()
        result = tool._run(table_name="test_table")
        
        assert 'FOR SELECT' in result
        assert 'FOR INSERT' in result
        assert 'FOR UPDATE' in result
        assert 'FOR DELETE' in result
    
    def test_includes_service_role_bypass(self):
        """RLS must include service role bypass"""
        tool = RLSPolicyGeneratorTool()
        result = tool._run(table_name="test_table")
        
        assert 'service_role' in result
        assert 'USING (true)' in result
    
    def test_requires_authentication(self):
        """RLS policies must require authentication"""
        tool = RLSPolicyGeneratorTool()
        result = tool._run(table_name="test_table")
        
        assert 'TO authenticated' in result
        assert 'auth.uid()' in result


class TestMigrationGenerator:
    """Tests for MigrationGeneratorTool"""
    
    def test_detects_dangerous_drop_table(self):
        """Must flag DROP TABLE as dangerous"""
        tool = MigrationGeneratorTool()
        result = tool._run(
            migration_name="dangerous",
            up_sql="DROP TABLE users;",
            down_sql="-- recreate"
        )
        
        assert 'DROP TABLE detected' in result
        assert '❌ NO' in result
    
    def test_approves_additive_changes(self):
        """Additive changes should be marked safe"""
        tool = MigrationGeneratorTool()
        result = tool._run(
            migration_name="add_column",
            up_sql="ALTER TABLE users ADD COLUMN notes TEXT;",
            down_sql="ALTER TABLE users DROP COLUMN notes;"
        )
        
        assert '✅ YES' in result
    
    def test_warns_about_non_concurrent_index(self):
        """Must warn about indexes without CONCURRENTLY"""
        tool = MigrationGeneratorTool()
        result = tool._run(
            migration_name="add_index",
            up_sql="CREATE INDEX idx_test ON test(col);",
            down_sql="DROP INDEX idx_test;"
        )
        
        assert 'CONCURRENTLY' in result or 'lock' in result.lower()


class TestQueryOptimizer:
    """Tests for QueryOptimizerTool"""
    
    def test_detects_select_star(self):
        """Must flag SELECT * as inefficient"""
        tool = QueryOptimizerTool()
        result = tool._run("SELECT * FROM users WHERE id = 1")
        
        assert 'SELECT *' in result
        assert 'wasteful' in result.lower() or 'columns' in result.lower()
    
    def test_warns_about_missing_where(self):
        """Must warn about missing WHERE clause"""
        tool = QueryOptimizerTool()
        result = tool._run("SELECT id FROM large_table")
        
        assert 'WHERE' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
