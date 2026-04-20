"""
数据库会话配置
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from .models import Base

# 数据库配置
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./emobridge.db"  # 默认使用SQLite
)

# 创建数据库引擎
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """初始化数据库"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 创建默认配置
    from .models import SystemConfig
    from sqlalchemy.orm import Session
    
    db = SessionLocal()
    try:
        # 检查是否已经存在系统配置
        if not db.query(SystemConfig).filter(SystemConfig.config_key == "emotion_recognition.enabled").first():
            # 启用情感识别
            db.add(SystemConfig(
                config_key="emotion_recognition.enabled",
                config_value=True,
                description="情感识别功能开关"
            ))
        
        if not db.query(SystemConfig).filter(SystemConfig.config_key == "multimodal_detection.threshold").first():
            # 设置多模态检测阈值
            db.add(SystemConfig(
                config_key="multimodal_detection.threshold",
                config_value=0.75,
                description="多模态检测置信度阈值"
            ))
        
        if not db.query(SystemConfig).filter(SystemConfig.config_key == "digital_twin.auto_update").first():
            # 启用数字孪生自动更新
            db.add(SystemConfig(
                config_key="digital_twin.auto_update",
                config_value=True,
                description="数字孪生自动更新开关"
            ))
        
        db.commit()
        print("数据库初始化完成")
        
    except Exception as e:
        db.rollback()
        print(f"数据库初始化失败: {e}")
    finally:
        db.close()

def drop_db():
    """删除数据库（仅用于开发）"""
    Base.metadata.drop_all(bind=engine)
    print("数据库已删除")

def backup_db():
    """备份数据库"""
    if "sqlite" in DATABASE_URL:
        import shutil
        from datetime import datetime
        
        db_path = DATABASE_URL.replace("sqlite:///", "")
        backup_path = f"backup_emobridge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        try:
            shutil.copy2(db_path, backup_path)
            print(f"数据库已备份到: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"备份失败: {e}")
            return None
    else:
        print("仅支持SQLite数据库备份")
        return None

def restore_db(backup_path: str):
    """从备份恢复数据库"""
    if "sqlite" in DATABASE_URL:
        import shutil
        
        db_path = DATABASE_URL.replace("sqlite:///", "")
        
        try:
            shutil.copy2(backup_path, db_path)
            print(f"数据库已从 {backup_path} 恢复")
            return True
        except Exception as e:
            print(f"恢复失败: {e}")
            return False
    else:
        print("仅支持SQLite数据库恢复")
        return False