"""情感支持数据模型"""
from pydantic import BaseModel, Field
from typing import Optional


class MoodCheckIn(BaseModel):
    user_id: str
    stress_level: int = Field(..., ge=1, le=10)
    mood_tag: str = Field("", description="当前心情标签")
    main_concern: str = Field("", description="主要困扰")
    need_immediate_help: bool = False


class CBTExercise(BaseModel):
    exercise_id: str
    title: str
    description: str
    steps: list[str]
    duration_minutes: int = 10


class BreathingExercise(BaseModel):
    exercise_id: str
    name: str
    pattern: str  # e.g. "4-7-8"
    description: str
    steps: list[str]


class SupportResponse(BaseModel):
    session_id: str
    validation_message: str
    coping_strategies: list[str]
    recommended_exercise: Optional[dict] = None
    follow_up_days: int = 3
    resources: list[str] = []
    crisis_hotline: Optional[str] = None
