from sqlalchemy import create_engine, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """数据库会话依赖"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库 - 安全地创建或更新数据库结构"""
    try:
        # 导入所有模型以确保它们被注册到 Base.metadata
        from app.models import models  # noqa: F401
        
        # 创建所有表（如果不存在）
        Base.metadata.create_all(bind=engine)
        
        # 检查并添加可能缺失的列（用于数据库迁移）
        _migrate_database_schema()
        
        print("✓ 数据库初始化成功")
        return True
    except Exception as e:
        print(f"✗ 数据库初始化失败: {str(e)}")
        raise


def _migrate_database_schema():
    """迁移数据库结构 - 添加新列到已存在的表"""
    try:
        with engine.connect() as conn:
            inspector = inspect(engine)
            
            # 检查表是否存在
            tables = inspector.get_table_names()
            
            # 迁移 optimization_sessions 表
            if "optimization_sessions" in tables:
                columns = {column["name"] for column in inspector.get_columns("optimization_sessions")}
                
                if "failed_segment_index" not in columns:
                    conn.execute(text("ALTER TABLE optimization_sessions ADD COLUMN failed_segment_index INTEGER"))
                    conn.commit()
                    print("  ✓ 添加字段: optimization_sessions.failed_segment_index")
                
                if "processing_mode" not in columns:
                    conn.execute(text("ALTER TABLE optimization_sessions ADD COLUMN processing_mode VARCHAR(50) DEFAULT 'paper_polish_enhance'"))
                    conn.commit()
                    print("  ✓ 添加字段: optimization_sessions.processing_mode")
                
                if "emotion_model" not in columns:
                    conn.execute(text("ALTER TABLE optimization_sessions ADD COLUMN emotion_model VARCHAR(100)"))
                    conn.execute(text("ALTER TABLE optimization_sessions ADD COLUMN emotion_api_key VARCHAR(255)"))
                    conn.execute(text("ALTER TABLE optimization_sessions ADD COLUMN emotion_base_url VARCHAR(255)"))
                    conn.commit()
                    print("  ✓ 添加字段: optimization_sessions.emotion_* 字段")
            
            # 迁移 users 表
            if "users" in tables:
                user_columns = {column["name"] for column in inspector.get_columns("users")}
                
                if "usage_limit" not in user_columns:
                    conn.execute(text(f"ALTER TABLE users ADD COLUMN usage_limit INTEGER DEFAULT {settings.DEFAULT_USAGE_LIMIT}"))
                    conn.commit()
                    print("  ✓ 添加字段: users.usage_limit")
                
                if "usage_count" not in user_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN usage_count INTEGER DEFAULT 0"))
                    conn.commit()
                    print("  ✓ 添加字段: users.usage_count")
                
                # 更新 NULL 值
                conn.execute(text(f"UPDATE users SET usage_limit = {settings.DEFAULT_USAGE_LIMIT} WHERE usage_limit IS NULL"))
                conn.execute(text("UPDATE users SET usage_count = 0 WHERE usage_count IS NULL"))
                conn.commit()
            
            # 迁移 optimization_segments 表
            if "optimization_segments" in tables:
                segment_columns = {column["name"] for column in inspector.get_columns("optimization_segments")}
                
                if "is_title" not in segment_columns:
                    conn.execute(text("ALTER TABLE optimization_segments ADD COLUMN is_title BOOLEAN DEFAULT 0"))
                    conn.commit()
                    print("  ✓ 添加字段: optimization_segments.is_title")
            
            # 迁移 custom_prompts 表
            if "custom_prompts" in tables:
                prompt_columns = {column["name"] for column in inspector.get_columns("custom_prompts")}
                
                if "is_system" not in prompt_columns:
                    conn.execute(text("ALTER TABLE custom_prompts ADD COLUMN is_system BOOLEAN DEFAULT 0"))
                    conn.commit()
                    print("  ✓ 添加字段: custom_prompts.is_system")
                
                if "is_active" not in prompt_columns:
                    conn.execute(text("ALTER TABLE custom_prompts ADD COLUMN is_active BOOLEAN DEFAULT 1"))
                    conn.commit()
                    print("  ✓ 添加字段: custom_prompts.is_active")
    
    except Exception as e:
        print(f"  ⚠ 数据库迁移警告: {str(e)}")
        # 迁移失败不应该阻止应用启动
