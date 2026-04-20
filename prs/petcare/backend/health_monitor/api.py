"""
Health Monitor - REST API endpoints.
"""
from datetime import datetime, date
from uuid import UUID
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from backend.database.session import get_db
from backend.database.models import Pet, ActivityLog, DietLog
from backend.health_monitor.models import (
    CameraAnalysisRequest, CameraAnalysisResponse,
    SoundAnalysisRequest, SoundAnalysisResponse,
    ActivityLogRequest, ActivitySummary,
    DietLogRequest, DietSummary, HealthOverview,
    BehaviorDetection, SoundEvent,
)
from backend.health_monitor.engine import camera_engine, sound_engine, activity_tracker, diet_monitor

router = APIRouter()


async def _get_pet_or_404(db: AsyncSession, pet_id: UUID):
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = result.scalar_one_or_none()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


def _row_to_dict(row):
    return {c.name: getattr(row, c.name) for c in row.__table__.columns}


def _estimate_calorie_target(pet) -> float:
    if not pet.weight:
        return 800.0
    rer = 70 * (pet.weight ** 0.75)
    return round(rer * 1.6, 1)


@router.post("/camera/analyze", response_model=CameraAnalysisResponse)
async def analyze_camera_image(request: CameraAnalysisRequest, db: AsyncSession = Depends(get_db)):
    """Analyze pet image for behavior, body condition, and anomalies."""
    pet = await _get_pet_or_404(db, request.pet_id)
    analysis = await camera_engine.analyze_image(request.image_data, pet.pet_type.value)
    return CameraAnalysisResponse(
        pet_id=request.pet_id, analysis_id=analysis["analysis_id"],
        timestamp=request.timestamp or datetime.utcnow(),
        behaviors=[BehaviorDetection(**b) for b in analysis["behaviors"]],
        body_condition_score=analysis["body_condition_score"],
        posture_quality=analysis["posture_quality"],
        coat_condition=analysis["coat_condition"],
        anomalies_detected=analysis["anomalies_detected"],
    )


@router.post("/sound/analyze", response_model=SoundAnalysisResponse)
async def analyze_sound(request: SoundAnalysisRequest, db: AsyncSession = Depends(get_db)):
    """Analyze pet audio for health indicators."""
    pet = await _get_pet_or_404(db, request.pet_id)
    analysis = await sound_engine.analyze_audio(request.audio_data, request.duration_seconds, pet.pet_type.value)
    return SoundAnalysisResponse(
        pet_id=request.pet_id, analysis_id=analysis["analysis_id"],
        timestamp=request.timestamp or datetime.utcnow(),
        events=[SoundEvent(**e) for e in analysis["events"]],
        overall_stress_level=analysis["overall_stress_level"],
        respiratory_pattern=analysis["respiratory_pattern"],
        health_indicators=analysis["health_indicators"],
    )


@router.post("/activity/log")
async def log_activity(request: ActivityLogRequest, db: AsyncSession = Depends(get_db)):
    """Log a pet activity event."""
    await _get_pet_or_404(db, request.pet_id)
    log = ActivityLog(
        pet_id=request.pet_id, activity_type=request.activity_type,
        duration_minutes=request.duration_minutes, distance_meters=request.distance_meters,
        calories_burned=request.calories_burned, heart_rate=request.heart_rate,
        steps=request.steps, recorded_at=request.timestamp or datetime.utcnow(),
    )
    db.add(log)
    await db.commit()
    return {"id": str(log.id), "status": "logged"}


