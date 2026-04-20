"""债务优化器 API 路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.debt_optimizer.models import DebtOptimizationRequest, DebtOptimizationResponse
from backend.debt_optimizer.engine import DebtOptimizerEngine
from backend.database.session import get_db
from backend.database.models import DebtProfile

router = APIRouter()
engine = DebtOptimizerEngine()


@router.post("/optimize", response_model=DebtOptimizationResponse)
async def optimize_debt(request: DebtOptimizationRequest, db: Session = Depends(get_db)):
    """分析债务结构并生成优化还款计划"""
    result = engine.optimize(request)

    db_record = DebtProfile(
        user_id=request.user_id,
        strategy=request.strategy.value,
        total_debt=result.total_debt,
        monthly_minimum=result.monthly_minimum,
        estimated_payoff_months=result.estimated_payoff_months,
        total_interest_saved=result.total_interest_saved,
        debts=[d.model_dump() for d in request.debts],
        payment_schedule=[s.model_dump() for s in result.payment_schedule[:24]],  # store first 24 months
        negotiation_templates=[t.model_dump() for t in result.negotiation_templates],
    )
    db.add(db_record)
    db.commit()

    return result


@router.get("/profile/{user_id}")
async def get_debt_profile(user_id: str, db: Session = Depends(get_db)):
    """获取用户最新债务档案"""
    profile = db.query(DebtProfile).filter_by(user_id=user_id).order_by(DebtProfile.created_at.desc()).first()
    if not profile:
        return {"detail": "No debt profile found"}
    return {
        "total_debt": profile.total_debt,
        "strategy": profile.strategy,
        "estimated_payoff_months": profile.estimated_payoff_months,
        "interest_saved": profile.total_interest_saved,
        "created_at": profile.created_at.isoformat(),
    }
