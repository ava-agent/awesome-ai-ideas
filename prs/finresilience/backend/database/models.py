"""SQLAlchemy 数据模型"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, JSON, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.session import Base


def _utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    display_name = Column(String(100))
    location_city = Column(String(100))
    location_state = Column(String(100))
    household_size = Column(Integer, default=1)
    monthly_income = Column(Float, default=0.0)
    monthly_expenses = Column(Float, default=0.0)
    total_assets = Column(Float, default=0.0)
    total_liabilities = Column(Float, default=0.0)
    risk_profile = Column(String(20), default="unknown")  # low/medium/high/crisis
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)

    # relationships
    crisis_assessments = relationship("CrisisAssessment", back_populates="user")
    debt_profiles = relationship("DebtProfile", back_populates="user")
    resource_matches = relationship("ResourceMatch", back_populates="user")
    education_progress = relationship("EducationProgress", back_populates="user")
    support_sessions = relationship("SupportSession", back_populates="user")


class CrisisAssessment(Base):
    __tablename__ = "crisis_assessments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    severity_level = Column(String(20), nullable=False)  # low/medium/high/crisis
    cash_flow_score = Column(Float, default=0.0)
    debt_burden_score = Column(Float, default=0.0)
    savings_buffer_months = Column(Float, default=0.0)
    risk_factors = Column(JSON, default=list)
    strengths = Column(JSON, default=list)
    action_plan_3m = Column(JSON, default=dict)
    action_plan_6m = Column(JSON, default=dict)
    action_plan_9m = Column(JSON, default=dict)
    ai_analysis = Column(Text)
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    user = relationship("User", back_populates="crisis_assessments")


class DebtProfile(Base):
    __tablename__ = "debt_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    strategy = Column(String(30), default="avalanche")  # avalanche/snowball/custom
    total_debt = Column(Float, default=0.0)
    monthly_minimum = Column(Float, default=0.0)
    estimated_payoff_months = Column(Integer, default=0)
    total_interest_saved = Column(Float, default=0.0)
    debts = Column(JSON, default=list)
    payment_schedule = Column(JSON, default=list)
    negotiation_templates = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)

    user = relationship("User", back_populates="debt_profiles")


class ResourceMatch(Base):
    __tablename__ = "resource_matches"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    category = Column(String(50))  # housing/food/employment/healthcare/utility
    resources = Column(JSON, default=list)
    application_status = Column(JSON, default=list)
    total_monthly_value = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    user = relationship("User", back_populates="resource_matches")


class EducationProgress(Base):
    __tablename__ = "education_progress"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    current_level = Column(String(20), default="beginner")  # beginner/intermediate/advanced
    completed_modules = Column(JSON, default=list)
    quiz_scores = Column(JSON, default=list)
    learning_path = Column(JSON, default=list)
    streak_days = Column(Integer, default=0)
    last_activity = Column(DateTime(timezone=True), default=_utcnow)
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    user = relationship("User", back_populates="education_progress")


class SupportSession(Base):
    __tablename__ = "support_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    stress_level = Column(Integer, default=5)  # 1-10
    mood_tag = Column(String(30))
    session_type = Column(String(30))  # cbt/meditation/breathing/community
    session_data = Column(JSON, default=dict)
    ai_response = Column(Text)
    follow_up_needed = Column(Integer, default=0)  # days until follow-up
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    user = relationship("User", back_populates="support_sessions")
