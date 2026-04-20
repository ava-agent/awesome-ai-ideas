"""危机分析器数据模型"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRISIS = "crisis"


class FinancialSnapshot(BaseModel):
    monthly_income: float = Field(..., ge=0, description="月收入")
    monthly_expenses: float = Field(..., ge=0, description="月支出")
    total_savings: float = Field(0, ge=0, description="总储蓄")
    total_debt: float = Field(0, ge=0, description="总负债")
    monthly_debt_payments: float = Field(0, ge=0, description="月债务还款")
    employment_status: str = Field("employed", description="就业状态")
    dependents: int = Field(0, ge=0, description="受抚养人数")
    insurance_coverage: bool = Field(False, description="是否有保险")
    recent_life_events: list[str] = Field(default_factory=list, description="近期生活事件")


class CrisisAssessmentRequest(BaseModel):
    user_id: str
    snapshot: FinancialSnapshot


class ActionPlan(BaseModel):
    timeline_months: int
    title: str
    priorities: list[str]
    estimated_savings: float = 0
    milestones: list[dict] = Field(default_factory=list)


class CrisisAssessmentResponse(BaseModel):
    assessment_id: str
    severity: SeverityLevel
    cash_flow_score: float
    debt_burden_score: float
    savings_buffer_months: float
    risk_factors: list[str]
    strengths: list[str]
    action_plan_3m: ActionPlan
    action_plan_6m: ActionPlan
    action_plan_9m: ActionPlan
    ai_analysis: str
