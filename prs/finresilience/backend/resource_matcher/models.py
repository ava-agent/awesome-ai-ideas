"""资源匹配器数据模型"""
from pydantic import BaseModel, Field
from typing import Optional


class UserProfile(BaseModel):
    user_id: str
    city: str
    state: str
    household_size: int = 1
    monthly_income: float = 0.0
    employment_status: str = "unknown"
    has_children: bool = False
    is_veteran: bool = False
    is_disabled: bool = False
    age: Optional[int] = None


class ResourceItem(BaseModel):
    name: str
    category: str  # housing/food/employment/healthcare/utility/legal
    provider: str
    description: str
    eligibility: list[str]
    benefit_value: float = 0.0
    benefit_period: str = "monthly"
    application_url: str = ""
    phone: str = ""
    address: str = ""
    documents_required: list[str] = []
    processing_time: str = ""
    match_score: float = 0.0


class ResourceMatchRequest(BaseModel):
    user: UserProfile
    categories: list[str] = Field(default_factory=list, description="过滤类别，空则全部")
