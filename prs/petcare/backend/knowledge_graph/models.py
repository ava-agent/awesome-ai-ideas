"""
Knowledge Graph - Pydantic models for veterinary knowledge graph.
"""
from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SymptomCheckRequest(BaseModel):
    pet_id: UUID
    symptoms: List[str] = Field(..., min_length=1)
    pet_type: str = Field(default="dog")
    breed: Optional[str] = None
    age_years: Optional[float] = None
    duration_days: Optional[int] = None
    severity: Optional[str] = Field(default="moderate")


class DiseaseMatch(BaseModel):
    disease_name: str
    confidence: float = Field(ge=0.0, le=1.0)
    description: str
    common_symptoms: List[str]
    severity: str
    urgency: str
    recommended_actions: List[str]
    veterinary_consult_recommended: bool = True


class SymptomCheckResponse(BaseModel):
    pet_id: UUID
    check_id: str
    timestamp: datetime
    reported_symptoms: List[str]
    possible_diseases: List[DiseaseMatch]
    summary: str
    disclaimer: str = "This is an AI-assisted analysis and does not replace professional veterinary advice."


class NutritionQueryRequest(BaseModel):
    pet_type: str
    breed: Optional[str] = None
    age_years: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None
    health_conditions: List[str] = Field(default_factory=list)
    life_stage: Optional[str] = None


class NutrientRecommendation(BaseModel):
    nutrient: str
    recommended_daily_amount: str
    unit: str
    importance: str
    notes: Optional[str] = None


class FoodSuggestion(BaseModel):
    food_category: str
    examples: List[str]
    benefits: List[str]
    avoid_reasons: List[str] = Field(default_factory=list)


class NutritionQueryResponse(BaseModel):
    pet_profile: Dict[str, Any]
    daily_calorie_target: float
    nutrient_recommendations: List[NutrientRecommendation]
    food_suggestions: List[FoodSuggestion]
    foods_to_avoid: List[str]
    feeding_schedule: Dict[str, str]
    special_notes: List[str]


class KnowledgeSearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    pet_type: Optional[str] = None
    category: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=50)


class KnowledgeArticle(BaseModel):
    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    pet_types: List[str]
    source: str
    relevance_score: float
    last_updated: datetime


class KnowledgeSearchResponse(BaseModel):
    query: str
    results: List[KnowledgeArticle]
    total_count: int
    suggestions: List[str] = Field(default_factory=list)


class DiseaseDetailRequest(BaseModel):
    disease_name: str
    pet_type: str = "dog"


class DiseaseDetail(BaseModel):
    name: str
    pet_types: List[str]
    description: str
    causes: List[str]
    symptoms: List[str]
    diagnosis_methods: List[str]
    treatment_options: List[str]
    prevention: List[str]
    prognosis: str
    when_to_see_vet: str
    related_diseases: List[str]
    references: List[str]
