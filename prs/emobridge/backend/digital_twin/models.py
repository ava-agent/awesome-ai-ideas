"""
数字孪生数据模型
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

class TwinStateType(str, Enum):
    """数字孪生状态类型"""
    STABLE = "stable"
    TRANSITIONING = "transitioning"
    PREDICTING = "predicting"
    ANOMALY = "anomaly"
    UPDATING = "updating"

class EmotionState(BaseModel):
    """情感状态"""
    emotion_type: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    intensity: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime

class PhysiologicalState(BaseModel):
    """生理状态"""
    heart_rate: Optional[float] = None
    hrv: Optional[float] = None
    gsr: Optional[float] = None
    temperature: Optional[float] = None
    blood_pressure: Optional[Dict[str, float]] = None
    eeg_patterns: Optional[Dict[str, float]] = None
    timestamp: datetime

class BehavioralState(BaseModel):
    """行为状态"""
    activity_level: float = Field(..., ge=0.0, le=1.0)
    interaction_patterns: List[str] = Field(default_factory=list)
    movement_metrics: Dict[str, float] = Field(default_factory=dict)
    social_engagement: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime

class PredictionType(str, Enum):
    """预测类型"""
    EMOTION_TRANSITION = "emotion_transition"
    TREATMENT_RESPONSE = "treatment_response"
    CRISIS_PREVENTION = "crisis_prevention"
    RECOVERY_PREDICTION = "recovery_prediction"

class PredictionResult(BaseModel):
    """预测结果"""
    prediction_type: PredictionType
    confidence: float = Field(..., ge=0.0, le=1.0)
    predicted_value: Any
    prediction_time: datetime
    confidence_interval: Optional[Dict[str, float]] = None
    influencing_factors: List[str] = Field(default_factory=list)
    recommendation: Optional[str] = None

class TwinState(BaseModel):
    """数字孪生状态"""
    state_type: TwinStateType
    emotional_state: Optional[EmotionState] = None
    physiological_state: Optional[PhysiologicalState] = None
    behavioral_state: Optional[BehavioralState] = None
    predictions: List[PredictionResult] = Field(default_factory=list)
    stability_score: float = Field(..., ge=0.0, le=1.0)
    last_updated: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)

class PatientDigitalTwin(BaseModel):
    """患者数字孪生"""
    patient_id: str
    twin_version: str
    current_state: TwinState
    historical_states: List[TwinState] = Field(default_factory=list)
    evolution_patterns: Dict[str, float] = Field(default_factory=dict)
    treatment_effectiveness: Dict[str, float] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

class TreatmentSimulation(BaseModel):
    """治疗模拟"""
    simulation_id: str
    patient_id: str
    treatment_plan: Dict[str, Any]
    simulation_parameters: Dict[str, Any]
    predicted_outcome: PredictionResult
    simulation_duration: float  # 模拟时长（小时）
    created_at: datetime

class CrisisDetectionResult(BaseModel):
    """危机检测结果"""
    crisis_level: float = Field(..., ge=0.0, le=1.0)
    crisis_type: str
    risk_factors: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    urgency_score: float = Field(..., ge=0.0, le=1.0)
    detection_time: datetime

class TwinUpdateRequest(BaseModel):
    """数字孪生更新请求"""
    patient_id: str
    emotion_data: Optional[Dict[str, Any]] = None
    physiological_data: Optional[Dict[str, Any]] = None
    behavioral_data: Optional[Dict[str, Any]] = None
    update_metadata: Dict[str, Any] = Field(default_factory=dict)

class TwinQueryRequest(BaseModel):
    """数字孪生查询请求"""
    patient_id: str
    query_type: str
    time_range: Optional[Dict[str, datetime]] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)