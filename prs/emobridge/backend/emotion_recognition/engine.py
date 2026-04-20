"""
情感识别引擎
多模态情感识别核心系统
"""

import numpy as np
import logging
from typing import List, Dict, Optional
from datetime import datetime
import json
from .models import (
    EmotionState, EmotionType, ModalityType, EmotionDetectionResult,
    PhysiologicalData, FacialExpression, BehavioralData, VoiceAnalysis, BCIData,
    PatientEmotionProfile, EmotionTreatmentRecommendation
)
from .processor import MultiModalProcessor

logger = logging.getLogger(__name__)

class EmotionRecognitionEngine:
    """情感识别引擎主类"""
    
    def __init__(self, model_path: Optional[str] = None):
        """初始化情感识别引擎"""
        self.processor = MultiModalProcessor()
        self.model_path = model_path
        self.patient_profiles: Dict[str, PatientEmotionProfile] = {}
        self.confidence_threshold = 0.75
        self.initialize_models()
    
    def initialize_models(self):
        """初始化AI模型"""
        logger.info("初始化情感识别模型...")
        try:
            # 这里应该加载预训练的模型
            # self.emotion_model = load_emotion_model(self.model_path)
            # self.facial_model = load_facial_expression_model()
            # self.physiological_model = load_physiological_model()
            
            # 临时使用模拟模型
            self.models_initialized = True
            logger.info("情感识别模型初始化完成")
        except Exception as e:
            logger.error(f"模型初始化失败: {e}")
            self.models_initialized = False
    
    def detect_emotion_from_physiological(self, physiological_data: PhysiologicalData) -> List[EmotionState]:
        """从生理信号检测情感"""
        if not self.models_initialized:
            return self._get_mock_emotion_states("physiological")
        
        try:
            # 特征提取
            features = self._extract_physiological_features(physiological_data)
            
            # 模型预测
            predictions = self.processor.predict_physiological_emotions(features)
            
            # 转换为EmotionState对象
            emotion_states = []
            for emotion, confidence in predictions.items():
                if confidence >= self.confidence_threshold:
                    emotion_states.append(EmotionState(
                        emotion_type=EmotionType(emotion),
                        confidence=confidence,
                        intensity=confidence * 0.8 + 0.2,  # 模拟强度计算
                        timestamp=datetime.now()
                    ))
            
            return emotion_states
            
        except Exception as e:
            logger.error(f"生理信号情感检测失败: {e}")
            return self._get_mock_emotion_states("physiological")
    
    def detect_emotion_from_facial(self, facial_data: FacialExpression) -> List[EmotionState]:
        """从面部表情检测情感"""
        if not self.models_initialized:
            return self._get_mock_emotion_states("facial")
        
        try:
            features = self._extract_facial_features(facial_data)
            predictions = self.processor.predict_facial_emotions(features)
            
            emotion_states = []
            for emotion, confidence in predictions.items():
                if confidence >= self.confidence_threshold:
                    emotion_states.append(EmotionState(
                        emotion_type=EmotionType(emotion),
                        confidence=confidence,
                        intensity=confidence * 0.9 + 0.1,
                        timestamp=datetime.now()
                    ))
            
            return emotion_states
            
        except Exception as e:
            logger.error(f"面部表情情感检测失败: {e}")
            return self._get_mock_emotion_states("facial")
    
    def detect_emotion_from_behavioral(self, behavioral_data: BehavioralData) -> List[EmotionState]:
        """从行为分析检测情感"""
        if not self.models_initialized:
            return self._get_mock_emotion_states("behavioral")
        
        try:
            features = self._extract_behavioral_features(behavioral_data)
            predictions = self.processor.predict_behavioral_emotions(features)
            
            emotion_states = []
            for emotion, confidence in predictions.items():
                if confidence >= self.confidence_threshold:
                    emotion_states.append(EmotionState(
                        emotion_type=EmotionType(emotion),
                        confidence=confidence,
                        intensity=confidence * 0.7 + 0.3,
                        timestamp=datetime.now()
                    ))
            
            return emotion_states
            
        except Exception as e:
            logger.error(f"行为分析情感检测失败: {e}")
            return self._get_mock_emotion_states("behavioral")
    
    def detect_emotion_from_voice(self, voice_data: VoiceAnalysis) -> List[EmotionState]:
        """从语音分析检测情感"""
        if not self.models_initialized:
            return self._get_mock_emotion_states("voice")
        
        try:
            features = self._extract_voice_features(voice_data)
            predictions = self.processor.predict_voice_emotions(features)
            
            emotion_states = []
            for emotion, confidence in predictions.items():
                if confidence >= self.confidence_threshold:
                    emotion_states.append(EmotionState(
                        emotion_type=EmotionType(emotion),
                        confidence=confidence,
                        intensity=confidence * 0.85 + 0.15,
                        timestamp=datetime.now()
                    ))
            
            return emotion_states
            
        except Exception as e:
            logger.error(f"语音分析情感检测失败: {e}")
            return self._get_mock_emotion_states("voice")
    
    def detect_emotion_from_bci(self, bci_data: BCIData) -> List[EmotionState]:
        """从脑机接口检测情感"""
        if not self.models_initialized:
            return self._get_mock_emotion_states("bci")
        
        try:
            features = self._extract_bci_features(bci_data)
            predictions = self.processor.predict_bci_emotions(features)
            
            emotion_states = []
            for emotion, confidence in predictions.items():
                if confidence >= self.confidence_threshold:
                    emotion_states.append(EmotionState(
                        emotion_type=EmotionType(emotion),
                        confidence=confidence,
                        intensity=confidence * 0.95 + 0.05,  # BCI数据通常更准确
                        timestamp=datetime.now()
                    ))
            
            return emotion_states
            
        except Exception as e:
            logger.error(f"脑机接口情感检测失败: {e}")
            return self._get_mock_emotion_states("bci")
    
    def multimodal_emotion_detection(self, modality_data_list: List) -> EmotionDetectionResult:
        """多模态情感检测"""
        start_time = datetime.now()
        
        all_emotions = []
        
        # 处理各个模态的数据
        for modality_data in modality_data_list:
            if hasattr(modality_data, 'physiological_data'):
                emotions = self.detect_emotion_from_physiological(modality_data.physiological_data)
                all_emotions.extend(emotions)
            elif hasattr(modality_data, 'facial_expression'):
                emotions = self.detect_emotion_from_facial(modality_data.facial_expression)
                all_emotions.extend(emotions)
            elif hasattr(modality_data, 'behavioral_data'):
                emotions = self.detect_emotion_from_behavioral(modality_data.behavioral_data)
                all_emotions.extend(emotions)
            elif hasattr(modality_data, 'voice_analysis'):
                emotions = self.detect_emotion_from_voice(modality_data.voice_analysis)
                all_emotions.extend(emotions)
            elif hasattr(modality_data, 'bci_data'):
                emotions = self.detect_emotion_from_bci(modality_data.bci_data)
                all_emotions.extend(emotions)
        
        # 融合多模态结果
        if all_emotions:
            overall_emotion = self._fuse_emotion_states(all_emotions)
        else:
            overall_emotion = EmotionState(
                emotion_type=EmotionType.NEUTRAL,
                confidence=0.5,
                intensity=0.3,
                timestamp=datetime.now()
            )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return EmotionDetectionResult(
            patient_id="temp_patient_id",
            session_id="temp_session_id",
            detected_emotions=all_emotions,
            raw_data=[],  # 需要根据实际数据结构填充
            overall_state=overall_emotion,
            analysis_metadata={"fusion_method": "weighted_average"},
            processing_time=processing_time
        )
    
    def update_patient_profile(self, patient_id: str, emotion_result: EmotionDetectionResult):
        """更新患者情感档案"""
        if patient_id not in self.patient_profiles:
            self.patient_profiles[patient_id] = PatientEmotionProfile(
                patient_id=patient_id,
                baseline_emotions={}
            )
        
        profile = self.patient_profiles[patient_id]
        profile.last_updated = datetime.now()
        
        # 更新基线情感
        for emotion in emotion_result.detected_emotions:
            if emotion.emotion_type not in profile.baseline_emotions:
                profile.baseline_emotions[emotion.emotion_type] = 0.0
            profile.baseline_emotions[emotion.emotion_type] += emotion.intensity / len(emotion_result.detected_emotions)
    
    def get_treatment_recommendation(self, patient_id: str, current_emotion: EmotionState) -> EmotionTreatmentRecommendation:
        """获取治疗建议"""
        profile = self.patient_profiles.get(patient_id)
        
        if profile:
            # 基于历史数据和当前情感状态生成建议
            recommendation = self._generate_personalized_recommendation(current_emotion, profile)
        else:
            # 通用建议
            recommendation = self._generate_general_recommendation(current_emotion)
        
        return recommendation
    
    def _extract_physiological_features(self, data: PhysiologicalData) -> Dict[str, float]:
        """提取生理信号特征"""
        features = {}
        if data.heart_rate:
            features['heart_rate'] = data.heart_rate
            features['hrv_normalized'] = (data.hrv or 0) / 100  # 归一化
        if data.gsr:
            features['gsr'] = data.gsr
        if data.eeg_data:
            features.update(data.eeg_data)
        return features
    
    def _extract_facial_features(self, data: FacialExpression) -> Dict[str, float]:
        """提取面部特征"""
        features = {
            'emotion_confidence': data.confidence,
            'emotion_type': 1.0 if data.emotion == EmotionType.HAPPY else 0.0
        }
        if data.keypoints:
            features.update(data.keypoints)
        return features
    
    def _extract_behavioral_features(self, data: BehavioralData) -> Dict[str, float]:
        """提取行为特征"""
        return {
            'activity_level': data.activity_level,
            'interaction_frequency': data.interaction_frequency,
            'movement_count': len(data.movement_patterns)
        }
    
    def _extract_voice_features(self, data: VoiceAnalysis) -> Dict[str, float]:
        """提取语音特征"""
        features = {}
        if data.pitch:
            features['pitch'] = data.pitch
        if data.volume:
            features['volume'] = data.volume
        if data.tempo:
            features['tempo'] = data.tempo
        return features
    
    def _extract_bci_features(self, data: BCIData) -> Dict[str, float]:
        """提取BCI特征"""
        features = {
            'attention_level': data.attention_level,
            'relaxation_level': data.relaxation_level
        }
        features.update(data.brain_wave_patterns)
        features.update(data.emotion_indicators)
        return features
    
    def _fuse_emotion_states(self, emotion_states: List[EmotionState]) -> EmotionState:
        """融合多模态情感状态"""
        if not emotion_states:
            return EmotionState(
                emotion_type=EmotionType.NEUTRAL,
                confidence=0.5,
                intensity=0.3,
                timestamp=datetime.now()
            )
        
        # 加权平均融合
        emotion_weights = {}
        total_confidence = sum(emotion.confidence for emotion in emotion_states)
        
        for emotion in emotion_states:
            weight = emotion.confidence / total_confidence
            if emotion.emotion_type not in emotion_weights:
                emotion_weights[emotion.emotion_type] = 0.0
            emotion_weights[emotion.emotion_type] += weight * emotion.intensity
        
        # 选择最可能的情感
        best_emotion = max(emotion_weights.items(), key=lambda x: x[1])
        
        return EmotionState(
            emotion_type=best_emotion[0],
            confidence=min(total_confidence, 1.0),
            intensity=best_emotion[1],
            timestamp=datetime.now()
        )
    
    def _get_mock_emotion_states(self, modality: str) -> List[EmotionState]:
        """获取模拟情感状态（用于测试）"""
        mock_emotions = {
            "physiological": EmotionType.NEUTRAL,
            "facial": EmotionType.HAPPY,
            "behavioral": EmotionType.CONCENTRATED,
            "voice": EmotionType.NEUTRAL,
            "bci": EmotionType.CONCENTRATED
        }
        
        return [EmotionState(
            emotion_type=mock_emotions.get(modality, EmotionType.NEUTRAL),
            confidence=0.8,
            intensity=0.6,
            timestamp=datetime.now()
        )]
    
    def _generate_personalized_recommendation(self, current_emotion: EmotionState, profile: PatientEmotionProfile) -> EmotionTreatmentRecommendation:
        """生成个性化治疗建议"""
        # 基于历史模式的个性化建议
        if current_emotion.emotion_type == EmotionType.FRUSTRATED:
            return EmotionTreatmentRecommendation(
                emotion_state=current_emotion,
                recommended_action="呼吸放松训练",
                intervention_intensity=0.7,
                expected_outcome="降低焦虑水平，提高注意力",
                confidence_level=0.85
            )
        elif current_emotion.emotion_type == EmotionType.CONFUSED:
            return EmotionTreatmentRecommendation(
                emotion_state=current_emotion,
                recommended_action="简化解释并确认理解",
                intervention_intensity=0.5,
                expected_outcome="提高认知清晰度",
                confidence_level=0.90
            )
        else:
            return self._generate_general_recommendation(current_emotion)
    
    def _generate_general_recommendation(self, current_emotion: EmotionState) -> EmotionTreatmentRecommendation:
        """生成通用治疗建议"""
        recommendations = {
            EmotionType.HAPPY: "维持积极状态，记录成功体验",
            EmotionType.SAD: "情感支持，引导表达",
            EmotionType.ANGRY: "冷静训练，情绪管理",
            EmotionType.FEAR: "安全感建立，逐步暴露",
            EmotionType.CONFUSED: "信息简化，重复确认",
            EmotionType.FRUSTRATED: "分解任务，提供支持"
        }
        
        return EmotionTreatmentRecommendation(
            emotion_state=current_emotion,
            recommended_action=recommendations.get(current_emotion.emotion_type, "标准治疗程序"),
            intervention_intensity=0.6,
            expected_outcome="改善情感状态",
            confidence_level=0.75
        )