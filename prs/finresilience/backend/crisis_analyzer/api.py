"""危机分析器 API 路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.crisis_analyzer.models import CrisisAssessmentRequest, CrisisAssessmentResponse
from backend.crisis_analyzer.engine import CrisisAnalyzerEngine
from backend.database.session import get_db
from backend.database.models import CrisisAssessment as CrisisAssessmentModel

router = APIRouter()
engine = CrisisAnalyzerEngine()


@router.post("/assess", response_model=CrisisAssessmentResponse)
async def create_assessment(request: CrisisAssessmentRequest, db: Session = Depends(get_db)):
    """执行财务危机评估，生成个性化行动计划"""
    result = engine.analyze(request.snapshot)

    # 保存到数据库
    db_record = CrisisAssessmentModel(
        user_id=request.user_id,
        severity_level=result.severity.value,
        cash_flow_score=result.cash_flow_score,
        debt_burden_score=result.debt_burden_score,
        savings_buffer_months=result.savings_buffer_months,
        risk_factors=result.risk_factors,
        strengths=result.strengths,
        action_plan_3m=result.action_plan_3m.model_dump(),
        action_plan_6m=result.action_plan_6m.model_dump(),
        action_plan_9m=result.action_plan_9m.model_dump(),
        ai_analysis=result.ai_analysis,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return result


@router.get("/history/{user_id}")
async def get_assessment_history(user_id: str, db: Session = Depends(get_db)):
    """获取用户历史评估记录"""
    records = db.query(CrisisAssessmentModel).filter_by(user_id=user_id).order_by(CrisisAssessmentModel.created_at.desc()).limit(10).all()
    return [{"id": r.id, "severity": r.severity_level, "created_at": r.created_at.isoformat()} for r in records]
