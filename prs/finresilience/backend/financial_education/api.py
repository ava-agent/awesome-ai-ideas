"""财务教育 API 路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.financial_education.models import AssessmentRequest, ProgressResponse
from backend.financial_education.engine import EducationEngine
from backend.database.session import get_db
from backend.database.models import EducationProgress

router = APIRouter()
engine = EducationEngine()


@router.get("/modules")
async def list_modules(level: str = None):
    """获取学习模块列表"""
    modules = engine.get_modules(level)
    return [{"id": m.module_id, "title": m.title, "level": m.level, "description": m.description, "minutes": m.estimated_minutes} for m in modules]


@router.get("/modules/{module_id}")
async def get_module(module_id: str):
    """获取模块详情"""
    module = engine.get_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module.model_dump()


@router.post("/assess", response_model=ProgressResponse)
async def assess_user_level(request: AssessmentRequest, db: Session = Depends(get_db)):
    """评估用户财务知识水平并推荐学习路径"""
    result = engine.assess_level(request)

    db_record = EducationProgress(
        user_id=request.user_id,
        current_level=result.current_level,
        quiz_scores=result.quiz_scores,
        learning_path=[{"module_id": result.next_module, "status": "recommended"}] if result.next_module else [],
    )
    db.add(db_record)
    db.commit()

    return result
