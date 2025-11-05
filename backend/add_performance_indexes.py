#!/usr/bin/env python3
"""
Performance optimization script: Add database indexes to improve query performance
Run this script to add indexes to existing databases without recreating tables.
"""
from sqlalchemy import create_engine, text
from app.config import settings
import sys


def add_indexes():
    """Add performance indexes to the database"""
    engine = create_engine(settings.DATABASE_URL)
    
    indexes = [
        # OptimizationSession indexes
        ("idx_opt_session_user_id", "optimization_sessions", "user_id"),
        ("idx_opt_session_status", "optimization_sessions", "status"),
        ("idx_opt_session_created_at", "optimization_sessions", "created_at"),
        
        # OptimizationSegment indexes
        ("idx_opt_segment_session_id", "optimization_segments", "session_id"),
        ("idx_opt_segment_index", "optimization_segments", "segment_index"),
        ("idx_opt_segment_status", "optimization_segments", "status"),
        
        # ChangeLog indexes
        ("idx_change_log_session_id", "change_logs", "session_id"),
        ("idx_change_log_segment_index", "change_logs", "segment_index"),
        ("idx_change_log_stage", "change_logs", "stage"),
    ]
    
    with engine.connect() as connection:
        for index_name, table_name, column_name in indexes:
            try:
                # Check if index already exists (for SQLite and PostgreSQL)
                if 'sqlite' in settings.DATABASE_URL:
                    # SQLite: Try to create index, ignore if exists
                    connection.execute(text(
                        f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({column_name})"
                    ))
                else:
                    # PostgreSQL: Check and create if not exists
                    check_query = text("""
                        SELECT 1 FROM pg_indexes 
                        WHERE indexname = :index_name
                    """)
                    result = connection.execute(check_query, {"index_name": index_name})
                    if not result.fetchone():
                        connection.execute(text(
                            f"CREATE INDEX {index_name} ON {table_name} ({column_name})"
                        ))
                        print(f"✓ Created index: {index_name}")
                    else:
                        print(f"→ Index already exists: {index_name}")
                
                connection.commit()
            except Exception as e:
                print(f"✗ Error creating index {index_name}: {e}")
                connection.rollback()
    
    print("\n✓ Database indexes optimization completed!")


if __name__ == "__main__":
    try:
        print("Adding performance indexes to database...")
        add_indexes()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
