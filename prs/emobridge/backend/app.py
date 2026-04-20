"""
EmoBridge - AI情感识别康复平台
主应用入口
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
from datetime import datetime

# 导入模块
from emotion_recognition.api import emotion_router
from digital_twin.api import twin_router
from therapy_environment.api import therapy_router
from database.session import engine, Base
from database.models import Patient, Therapist, TreatmentSession

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('emobridge.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="EmoBridge AI情感识别康复平台",
    description="专为康复治疗师设计的AI驱动的情感识别和精准康复平台",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册路由
app.include_router(emotion_router, prefix="/api/emotion", tags=["情感识别"])
app.include_router(twin_router, prefix="/api/twin", tags=["数字孪生"])
app.include_router(therapy_router, prefix="/api/therapy", tags=["治疗环境"])

@app.on_event("startup")
async def startup_event():
    """启动时初始化数据库"""
    logger.info("启动EmoBridge平台...")
    
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    
    logger.info("数据库初始化完成")
    logger.info(f"服务启动时间: {datetime.now().isoformat()}")

@app.on_event("shutdown")
async def shutdown_event():
    """关闭时清理资源"""
    logger.info("正在关闭EmoBridge平台...")
    logger.info("服务已安全关闭")

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用EmoBridge AI情感识别康复平台",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "EmoBridge"
    }

@app.get("/api/status")
async def platform_status():
    """平台状态"""
    try:
        # 这里可以添加更详细的状态检查
        return {
            "status": "operational",
            "components": {
                "emotion_recognition": "active",
                "digital_twin": "active", 
                "therapy_environment": "active",
                "database": "connected"
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"状态检查失败: {e}")
        raise HTTPException(status_code=500, detail="平台状态检查失败")

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )