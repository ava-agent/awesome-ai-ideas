"""
数字孪生引擎
情感数字孪生核心系统
"""

import numpy as np
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
from .models import (
    PatientDigitalTwin, TwinState, TwinStateType, EmotionState,
    PhysiologicalState, BehavioralState, PredictionResult, PredictionType,
    TreatmentSimulation, CrisisDetectionResult, TwinUpdateRequest
)
from ..emotion_recognition.models import EmotionType

logger = logging.getLogger(__name__)

class DigitalTwinEngine:
    """数字孪生引擎主类"""
    
    def __init__(self):
        """初始化数字孪生引擎"""
        self.patient_twins: Dict[str, PatientDigitalTwin] = {}
        self.prediction_models = {}
        self.simulation_engine = None
        self.initialize_models()
    
    def initialize_models(self):
        """初始化预测模型"""
        logger.info("初始化数字孪生预测模型...")
        
        try:
            # 这里应该加载预训练的预测模型
            # self.prediction_models['emotion_transition'] = load_emotion_transition_model()
            # self.prediction_models['treatment_response'] = load_treatment_response_model()
            # self.prediction_models['crisis_prevention'] = load_crisis_prevention_model()
            
            # 临时使用模拟模型
            self.models_initialized = True
            logger.info("数字孪生预测模型初始化完成")
            
        except Exception as e:
            logger.error(f"预测模型初始化失败: {e}")
            self.models_initialized = False
    
    def create_patient_twin(self, patient_id: str) -> PatientDigitalTwin:
        """创建患者数字孪生"""
        if patient_id in self.patient_twins:
            raise ValueError(f"患者 {patient_id} 的数字孪生已存在")
        
        # 创建初始状态
        initial_state = TwinState(
            state_type=TwinStateType.STABLE,
            stability_score=1.0,
            last_updated=datetime.now()
        )
        
        twin = PatientDigitalTwin(
            patient_id=patient_id,
            twin_version="1.0.0",
            current_state=initial_state,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.patient_twins[patient_id] = twin
        logger.info(f"创建患者 {patient_id} 的数字孪生")
        
        return twin
    
    def update_twin_state(self, update_request: TwinUpdateRequest) -> PatientDigitalTwin:
        """更新数字孪生状态"""
        patient_id = update_request.patient_id
        
        if patient_id not in self.patient_twins:
            # 如果不存在，先创建
            self.create_patient_twin(patient_id)
        
        twin = self.patient_twins[patient_id]
        current_state = twin.current_state
        
        # 更新状态
        new_state = TwinState(
            state_type=TwinStateType.UPDATING,
            last_updated=datetime.now()
        )
        
        # 处理情感数据
        if update_request.emotion_data:
            emotion_state = self._process_emotion_data(update_request.emotion_data)
            new_state.emotional_state = emotion_state
        
        # 处理生理数据
        if update_request.physiological_data:
            physiological_state = self._process_physiological_data(update_request.physiological_data)
            new_state.physiological_state = physiological_state
        
        # 处理行为数据
        if update_request.behavioral_data:
            behavioral_state = self._process_behavioral_data(update_request.behavioral_data)
            new_state.behavioral_state = behavioral_state
        
        # 计算稳定性分数
        new_state.stability_score = self._calculate_stability_score(new_state)
        
        # 确定状态类型
        new_state.state_type = self._determine_state_type(new_state)
        
        # 添加到历史状态
        twin.historical_states.append(twin.current_state)
        
        # 更新当前状态
        twin.current_state = new_state
        twin.updated_at = datetime.now()
        
        # 更新演化模式
        self._update_evolution_patterns(twin)
        
        logger.info(f"更新患者 {patient_id} 的数字孪生状态")
        
        return twin
    
    def predict_emotion_transition(self, patient_id: str, hours_ahead: float = 24) -> PredictionResult:
        """预测情感转换"""
        if patient_id not in self.patient_twins:
            raise ValueError(f"患者 {patient_id} 的数字孪生不存在")
        
        twin = self.patient_twins[patient_id]
        
        if not self.models_initialized:
            return self._get_mock_emotion_prediction()
        
        try:
            # 基于历史数据进行情感转换预测
            current_emotion = twin.current_state.emotional_state
            evolution_data = twin.evolution_patterns
            
            # 模拟预测逻辑
            prediction = self._simulate_emotion_prediction(current_emotion, evolution_data, hours_ahead)
            
            return prediction
            
        except Exception as e:
            logger.error(f"情感转换预测失败: {e}")
            return self._get_mock_emotion_prediction()
    
    def predict_treatment_response(self, patient_id: str, treatment_plan: Dict[str, Any]) -> PredictionResult:
        """预测治疗响应"""
        if patient_id not in self.patient_twins:
            raise ValueError(f"患者 {patient_id} 的数字孪生不存在")
        
        twin = self.patient_twins[patient_id]
        
        if not self.models_initialized:
            return self._get_mock_treatment_prediction(treatment_plan)
        
        try:
            # 基于当前状态和历史响应预测治疗效果
            current_state = twin.current_state
            historical_responses = twin.treatment_effectiveness
            
            prediction = self._simulate_treatment_prediction(current_state, treatment_plan, historical_responses)
            
            return prediction
            
        except Exception as e:
            logger.error(f"治疗响应预测失败: {e}")
            return self._get_mock_treatment_prediction(treatment_plan)
    
    def detect_crisis(self, patient_id: str) -> CrisisDetectionResult:
        """检测危机状态"""
        if patient_id not in self.patient_twins:
            raise ValueError(f"患者 {patient_id} 的数字孪生不存在")
        
        twin = self.patient_twins[patient_id]
        
        try:
            # 分析当前状态以检测潜在危机
            crisis_result = self._analyze_crisis_risk(twin.current_state)
            
            # 基于历史趋势验证
            crisis_result = self._validate_crisis_with_historical_data(twin, crisis_result)
            
            return crisis_result
            
        except Exception as e:
            logger.error(f"危机检测失败: {e}")
            return CrisisDetectionResult(
                crisis_level=0.1,
                crisis_type="unknown",
                risk_factors=[],
                recommended_actions=["继续监测"],
                urgency_score=0.1,
                detection_time=datetime.now()
            )
    
    def simulate_treatment(self, patient_id: str, treatment_plan: Dict[str, Any], duration_hours: float = 168) -> TreatmentSimulation:
        """模拟治疗效果"""
        if patient_id not in self.patient_twins:
            raise ValueError(f"患者 {patient_id} 的数字孪生不存在")
        
        twin = self.patient_twins[patient_id]
        
        try:
            # 基于当前状态和治疗计划进行模拟
            predicted_outcome = self.predict_treatment_response(patient_id, treatment_plan)
            
            simulation = TreatmentSimulation(
                simulation_id=f"sim_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                patient_id=patient_id,
                treatment_plan=treatment_plan,
                simulation_parameters={
                    "duration_hours": duration_hours,
                    "model_version": "1.0.0",
                    "simulation_type": "monte_carlo"
                },
                predicted_outcome=predicted_outcome,
                simulation_duration=duration_hours,
                created_at=datetime.now()
            )
            
            return simulation
            
        except Exception as e:
            logger.error(f"治疗模拟失败: {e}")
            raise e
    
    def get_twin_insights(self, patient_id: str, time_range: Optional[Dict[str, datetime]] = None) -> Dict[str, Any]:
        """获取数字孪生洞察"""
        if patient_id not in self.patient_twins:
            raise ValueError(f"患者 {patient_id} 的数字孪生不存在")
        
        twin = self.patient_twins[patient_id]
        
        # 筛选时间范围内的历史数据
        historical_data = self._filter_historical_data(twin, time_range)
        
        insights = {
            "current_state": twin.current_state.dict(),
            "evolution_patterns": twin.evolution_patterns,
            "treatment_effectiveness": twin.treatment_effectiveness,
            "historical_analysis": self._analyze_historical_trends(historical_data),
            "risk_factors": self._identify_risk_factors(twin),
            "recommendations": self._generate_recommendations(twin)
        }
        
        return insights
    
    def get_twin_state_history(self, patient_id: str, limit: int = 100) -> List[TwinState]:
        """获取数字孪生历史状态"""
        if patient_id not in self.patient_twins:
            raise ValueError(f"患者 {patient_id} 的数字孪生不存在")
        
        twin = self.patient_twins[patient_id]
        return twin.historical_states[-limit:]  # 返回最近的limit条记录
    
    def export_twin_data(self, patient_id: str) -> Dict[str, Any]:
        """导出数字孪生数据"""
        if patient_id not in self.patient_twins:
            raise ValueError(f"患者 {patient_id} 的数字孪生不存在")
        
        twin = self.patient_twins[patient_id]
        
        export_data = {
            "patient_id": patient_id,
            "twin_version": twin.twin_version,
            "current_state": twin.current_state.dict(),
            "evolution_patterns": twin.evolution_patterns,
            "treatment_effectiveness": twin.treatment_effectiveness,
            "historical_states": [state.dict() for state in twin.historical_states],
            "export_timestamp": datetime.now().isoformat()
        }
        
        return export_data
    
    def _process_emotion_data(self, emotion_data: Dict[str, Any]) -> EmotionState:
        """处理情感数据"""
        return EmotionState(
            emotion_type=emotion_data.get("emotion_type", "neutral"),
            confidence=emotion_data.get("confidence", 0.5),
            intensity=emotion_data.get("intensity", 0.3),
            timestamp=datetime.now()
        )
    
    def _process_physiological_data(self, physiological_data: Dict[str, Any]) -> PhysiologicalState:
        """处理生理数据"""
        return PhysiologicalState(
            heart_rate=physiological_data.get("heart_rate"),
            hrv=physiological_data.get("hrv"),
            gsr=physiological_data.get("gsr"),
            temperature=physiological_data.get("temperature"),
            blood_pressure=physiological_data.get("blood_pressure"),
            eeg_patterns=physiological_data.get("eeg_patterns"),
            timestamp=datetime.now()
        )
    
    def _process_behavioral_data(self, behavioral_data: Dict[str, Any]) -> BehavioralState:
        """处理行为数据"""
        return BehavioralState(
            activity_level=behavioral_data.get("activity_level", 0.5),
            interaction_patterns=behavioral_data.get("interaction_patterns", []),
            movement_metrics=behavioral_data.get("movement_metrics", {}),
            social_engagement=behavioral_data.get("social_engagement", 0.5),
            timestamp=datetime.now()
        )
    
    def _calculate_stability_score(self, state: TwinState) -> float:
        """计算稳定性分数"""
        stability_score = 1.0
        
        # 基于情感状态稳定性
        if state.emotional_state:
            stability_score *= (1.0 - state.emotional_state.intensity * 0.3)
        
        # 基于生理状态稳定性
        if state.physiological_state:
            if state.physiological_state.heart_rate and state.physiological_state.heart_rate > 100:
                stability_score *= 0.8
        
        # 基于行为状态稳定性
        if state.behavioral_state:
            if state.behavioral_state.activity_level > 0.8:
                stability_score *= 0.9
        
        return max(0.0, min(1.0, stability_score))
    
    def _determine_state_type(self, state: TwinState) -> TwinStateType:
        """确定状态类型"""
        if state.stability_score < 0.3:
            return TwinStateType.ANOMALY
        elif state.stability_score < 0.6:
            return TwinStateType.TRANSITIONING
        elif len(state.predictions) > 0:
            return TwinStateType.PREDICTING
        else:
            return TwinStateType.STABLE
    
    def _update_evolution_patterns(self, twin: PatientDigitalTwin):
        """更新演化模式"""
        if len(twin.historical_states) < 2:
            return
        
        # 分析情感变化模式
        recent_emotions = [state.emotional_state for state in twin.historical_states[-5:] 
                          if state.emotional_state]
        
        if recent_emotions:
            emotion_changes = []
            for i in range(1, len(recent_emotions)):
                emotion_changes.append(recent_emotions[i].emotion_type)
            
            # 计算情感转换频率
            emotion_transition_rate = len(set(emotion_changes)) / len(emotion_changes) if emotion_changes else 0
            twin.evolution_patterns["emotion_transition_rate"] = emotion_transition_rate
    
    def _simulate_emotion_prediction(self, current_emotion: EmotionState, evolution_data: Dict[str, Any], hours_ahead: float) -> PredictionResult:
        """模拟情感预测"""
        # 基于当前情感和演化模式预测情感转换
        possible_transitions = ["happy", "sad", "angry", "neutral", "concentrated"]
        
        # 基于演化数据调整转换概率
        if evolution_data.get("emotion_transition_rate", 0) > 0.5:
            # 高转换率，情感变化快
            predicted_emotion = np.random.choice(possible_transitions)
            confidence = 0.6
        else:
            # 稳定状态，保持当前情感
            predicted_emotion = current_emotion.emotion_type
            confidence = 0.8
        
        return PredictionResult(
            prediction_type=PredictionType.EMOTION_TRANSITION,
            confidence=confidence,
            predicted_value=predicted_emotion,
            prediction_time=datetime.now() + timedelta(hours=hours_ahead),
            influencing_factors=["current_emotional_state", "historical_patterns"],
            recommendation="根据当前情感状态调整治疗策略"
        )
    
    def _simulate_treatment_prediction(self, current_state: TwinState, treatment_plan: Dict[str, Any], historical_responses: Dict[str, float]) -> PredictionResult:
        """模拟治疗响应预测"""
        # 基于当前状态和历史响应预测治疗效果
        
        # 计算基础响应概率
        base_response_rate = 0.7
        
        # 根据当前状态调整
        if current_state.stability_score < 0.5:
            base_response_rate *= 0.8
        else:
            base_response_rate *= 1.2
        
        # 根据治疗类型调整
        treatment_type = treatment_plan.get("type", "standard")
        treatment_effectiveness = historical_responses.get(treatment_type, 0.7)
        
        final_confidence = min(0.95, base_response_rate * treatment_effectiveness)
        
        return PredictionResult(
            prediction_type=PredictionType.TREATMENT_RESPONSE,
            confidence=final_confidence,
            predicted_value="improvement",
            prediction_time=datetime.now() + timedelta(hours=48),
            confidence_interval={"lower": final_confidence - 0.1, "upper": final_confidence + 0.1},
            influencing_factors=["current_state", "treatment_type", "historical_response"],
            recommendation="继续当前治疗计划"
        )
    
    def _analyze_crisis_risk(self, state: TwinState) -> CrisisDetectionResult:
        """分析危机风险"""
        crisis_level = 0.0
        risk_factors = []
        
        # 分析情感状态
        if state.emotional_state:
            if state.emotional_state.emotion_type in ["angry", "fear", "sad"]:
                crisis_level += state.emotional_state.intensity * 0.4
                risk_factors.append("high_negative_emotion")
        
        # 分析生理状态
        if state.physiological_state:
            if state.physiological_state.heart_rate and state.physiological_state.heart_rate > 120:
                crisis_level += 0.3
                risk_factors.append("elevated_heart_rate")
            
            if state.physiological_state.gsr and state.physiological_state.gsr > 0.8:
                crisis_level += 0.2
                risk_factors.append("high_stress_level")
        
        # 分析行为状态
        if state.behavioral_state:
            if state.behavioral_state.activity_level > 0.9:
                crisis_level += 0.2
                risk_factors.append("agitated_behavior")
            elif state.behavioral_state.activity_level < 0.1:
                crisis_level += 0.1
                risk_factors.append("withdrawn_behavior")
        
        crisis_level = min(1.0, crisis_level)
        
        # 确定危机类型和紧急程度
        if crisis_level > 0.7:
            crisis_type = "severe_crisis"
            urgency_score = crisis_level
        elif crisis_level > 0.4:
            crisis_type = "moderate_crisis"
            urgency_score = crisis_level
        else:
            crisis_type = "low_risk"
            urgency_score = crisis_level
        
        # 生成建议
        recommendations = []
        if crisis_level > 0.5:
            recommendations.append("立即干预")
        if crisis_level > 0.3:
            recommendations.append("增加监测频率")
        recommendations.append("记录当前状态")
        
        return CrisisDetectionResult(
            crisis_level=crisis_level,
            crisis_type=crisis_type,
            risk_factors=risk_factors,
            recommended_actions=recommendations,
            urgency_score=urgency_score,
            detection_time=datetime.now()
        )
    
    def _validate_crisis_with_historical_data(self, twin: PatientDigitalTwin, crisis_result: CrisisDetectionResult) -> CrisisDetectionResult:
        """基于历史数据验证危机检测"""
        # 检查历史趋势
        if len(twin.historical_states) >= 3:
            recent_stability = [state.stability_score for state in twin.historical_states[-3:]]
            
            # 如果稳定性持续下降，提高危机级别
            if all(recent_stability[i] > recent_stability[i+1] for i in range(len(recent_stability)-1)):
                crisis_result.crisis_level *= 1.2
                crisis_result.urgency_score *= 1.2
        
        return crisis_result
    
    def _filter_historical_data(self, twin: PatientDigitalTwin, time_range: Optional[Dict[str, datetime]] = None) -> List[TwinState]:
        """筛选历史数据"""
        if not time_range:
            return twin.historical_states
        
        start_time = time_range.get("start")
        end_time = time_range.get("end")
        
        filtered_data = []
        for state in twin.historical_states:
            if start_time and state.last_updated < start_time:
                continue
            if end_time and state.last_updated > end_time:
                continue
            filtered_data.append(state)
        
        return filtered_data
    
    def _analyze_historical_trends(self, historical_data: List[TwinState]) -> Dict[str, Any]:
        """分析历史趋势"""
        if not historical_data:
            return {}
        
        # 计算平均稳定性
        avg_stability = np.mean([state.stability_score for state in historical_data])
        
        # 分析情感变化趋势
        emotion_changes = []
        for state in historical_data:
            if state.emotional_state:
                emotion_changes.append(state.emotional_state.emotion_type)
        
        emotion_distribution = {}
        for emotion in emotion_changes:
            emotion_distribution[emotion] = emotion_distribution.get(emotion, 0) + 1
        
        return {
            "average_stability": avg_stability,
            "emotion_distribution": emotion_distribution,
            "data_points": len(historical_data)
        }
    
    def _identify_risk_factors(self, twin: PatientDigitalTwin) -> List[str]:
        """识别风险因素"""
        risk_factors = []
        
        # 基于当前状态的风险
        current_state = twin.current_state
        if current_state.stability_score < 0.5:
            risk_factors.append("low_stability")
        
        if current_state.emotional_state and current_state.emotional_state.intensity > 0.8:
            risk_factors.append("high_emotional_intensity")
        
        # 基于历史趋势的风险
        if len(twin.historical_states) >= 5:
            recent_states = twin.historical_states[-5:]
            stability_trend = [state.stability_score for state in recent_states]
            
            if stability_trend[-1] < stability_trend[0] * 0.8:
                risk_factors.append("declining_stability")
        
        return risk_factors
    
    def _generate_recommendations(self, twin: PatientDigitalTwin) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 基于稳定性评分
        if twin.current_state.stability_score < 0.5:
            recommendations.append("建议增加治疗频率")
        elif twin.current_state.stability_score > 0.8:
            recommendations.append("保持当前治疗节奏")
        
        # 基于情感状态
        if twin.current_state.emotional_state:
            emotion = twin.current_state.emotional_state.emotion_type
            if emotion == "sad":
                recommendations.append("考虑增加情感支持")
            elif emotion == "angry":
                recommendations.append("考虑引入愤怒管理技术")
        
        return recommendations
    
    def _get_mock_emotion_prediction(self) -> PredictionResult:
        """获取模拟情感预测"""
        return PredictionResult(
            prediction_type=PredictionType.EMOTION_TRANSITION,
            confidence=0.75,
            predicted_value="stable",
            prediction_time=datetime.now() + timedelta(hours=24),
            influencing_factors=["historical_patterns"],
            recommendation="继续监测情感变化"
        )
    
    def _get_mock_treatment_prediction(self, treatment_plan: Dict[str, Any]) -> PredictionResult:
        """获取模拟治疗预测"""
        return PredictionResult(
            prediction_type=PredictionType.TREATMENT_RESPONSE,
            confidence=0.8,
            predicted_value="improvement",
            prediction_time=datetime.now() + timedelta(hours=48),
            confidence_interval={"lower": 0.7, "upper": 0.9},
            influencing_factors=["current_state", "treatment_type"],
            recommendation="继续当前治疗计划"
        )