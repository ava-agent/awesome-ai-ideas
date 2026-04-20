"""债务优化器数据模型"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class DebtType(str, Enum):
    CREDIT_CARD = "credit_card"
    STUDENT_LOAN = "student_loan"
    MEDICAL = "medical"
    PERSONAL_LOAN = "personal_loan"
    MORTGAGE = "mortgage"
    AUTO_LOAN = "auto_loan"
    PAYDAY_LOAN = "payday_loan"
    OTHER = "other"


class DebtItem(BaseModel):
    name: str
    debt_type: DebtType
    balance: float = Field(..., gt=0)
    interest_rate: float = Field(..., ge=0)
    minimum_payment: float = Field(..., gt=0)
    due_date: int = Field(1, ge=1, le=31)
    creditor: str = ""
    is_collection: bool = False


class DebtStrategy(str, Enum):
    AVALANCHE = "avalanche"   # 高息优先
    SNOWBALL = "snowball"     # 小额优先
    CUSTOM = "custom"


class DebtOptimizationRequest(BaseModel):
    user_id: str
    debts: list[DebtItem]
    strategy: DebtStrategy = DebtStrategy.AVALANCHE
    available_monthly: float = Field(..., ge=0)


class PaymentStep(BaseModel):
    month: int
    payments: list[dict]  # [{name, amount, remaining}]
    total_paid: float
    total_remaining: float


class NegotiationTemplate(BaseModel):
    creditor: str
    debt_type: str
    template_subject: str
    template_body: str
    tips: list[str]


class DebtOptimizationResponse(BaseModel):
    optimization_id: str
    strategy_used: DebtStrategy
    total_debt: float
    monthly_minimum: float
    extra_payment: float
    estimated_payoff_months: int
    total_interest: float
    total_interest_saved: float
    payment_schedule: list[PaymentStep]
    negotiation_templates: list[NegotiationTemplate]
    recommendations: list[str]
