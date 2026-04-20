"""
Training Assistant - Pydantic models.
"""
from datetime import datetime, date
from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class TrainingPlanRequest(BaseModel):
    pet_id: UUID
    goals: List[str] = Field(..., min_length=1)
    current_level: str = Field(default="beginner")
    daily_time_budget_minutes: int = Field(default=15, ge=5, le=120)
    preferred_style: str = Field(default="positive_reinforcement")


class TrainingSessionStep(BaseModel):
    step_number: int
    action: str
    duration_seconds: int
    description: str
    tips: List[str] = Field(default_factory=list)
    success_criteria: str


class TrainingSessionPlan(BaseModel):
    session_id: str
    skill_name: str
    difficulty: str
    estimated_duration_minutes: int
    steps: List[TrainingSessionStep]
    equipment_needed: List[str] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)


class TrainingPlanResponse(BaseModel):
    pet_id: UUID
    plan_id: str
    created_at: datetime
    goals: List[str]
    weekly_schedule: List[TrainingSessionPlan]
    milestones: List[Dict[str, Any]]
    estimated_completion_weeks: int
    tips: List[str]


class TrainingLogRequest(BaseModel):
    pet_id: UUID
    plan_id: Optional[UUID] = None
    skill_name: str
    duration_minutes: int = Field(gt=0)
    success_rating: float = Field(ge=0.0, le=1.0)
    notes: Optional[str] = None
    improvements: Optional[str] = None
    video_url: Optional[str] = None


class TrainingLogResponse(BaseModel):
    log_id: str
    pet_id: UUID
    skill_name: str
    success_rating: float
    feedback: str
    next_steps: List[str]


class TrainingProgressResponse(BaseModel):
    pet_id: UUID
    overall_progress: float = Field(ge=0.0, le=1.0)
    skills_mastered: List[str]
    skills_in_progress: List[Dict[str, Any]]
    skills_locked: List[str]
    consistency_score: float = Field(ge=0.0, le=1.0)
    streak_days: int
    total_training_hours: float
    weekly_progress: List[Dict[str, float]]


class RealTimeGuidanceRequest(BaseModel):
    pet_id: UUID
    current_skill: str
    current_step: int
    image_data: Optional[str] = None
    description: Optional[str] = None


class GuidanceFeedback(BaseModel):
    step_number: int
    is_correct: bool
    confidence: float = Field(ge=0.0, le=1.0)
    feedback_text: str
    correction_hint: Optional[str] = None
    encouragement: Optional[str] = None
    suggested_next_action: Optional[str] = None


class RealTimeGuidanceResponse(BaseModel):
    pet_id: UUID
    skill: str
    feedback: List[GuidanceFeedback]
    overall_session_rating: float
    session_summary: str
