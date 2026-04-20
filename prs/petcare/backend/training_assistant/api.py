"""
Training Assistant - REST API endpoints.
"""
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.database.session import get_db
from backend.database.models import Pet, TrainingSession
from backend.training_assistant.models import (
    TrainingPlanRequest, TrainingPlanResponse, TrainingLogRequest, TrainingLogResponse,
    TrainingProgressResponse, RealTimeGuidanceRequest, RealTimeGuidanceResponse,
    TrainingSessionPlan, TrainingSessionStep, GuidanceFeedback,
)
from backend.training_assistant.engine import plan_generator, progress_tracker, guidance_engine

router = APIRouter()


@router.post("/plan", response_model=TrainingPlanResponse)
async def create_training_plan(request: TrainingPlanRequest, db: AsyncSession = Depends(get_db)):
    """Generate a personalized training plan for a pet."""
    result = await db.execute(select(Pet).where(Pet.id == request.pet_id))
    pet = result.scalar_one_or_none()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    plan = plan_generator.generate_plan(
        goals=request.goals, breed=pet.breed, current_level=request.current_level,
        daily_time_budget=request.daily_time_budget_minutes, preferred_style=request.preferred_style,
    )

    return TrainingPlanResponse(
        pet_id=request.pet_id, plan_id=plan["plan_id"], created_at=plan["created_at"],
        goals=plan["goals"],
        weekly_schedule=[TrainingSessionPlan(**s) for s in plan["weekly_schedule"]],
        milestones=plan["milestones"],
        estimated_completion_weeks=plan["estimated_completion_weeks"],
        tips=plan["tips"],
    )


@router.post("/log", response_model=TrainingLogResponse)
async def log_training_session(request: TrainingLogRequest, db: AsyncSession = Depends(get_db)):
    """Log a completed training session."""
    result = await db.execute(select(Pet).where(Pet.id == request.pet_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Pet not found")

    session = TrainingSession(
        pet_id=request.pet_id, plan_id=request.plan_id, skill_name=request.skill_name,
        duration_minutes=request.duration_minutes, success_rating=request.success_rating,
        notes=request.notes, improvements=request.improvements, video_url=request.video_url,
        completed_at=datetime.utcnow(),
    )
    db.add(session)
    await db.commit()

    result = progress_tracker.log_session(
        skill_name=request.skill_name, success_rating=request.success_rating,
        duration_minutes=request.duration_minutes, notes=request.notes,
    )

    return TrainingLogResponse(
        log_id=result["log_id"], pet_id=request.pet_id, skill_name=request.skill_name,
        success_rating=request.success_rating, feedback=result["feedback"],
        next_steps=result["next_steps"],
    )


@router.get("/progress/{pet_id}", response_model=TrainingProgressResponse)
async def get_training_progress(pet_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get training progress for a pet."""
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Pet not found")

    sessions_result = await db.execute(
        select(TrainingSession).where(TrainingSession.pet_id == pet_id).order_by(TrainingSession.completed_at)
    )
    sessions = sessions_result.scalars().all()

    skills_done: dict = {}
    total_hours = 0.0
    for s in sessions:
        if s.skill_name not in skills_done:
            skills_done[s.skill_name] = {"count": 0, "total_rating": 0.0, "total_duration": 0}
        skills_done[s.skill_name]["count"] += 1
        skills_done[s.skill_name]["total_rating"] += (s.success_rating or 0)
        skills_done[s.skill_name]["total_duration"] += (s.duration_minutes or 0)
        total_hours += (s.duration_minutes or 0) / 60.0

    mastered = [name for name, data in skills_done.items() if data["count"] >= 5 and data["total_rating"] / data["count"] >= 0.8]
    in_progress = [{"name": name, "sessions": data["count"],
                    "avg_rating": round(data["total_rating"] / data["count"], 2)}
                   for name, data in skills_done.items() if name not in mastered]
    overall = len(mastered) / max(len(mastered) + len(in_progress), 1)

    return TrainingProgressResponse(
        pet_id=pet_id, overall_progress=round(overall, 2),
        skills_mastered=mastered, skills_in_progress=in_progress,
        skills_locked=["advanced_skills"], consistency_score=0.7, streak_days=len(set(
            s.completed_at.date() for s in sessions if s.completed_at
        )),
        total_training_hours=round(total_hours, 1),
        weekly_progress=[{"week": 1, "progress": overall}],
    )


@router.post("/guidance", response_model=RealTimeGuidanceResponse)
async def get_real_time_guidance(request: RealTimeGuidanceRequest):
    """Get real-time training guidance for current step."""
    result = guidance_engine.analyze_step(
        skill=request.current_skill, step=request.current_step, description=request.description,
    )
    return RealTimeGuidanceResponse(
        pet_id=request.pet_id, skill=request.current_skill,
        feedback=[GuidanceFeedback(**f) for f in result["feedback"]],
        overall_session_rating=result["overall_session_rating"],
        session_summary=result["session_summary"],
    )
