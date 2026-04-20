"""
多模态情感处理器
处理各种模态的情感识别
"""

import numpy as np
from typing import Dict, List, Any
import logging
from .models import EmotionType

logger = logging.getLogger(__name__)

class MultiModalProcessor:
    """多模态处理器"""
    
    def __init__(self):
        """初始化处理器"""
        self.emotion_labels = list(EmotionType)
        self.model_weights = {
            EmotionType.HAPPY: 1.0,
            EmotionType.SAD: 0.9,
            EmotionType.ANGRY: 0.95,
            EmotionType.FEAR: 0.85,
            EmotionType.SURPRISE: 0.8,
            EmotionType.DISGUST: 0.9,
            EmotionType.NEUTRAL: 0.7,
            EmotionType.CONCENTRATED: 0.85,
            EmotionType.CONFUSED: 0.8,
            EmotionType.FRUSTRATED: 0.9
        }
    
    def predict_physiological_emotions(self, features: Dict[str, float]) -> Dict[str, float]:
        """预测生理信号情感"""
        # 模拟生理信号情感识别
        predictions = {}
        
        # 基于心率的情感预测
        if 'heart_rate' in features:
            hr = features['heart_rate']
            if hr < 60:
                predictions['sad'] = 0.7 * self.model_weights[EmotionType.SAD]
                predictions['neutral'] = 0.5
            elif hr > 100:
                predictions['angry'] = 0.8 * self.model_weights[EmotionType.ANGRY]
                predictions['fear'] = 0.6 * self.model_weights[EmotionType.FEAR]
            else:
                predictions['neutral'] = 0.8
                predictions['happy'] = 0.3 * self.model_weights[EmotionType.HAPPY]
        
        # 基于HRV的情感预测
        if 'hrv_normalized' in features:
            hrv = features['hrv_normalized']
            if hrv > 0.6:
                predictions['concentrated'] = 0.8 * self.model_weights[EmotionType.CONCENTRATED]
            elif hrv < 0.3:
                predictions['confused'] = 0.7 * self.model_weights[EmotionType.CONFUSED]
        
        # 基于GSR的情感预测
        if 'gsr' in features:
            gsr = features['gsr']
            if gsr > 0.7:
                predictions['fear'] = 0.9 * self.model_weights[EmotionType.FEAR]
                predictions['angry'] = 0.6 * self.model_weights[EmotionType.ANGRY]
            elif gsr < 0.2:
                predictions['relaxed'] = 0.8 * self.model_weights[EmotionType.NEUTRAL]
        
        # 基于EEG的情感预测
        if 'alpha' in features and 'beta' in features:
            alpha = features['alpha']
            beta = features['beta']
            alpha_beta_ratio = alpha / (beta + 0.001)
            
            if alpha_beta_ratio > 1.5:
                predictions['relaxed'] = 0.85 * self.model_weights[EmotionType.NEUTRAL]
            elif alpha_beta_ratio < 0.8:
                predictions['concentrated'] = 0.9 * self.model_weights[EmotionType.CONCENTRATED]
        
        # 归一化预测结果
        total = sum(predictions.values())
        if total > 0:
            return {k: v/total for k, v in predictions.items()}
        else:
            return {emotion: 1.0/len(self.emotion_labels) for emotion in self.emotion_labels}
    
    def predict_facial_emotions(self, features: Dict[str, float]) -> Dict[str, float]:
        """预测面部表情情感"""
        predictions = {}
        
        # 基于表情置信度的预测
        confidence = features.get('emotion_confidence', 0.5)
        
        # 基于面部关键点的预测
        if 'mouth_openness' in features:
            mouth_openness = features['mouth_openness']
            if mouth_openness > 0.7:
                predictions['surprise'] = 0.8 * self.model_weights[EmotionType.SURPRISE]
            elif mouth_openness < 0.2:
                predictions['sad'] = 0.7 * self.model_weights[EmotionType.SAD]
        
        if 'eyebrow_height' in features:
            eyebrow_height = features['eyebrow_height']
            if eyebrow_height > 0.8:
                predictions['surprise'] = 0.9 * self.model_weights[EmotionType.SURPRISE]
            elif eyebrow_height < 0.2:
                predictions['angry'] = 0.8 * self.model_weights[EmotionType.ANGRY]
        
        if 'eye_wrinkle' in features:
            eye_wrinkle = features['eye_wrinkle']
            if eye_wrinkle > 0.6:
                predictions['happy'] = 0.95 * self.model_weights[EmotionType.HAPPY]
        
        # 归一化
        total = sum(predictions.values())
        if total > 0:
            return {k: v/total for k, v in predictions.items()}
        else:
            # 默认分布
            base_predictions = {
                'neutral': 0.4,
                'happy': 0.2,
                'sad': 0.1,
                'angry': 0.1,
                'surprise': 0.1,
                'confused': 0.1
            }
            return {k: v * confidence for k, v in base_predictions.items()}
    
    def predict_behavioral_emotions(self, features: Dict[str, float]) -> Dict[str, float]:
        """预测行为情感"""
        predictions = {}
        
        # 基于活动水平的预测
        activity_level = features.get('activity_level', 0.5)
        
        if activity_level > 0.8:
            predictions['energetic'] = 0.8
            predictions['happy'] = 0.6 * self.model_weights[EmotionType.HAPPY]
        elif activity_level < 0.2:
            predictions['tired'] = 0.8
            predictions['sad'] = 0.7 * self.model_weights[EmotionType.SAD]
        
        # 基于交互频率的预测
        interaction_freq = features.get('interaction_frequency', 0.5)
        if interaction_freq > 0.7:
            predictions['engaged'] = 0.9 * self.model_weights[EmotionType.CONCENTRATED]
        elif interaction_freq < 0.3:
            predictions['withdrawn'] = 0.8
            predictions['sad'] = 0.6 * self.model_weights[EmotionType.SAD]
        
        # 基于运动模式的预测
        movement_count = features.get('movement_count', 0)
        if movement_count > 5:
            predictions['restless'] = 0.7
            predictions['anxious'] = 0.6 * self.model_weights[EmotionType.FEAR]
        elif movement_count == 0:
            predictions['still'] = 0.8
            predictions['concentrated'] = 0.6 * self.model_weights[EmotionType.CONCENTRATED]
        
        # 归一化
        total = sum(predictions.values())
        if total > 0:
            return {k: v/total for k, v in predictions.items()}
        else:
            return {emotion: 1.0/len(self.emotion_labels) for emotion in self.emotion_labels}
    
    def predict_voice_emotions(self, features: Dict[str, float]) -> Dict[str, float]:
        """预测语音情感"""
        predictions = {}
        
        # 基于音调的预测
        if 'pitch' in features:
            pitch = features['pitch']
            if pitch > 200:  # 高音调
                predictions['excited'] = 0.8
                predictions['happy'] = 0.7 * self.model_weights[EmotionType.HAPPY]
            elif pitch < 100:  # 低音调
                predictions['sad'] = 0.8 * self.model_weights[EmotionType.SAD]
                predictions['angry'] = 0.6 * self.model_weights[EmotionType.ANGRY]
        
        # 基于音量的预测
        if 'volume' in features:
            volume = features['volume']
            if volume > 0.8:
                predictions['loud'] = 0.9
                predictions['angry'] = 0.7 * self.model_weights[EmotionType.ANGRY]
            elif volume < 0.2:
                predictions['quiet'] = 0.9
                predictions['sad'] = 0.7 * self.model_weights[EmotionType.SAD]
        
        # 基于语速的预测
        if 'tempo' in features:
            tempo = features['tempo']
            if tempo > 200:  # 快速
                predictions['fast'] = 0.8
                predictions['excited'] = 0.6 * self.model_weights[EmotionType.SURPRISE]
            elif tempo < 100:  # 慢速
                predictions['slow'] = 0.8
                predictions['sad'] = 0.6 * self.model_weights[EmotionType.SAD]
        
        # 归一化
        total = sum(predictions.values())
        if total > 0:
            return {k: v/total for k, v in predictions.items()}
        else:
            return {emotion: 1.0/len(self.emotion_labels) for emotion in self.emotion_labels}
    
    def predict_bci_emotions(self, features: Dict[str, float]) -> Dict[str, float]:
        """预测BCI信号情感"""
        predictions = {}
        
        # 基于注意力水平的预测
        attention_level = features.get('attention_level', 0.5)
        if attention_level > 0.8:
            predictions['focused'] = 0.9 * self.model_weights[EmotionType.CONCENTRATED]
        elif attention_level < 0.3:
            predictions['distracted'] = 0.8
            predictions['confused'] = 0.7 * self.model_weights[EmotionType.CONFUSED]
        
        # 基于放松程度的预测
        relaxation_level = features.get('relaxation_level', 0.5)
        if relaxation_level > 0.7:
            predictions['relaxed'] = 0.9
            predictions['happy'] = 0.6 * self.model_weights[EmotionType.HAPPY]
        elif relaxation_level < 0.3:
            predictions 'stressed'] = 0.9
            predictions['angry'] = 0.7 * self.model_weights[EmotionType.ANGRY]
        
        # 基于脑电波模式的预测
        if 'alpha_power' in features:
            alpha = features['alpha_power']
            beta = features.get('beta_power', 0.1)
            theta = features.get('theta_power', 0.1)
            
            alpha_beta_ratio = alpha / (beta + 0.001)
            alpha_theta_ratio = alpha / (theta + 0.001)
            
            if alpha_beta_ratio > 2.0 and alpha_theta_ratio > 1.5:
                predictions['deep_relaxation'] = 0.95
                predictions['happy'] = 0.8 * self.model_weights[EmotionType.HAPPY]
            elif alpha_beta_ratio < 0.5:
                predictions['active_thinking'] = 0.9 * self.model_weights[EmotionType.CONCENTRATED]
        
        # 归一化
        total = sum(predictions.values())
        if total > 0:
            return {k: v/total for k, v in predictions.items()}
        else:
            return {emotion: 1.0/len(self.emotion_labels) for emotion in self.emotion_labels}
    
    def fuse_modalities(self, predictions_list: List[Dict[str, float]]) -> Dict[str, float]:
        """融合多个模态的预测结果"""
        if not predictions_list:
            return {emotion: 1.0/len(self.emotion_labels) for emotion in self.emotion_labels}
        
        # 加权平均融合
        fused_predictions = {}
        num_modalities = len(predictions_list)
        
        for emotion in self.emotion_labels:
            total_confidence = 0.0
            for predictions in predictions_list:
                # 查找匹配的情感标签
                emotion_key = emotion.value
                if emotion_key in predictions:
                    total_confidence += predictions[emotion_key]
                else:
                    # 如果没有直接匹配，使用默认值
                    total_confidence += 0.1
            
            fused_predictions[emotion] = total_confidence / num_modalities
        
        # 归一化
        total = sum(fused_predictions.values())
        if total > 0:
            return {k: v/total for k, v in fused_predictions.items()}
        else:
            return {emotion: 1.0/len(self.emotion_labels) for emotion in self.emotion_labels}
    
    def calculate_emotion_similarity(self, emotion1: str, emotion2: str) -> float:
        """计算情感相似度"""
        # 定义情感相似度矩阵
        similarity_matrix = {
            ('happy', 'excited'): 0.9,
            ('happy', 'energetic'): 0.8,
            ('sad', 'tired'): 0.8,
            ('sad', 'depressed'): 0.9,
            ('angry', 'frustrated'): 0.8,
            ('angry', 'irritated'): 0.9,
            ('fear', 'anxious'): 0.9,
            ('fear', 'worried'): 0.8,
            ('surprise', 'astonished'): 0.9,
            ('concentrated', 'focused'): 0.9,
            ('confused', 'distracted'): 0.8,
            ('neutral', 'calm'): 0.8
        }
        
        # 查找相似度
        key1 = (emotion1, emotion2)
        key2 = (emotion2, emotion1)
        
        if key1 in similarity_matrix:
            return similarity_matrix[key1]
        elif key2 in similarity_matrix:
            return similarity_matrix[key2]
        else:
            # 默认相似度
            if emotion1 == emotion2:
                return 1.0
            else:
                return 0.3
    
    def detect_emotion_transitions(self, emotion_history: List[str]) -> List[str]:
        """检测情感转换模式"""
        if len(emotion_history) < 2:
            return []
        
        transitions = []
        
        for i in range(1, len(emotion_history)):
            prev_emotion = emotion_history[i-1]
            current_emotion = emotion_history[i]
            
            if prev_emotion != current_emotion:
                similarity = self.calculate_emotion_similarity(prev_emotion, current_emotion)
                
                if similarity < 0.5:  # 显著转换
                    transition = f"{prev_emotion} -> {current_emotion}"
                    transitions.append(transition)
        
        return transitions