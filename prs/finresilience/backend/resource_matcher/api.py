"""资源匹配器 API 路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.resource_matcher.models import ResourceMatchRequest
from backend.resource_matcher.engine import ResourceMatcherEngine
from backend.database.session import get_db
from backend.database.models import ResourceMatch as ResourceMatchModel

router = APIRouter()
engine = ResourceMatcherEngine()


@router.post("/match")
async def match_resources(request: ResourceMatchRequest, db: Session = Depends(get_db)):
    """基于用户画像匹配最适合的援助资源"""
    results = engine.match(request)

    total_value = sum(r.benefit_value for r in results if r.benefit_period == "monthly")

    db_record = ResourceMatchModel(
        user_id=request.user.user_id,
        category=",".join(set(r.category for r in results)),
        resources=[r.model_dump() for r in results],
        total_monthly_value=total_value,
    )
    db.add(db_record)
    db.commit()

    return {
        "total_matches": len(results),
        "estimated_monthly_value": round(total_value, 2),
        "resources": [r.model_dump() for r in results],
    }


@router.get("/categories")
async def list_categories():
    """获取所有资源类别"""
    return {"categories": ["housing", "food", "employment", "healthcare", "utility", "legal"]}
