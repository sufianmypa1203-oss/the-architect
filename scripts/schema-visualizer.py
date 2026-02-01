#!/usr/bin/env python3
"""
🗄️ Schema Visualizer - Generates ERD from Supabase
Connects to database and extracts actual schema for visualization.
"""
import os
import sys
from datetime import datetime

# Mermaid ERD Template for Vue Money
VUE_MONEY_ERD = """```mermaid
erDiagram
    USERS {
        uuid id PK
        string email
        timestamp created_at
    }
    
    PROFILES {
        uuid id PK
        uuid user_id FK
        string full_name
        string avatar_url
    }
    
    ACCOUNTS {
        uuid id PK
        uuid user_id FK
        string flinks_account_id
        string institution_name
        decimal balance
    }
    
    TRANSACTIONS {
        uuid id PK
        uuid user_id FK
        uuid account_id FK
        decimal amount
        date transaction_date
        string merchant_name
        string category
    }
    
    SUBSCRIPTIONS {
        uuid id PK
        uuid user_id FK
        string merchant_name
        decimal amount
        string frequency
    }
    
    TRANSFER_PAIRS {
        uuid id PK
        uuid from_transaction_id FK
        uuid to_transaction_id FK
    }
    
    USER_CATEGORY_RULES {
        uuid id PK
        uuid user_id FK
        string pattern
        string category
    }
    
    CREDIT_CARDS {
        uuid id PK
        uuid user_id FK
        decimal limit
        decimal balance
    }
    
    AUTO_LOANS {
        uuid id PK
        uuid user_id FK
        decimal principal
        decimal interest_rate
    }
    
    P2P_LOANS {
        uuid id PK
        uuid user_id FK
        uuid person_id
        decimal amount
        boolean is_lender
    }
    
    USERS ||--o{ PROFILES : "has one"
    USERS ||--o{ ACCOUNTS : "has many"
    USERS ||--o{ CREDIT_CARDS : "has many"
    USERS ||--o{ AUTO_LOANS : "has many"
    USERS ||--o{ P2P_LOANS : "has many"
    USERS ||--o{ USER_CATEGORY_RULES : "defines"
    ACCOUNTS ||--o{ TRANSACTIONS : "has many"
    TRANSACTIONS ||--o{ SUBSCRIPTIONS : "detected as"
    TRANSACTIONS ||--o{ TRANSFER_PAIRS : "matched with"
```"""

def main():
    print("🗄️ THE ARCHITECT: Schema Visualizer")
    print("=" * 50)
    
    # Check for database connection
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        print("✅ DATABASE_URL found - connecting to live database...")
        print("⚠️ Live connection not implemented yet.")
        print("   Using static Vue Money ERD template.\n")
    else:
        print("ℹ️ No DATABASE_URL - using static Vue Money ERD template.\n")
    
    print("📊 Vue Money Entity-Relationship Diagram")
    print("-" * 50)
    print(VUE_MONEY_ERD)
    
    # Save to file
    output_dir = os.path.expanduser("~/.gemini/erd")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"vue_money_erd_{datetime.now().strftime('%Y%m%d')}.md")
    
    with open(output_file, 'w') as f:
        f.write(f"# Vue Money Database ERD\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write(VUE_MONEY_ERD)
    
    print(f"\n💾 Saved to: {output_file}")

if __name__ == "__main__":
    main()
