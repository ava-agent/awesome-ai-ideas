"""情感支持 API 路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.emotional_support.models import MoodCheckIn, SupportResponse
from backend.emotional_support.engine import EmotionalSupportEngine
from backend.database.session import get_db
from backend.database.models import SupportSession as SupportSessionModel

router = APIRouter()
engine = EmotionalSupportEngine()


@router.post("/check-in", response_model=SupportResponse)
async def mood_check_in(check_in: MoodCheckIn, db: Session = Depends(get_db)):
    """提交心情签到，获取个性化情感支持"""
    result = engine.process_check_in(check_in)

    db_record = SupportSessionModel(
        user_id=check_in.user_id,
        stress_level=check_in.stress_level,
        mood_tag=check_in.mood_tag,
        session_type=result.recommended_exercise.get("type", "general") if result.recommended_exercise else "general",
        session_data=result.recommended_exercise or {},
        ai_response=result.validation_message,
        follow_up_needed=result.follow_up_days,
    )
    db.add(db_record)
    db.commit()

    return result


@router.get("/history/{user_id}")
async def get_support_history(user_id: str, db: Session = Depends(get_db)):
    """获取情感支持历史记录"""
    sessions = db.query(SupportSessionModel).filter_by(user_id=user_id).order_by(SupportSessionModel.created_at.desc()).limit(20).all()
    return [
        {"date": s.created_at.isoformat(), "stress_level": s.stress_level, "mood": s.mood_tag, "exercise": s.session_type}
        for s in sessions
    ]


@router.get("/exercises")
async def list_exercises():
    """获取所有可用的练习"""
    return {
        "breathing": [
            {"name": "4-7-8 呼吸法", "pattern": "4-7-8", "description": "快速缓解焦虑"},
            {"name": "箱式呼吸", "pattern": "4-4-4-4", "description": "保持冷静和专注"},
        ],
        "grounding": [
            {"name": "5-4-3-2-1 接地法", "description": "减少焦虑，回到当下"},
        ],
        "mindfulness": [
            {"name": "身体扫描冥想", "duration": 10, "description": "放松身体各部位"},
        ],
    }
