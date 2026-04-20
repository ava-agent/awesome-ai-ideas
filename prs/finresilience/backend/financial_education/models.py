"""财务教育数据模型"""
from pydantic import BaseModel, Field
from typing import Optional


class QuizQuestion(BaseModel):
    question_id: str
    question: str
    options: list[str]
    correct_answer: int
    explanation: str


class LearningModule(BaseModel):
    module_id: str
    title: str
    level: str  # beginner/intermediate/advanced
    description: str
    content: str
    estimated_minutes: int = 15
    quiz: list[QuizQuestion] = Field(default_factory=list)


class AssessmentRequest(BaseModel):
    user_id: str
    answers: list[dict]  # [{question_id, answer_index}]


class ProgressResponse(BaseModel):
    user_id: str
    current_level: str
    completed_modules: list[str]
    next_module: Optional[str]
    streak_days: int
    quiz_scores: list[dict]
