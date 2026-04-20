"""FinResilience AI - FastAPI 主入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.crisis_analyzer.api import router as crisis_router
from backend.debt_optimizer.api import router as debt_router
from backend.resource_matcher.api import router as resource_router
from backend.financial_education.api import router as education_router
from backend.emotional_support.api import router as support_router
from backend.database.session import engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinResilience AI",
    description="AI驱动的财务韧性平台 - 为面临经济困难的人群提供全方位支持",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crisis_router, prefix="/api/v1/crisis", tags=["危机分析"])
app.include_router(debt_router, prefix="/api/v1/debt", tags=["债务优化"])
app.include_router(resource_router, prefix="/api/v1/resources", tags=["资源匹配"])
app.include_router(education_router, prefix="/api/v1/education", tags=["财务教育"])
app.include_router(support_router, prefix="/api/v1/support", tags=["情感支持"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FinResilience AI"}


@app.get("/")
async def root():
    return {
        "service": "FinResilience AI",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "path": str(request.url)},
    )