@router.get("/activity/summary/{pet_id}", response_model=ActivitySummary)
async def get_activity_summary(
    pet_id: UUID, target_date: Optional[date] = Query(None), db: AsyncSession = Depends(get_db),
):
    """Get daily activity summary for a pet."""
    await _get_pet_or_404(db, pet_id)
    query_date = target_date or date.today()
    start, end = datetime.combine(query_date, datetime.min.time()), datetime.combine(query_date, datetime.max.time())
    stmt = select(ActivityLog).where(and_(ActivityLog.pet_id == pet_id, ActivityLog.recorded_at >= start, ActivityLog.recorded_at <= end))
    result = await db.execute(stmt)
    logs = [_row_to_dict(log) for log in result.scalars().all()]
    summary = activity_tracker.calculate_daily_summary(logs)
    return ActivitySummary(pet_id=pet_id, date=query_date.isoformat(), **summary)


@router.post("/diet/log")
async def log_diet(request: DietLogRequest, db: AsyncSession = Depends(get_db)):
    """Log a pet diet event."""
    await _get_pet_or_404(db, request.pet_id)
    log = DietLog(
        pet_id=request.pet_id, meal_type=request.meal_type, food_name=request.food_name,
        food_brand=request.food_brand, amount_grams=request.amount_grams, calories=request.calories,
        protein=request.protein, fat=request.fat, carbs=request.carbs,
        water_intake_ml=request.water_intake_ml, logged_at=request.timestamp or datetime.utcnow(),
    )
    db.add(log)
    await db.commit()
    return {"id": str(log.id), "status": "logged"}


@router.get("/diet/summary/{pet_id}", response_model=DietSummary)
async def get_diet_summary(
    pet_id: UUID, target_date: Optional[date] = Query(None), db: AsyncSession = Depends(get_db),
):
    """Get daily diet/nutrition summary for a pet."""
    pet = await _get_pet_or_404(db, pet_id)
    query_date = target_date or date.today()
    start, end = datetime.combine(query_date, datetime.min.time()), datetime.combine(query_date, datetime.max.time())
    stmt = select(DietLog).where(and_(DietLog.pet_id == pet_id, DietLog.logged_at >= start, DietLog.logged_at <= end))
    result = await db.execute(stmt)
    logs = [_row_to_dict(log) for log in result.scalars().all()]
    summary = diet_monitor.calculate_daily_summary(logs, {"daily_calorie_target": _estimate_calorie_target(pet)})
    return DietSummary(pet_id=pet_id, date=query_date.isoformat(), **summary)


@router.get("/overview/{pet_id}", response_model=HealthOverview)
async def get_health_overview(pet_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get comprehensive health overview for a pet."""
    await _get_pet_or_404(db, pet_id)
    today = date.today()
    start, end = datetime.combine(today, datetime.min.time()), datetime.combine(today, datetime.max.time())

    act_result = await db.execute(select(ActivityLog).where(and_(ActivityLog.pet_id == pet_id, ActivityLog.recorded_at >= start, ActivityLog.recorded_at <= end)))
    act_logs = [_row_to_dict(l) for l in act_result.scalars().all()]
    act_summary = activity_tracker.calculate_daily_summary(act_logs)

    pet = await _get_pet_or_404(db, pet_id)
    diet_result = await db.execute(select(DietLog).where(and_(DietLog.pet_id == pet_id, DietLog.logged_at >= start, DietLog.logged_at <= end)))
    diet_logs = [_row_to_dict(l) for l in diet_result.scalars().all()]
    diet_summary = diet_monitor.calculate_daily_summary(diet_logs, {"daily_calorie_target": _estimate_calorie_target(pet)})

    act_score = min(act_summary["total_duration_minutes"] / 90.0, 1.0)
    diet_score = diet_summary["nutritional_balance_score"]
    overall = round((act_score * 0.4 + diet_score * 0.3 + 0.3), 2)

    recommendations = []
    if act_score < 0.5:
        recommendations.append("Increase daily activity - aim for at least 60 minutes")
    if diet_score < 0.5:
        recommendations.append("Improve nutritional balance - consult nutrition guide")

    return HealthOverview(
        pet_id=pet_id, overall_health_score=overall, behavior_health=0.7,
        diet_health=diet_score, activity_health=act_score,
        recommendations=recommendations, last_updated=datetime.utcnow(),
    )
