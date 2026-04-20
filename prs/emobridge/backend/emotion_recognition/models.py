"""
情感识别数据模型
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class EmotionType(str, Enum):
    """情感类型枚举"""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    NEUTRAL = "neutral"
    CONCENTRATED = "concentrated"
    CONFUSED = "confused"
    FRUSTRATED = "frustrated"

class ModalityType(str, Enum):
    """模态类型枚举"""
    FACIAL = "facial"           # 面部表情
    PHYSIOLOGICAL = "physiological"  # 生理信号
    BEHAVIORAL = "behavioral"   # 行为分析
    VOICE = "voice"             # 语音分析
    BCI = "bci"                 # 脑机接口

class EmotionState(BaseModel):
    """情感状态模型"""
    emotion_type: EmotionType
    confidence: float = Field(..., ge=0.0, le=1.0, description="置信度")
    intensity: float = Field(..., ge=0.0, le=1.0, description="强度")
    timestamp: datetime
    duration: Optional[float] = Field(None, description="持续时间(秒)")
    
    class Config:
        use_enum_values = True

class PhysiologicalData(BaseModel):
    """生理信号数据"""
    heart_rate: Optional[float] = Field(None, description="心率")
    hrv: Optional[float] = Field(None, description="心率变异性")
    gsr: Optional[float] = Field(None, description="皮肤电反应")
    temperature: Optional[float] = Field(None, description="体温")
    blood_pressure: Optional[Dict[str, float]] = Field(None, description="血压")
    eeg_data: Optional[Dict[str, float]] = Field(None, description="脑电波数据")
    
    class Config:
        use_enum_values = True

class FacialExpression(BaseModel):
    """面部表情数据"""
    emotion: EmotionType
    confidence: float = Field(..., ge=0.0, le=1.0)
    keypoints: Optional[Dict[str, float]] = Field(None, description="面部关键点")
    gaze_direction: Optional[str] = Field(None, description="注视方向")
    
    class Config:
        use_enum_values = True

class BehavioralData(BaseModel):
    """行为分析数据"""
    activity_level: float = Field(..., ge=0.0, le=1.0, description="活动水平")
    movement_patterns: List[str] = Field(default=[], description="运动模式")
    interaction_frequency: float = Field(..., ge=0.0, description="交互频率")
    posture_analysis: Optional[str] = Field(None, description="姿态分析")
    
    class Config:
        use_enum_values = True

class VoiceAnalysis(BaseModel):
    """语音分析数据"""
    pitch: Optional[float] = Field(None, description="音调")
    volume: Optional[float] = Field(None, description="音量")
    tempo: Optional[float] = Field(None, description="语速")
    emotion: Optional[EmotionType] = Field(None, description="情感识别")
    confidence: Optional[float] = Field(None, description="置信度")
    
    class Config:
        use_enum_values = True

class BCIData(BaseModel):
    """脑机接口数据"""
    brain_wave_patterns: Dict[str, float] = Field(default={}, description="脑电波模式")
    emotion_indicators: Dict[str, float] = Field(default={}, description="情感指标")
    attention_level: float = Field(..., ge=0.0, le=1.0, description="注意力水平")
    relaxation_level: float = Field(..., ge=0.0, le=1.0, description="放松程度")
    
    class Config:
        use_enum_values = True

class ModalityData(BaseModel):
    """多模态数据模型"""
    modality_type: ModalityType
    data: Dict[str, Any]
    timestamp: datetime
    device_id: Optional[str] = Field(None, description="设备ID")
    
    class Config:
        use_enum_values = True

class EmotionDetectionResult(BaseModel):
    """情感检测结果"""
    patient_id: str
    session_id: str
    detected_emotions: List[EmotionState]
    raw_data: List[ModalityData]
    overall_state: EmotionState
    analysis_metadata: Dict[str, Any] = Field(default_factory=dict)
    processing_time: float = Field(..., description="处理时间(秒)")
    
    class Config:
        use_enum_values = True

class PatientEmotionProfile(BaseModel):
    """患者情感档案"""
    patient_id: str
    baseline_emotions: Dict[EmotionType, float] = Field(default_factory=dict)
    emotional_triggers: List[str] = Field(default_factory=list)
    treatment_response_patterns: Dict[str, float] = Field(default_factory=dict)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True

class EmotionTreatmentRecommendation(BaseModel):
    """情感治疗建议"""
    emotion_state: EmotionState
    recommended_action: str
    intervention_intensity: float = Field(..., ge=0.0, le=1.0)
    expected_outcome: str
    confidence_level: float = Field(..., ge=0.0, le=1.0)
    
    class Config:
        use_enum_values = True