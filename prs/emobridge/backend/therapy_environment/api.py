"""
治疗环境API路由
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from .models import (
    VRSession, ARSession, PhysicalSession, EnvironmentConfig, EnvironmentType,
    TherapyType, SessionStatus, TherapyEnvironmentRequest, SessionMetrics,
    EnvironmentSimulationResult, EnvironmentProfile, SessionSummary
)
from .engine import TherapyEnvironmentEngine

from ..emotion_recognition.models import EmotionState

logger = logging.getLogger(__name__)
therapy_router = APIRouter()

# 全局治疗环境引擎
therapy_engine = TherapyEnvironmentEngine()

@therapy_router.post("/create-session")
async def create_therapy_session(request: TherapyEnvironmentRequest):
    """
    创建治疗会话
    """
    try:
        session = therapy_engine.create_session(request)
        return {
            "success": True,
            "message": "治疗会话创建成功",
            "session": session.dict(),
            "session_id": session.session_id,
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"创建治疗会话失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")

@therapy_router.post("/start-session/{session_id}")
async def start_therapy_session(session_id: str):
    """
    开始治疗会话
    """
    try:
        session = therapy_engine.start_session(session_id)
        return {
            "success": True,
            "message": "治疗会话开始成功",
            "session": session.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"开始治疗会话失败: {e}")
        raise HTTPException(status_code=500, detail=f"开始失败: {str(e)}")

@therapy_router.post("/update-progress/{session_id}")
async def update_session_progress(session_id: str, progress_data: Dict[str, Any]):
    """
    更新治疗会话进度
    """
    try:
        session = therapy_engine.update_session_progress(session_id, progress_data)
        return {
            "success": True,
            "message": "治疗会话进度更新成功",
            "session": session.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"更新治疗会话进度失败: {e}")
        raise HTTPException(status_code=500, detail=f"更新失败: {str(e)}")

@therapy_router.post("/complete-session/{session_id}")
async def complete_therapy_session(session_id: str, completion_data: Optional[Dict[str, Any]] = None):
    """
    完成治疗会话
    """
    try:
        session = therapy_engine.complete_session(session_id, completion_data)
        return {
            "success": True,
            "message": "治疗会话完成成功",
            "session": session.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"完成治疗会话失败: {e}")
        raise HTTPException(status_code=500, detail=f"完成失败: {str(e)}")

@therapy_router.post("/pause-session/{session_id}")
async def pause_therapy_session(session_id: str, reason: str = ""):
    """
    暂停治疗会话
    """
    try:
        session = therapy_engine.pause_session(session_id, reason)
        return {
            "success": True,
            "message": "治疗会话暂停成功",
            "session": session.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"暂停治疗会话失败: {e}")
        raise HTTPException(status_code=500, detail=f"暂停失败: {str(e)}")

@therapy_router.post("/resume-session/{session_id}")
async def resume_therapy_session(session_id: str):
    """
    恢复治疗会话
    """
    try:
        session = therapy_engine.resume_session(session_id)
        return {
            "success": True,
            "message": "治疗会话恢复成功",
            "session": session.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"恢复治疗会话失败: {e}")
        raise HTTPException(status_code=500, detail=f"恢复失败: {str(e)}")

@therapy_router.post("/cancel-session/{session_id}")
async def cancel_therapy_session(session_id: str, reason: str = ""):
    """
    取消治疗会话
    """
    try:
        session = therapy_engine.cancel_session(session_id, reason)
        return {
            "success": True,
            "message": "治疗会话取消成功",
            "session": session.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"取消治疗会话失败: {e}")
        raise HTTPException(status_code=500, detail=f"取消失败: {str(e)}")

@therapy_router.get("/session/{session_id}")
async def get_therapy_session(session_id: str):
    """
    获取治疗会话详情
    """
    try:
        if session_id not in therapy_engine.active_sessions and session_id not in therapy_engine.completed_sessions:
            raise HTTPException(status_code=404, detail="治疗会话不存在")
        
        session = therapy_engine.active_sessions.get(session_id, therapy_engine.completed_sessions[session_id])
        return {
            "success": True,
            "session": session.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取治疗会话失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")

@therapy_router.get("/session/{session_id}/metrics")
async def get_session_metrics(session_id: str):
    """
    获取治疗会话指标
    """
    try:
        metrics = therapy_engine.get_session_metrics(session_id)
        return {
            "success": True,
            "metrics": metrics.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取会话指标失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取指标失败: {str(e)}")

@therapy_router.get("/session/{session_id}/summary")
async def get_session_summary(session_id: str):
    """
    获取治疗会话摘要
    """
    try:
        summary = therapy_engine.get_session_summary(session_id)
        return {
            "success": True,
            "summary": summary.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取会话摘要失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取摘要失败: {str(e)}")

@therapy_router.get("/sessions/active")
async def get_active_sessions():
    """
    获取活跃的治疗会话
    """
    try:
        sessions = therapy_engine.get_active_sessions()
        return {
            "success": True,
            "sessions": [session.dict() for session in sessions],
            "count": len(sessions),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"获取活跃会话失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")

@therapy_router.get("/sessions/patient/{patient_id}")
async def get_patient_sessions(patient_id: str):
    """
    获取患者的治疗会话
    """
    try:
        sessions = therapy_engine.get_patient_sessions(patient_id)
        return {
            "success": True,
            "sessions": [session.dict() for session in sessions],
            "count": len(sessions),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"获取患者会话失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")

@therapy_router.post("/simulate-environment")
async def simulate_environment(config: EnvironmentConfig):
    """
    模拟治疗效果
    """
    try:
        simulation = therapy_engine.simulate_environment(config)
        return {
            "success": True,
            "simulation": simulation.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"环境模拟失败: {e}")
        raise HTTPException(status_code=500, detail=f"模拟失败: {str(e)}")

@therapy_router.get("/environment-profiles")
async def get_environment_profiles(
    environment_type: Optional[EnvironmentType] = None,
    therapy_type: Optional[TherapyType] = None
):
    """
    获取环境档案列表
    """
    try:
        profiles = therapy_engine.get_environment_profiles(environment_type, therapy_type)
        return {
            "success": True,
            "profiles": [profile.dict() for profile in profiles],
            "count": len(profiles),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"获取环境档案失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")

@therapy_router.post("/environment-profiles")
async def create_environment_profile(profile: EnvironmentProfile):
    """
    创建环境档案
    """
    try:
        new_profile = therapy_engine.create_custom_profile(profile)
        return {
            "success": True,
            "message": "环境档案创建成功",
            "profile": new_profile.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"创建环境档案失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")

@therapy_router.get("/environment-profiles/{profile_id}")
async def get_environment_profile(profile_id: str):
    """
    获取特定环境档案
    """
    try:
        if profile_id not in therapy_engine.environment_profiles:
            raise HTTPException(status_code=404, detail="环境档案不存在")
        
        profile = therapy_engine.environment_profiles[profile_id]
        return {
            "success": True,
            "profile": profile.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取环境档案失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")

@therapy_router.get("/sessions/export/{session_id}")
async def export_session_data(session_id: str):
    """
    导出治疗会话数据
    """
    try:
        export_data = therapy_engine.export_session_data(session_id)
        return {
            "success": True,
            "export_data": export_data,
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"导出会话数据失败: {e}")
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")

@therapy_router.get("/sessions/export/all/{patient_id}")
async def export_all_patient_data(patient_id: str):
    """
    导出患者所有会话数据
    """
    try:
        sessions = therapy_engine.get_patient_sessions(patient_id)
        export_data = {
            "patient_id": patient_id,
            "sessions": [],
            "export_timestamp": datetime.now().isoformat()
        }
        
        for session in sessions:
            session_data = therapy_engine.export_session_data(session.session_id)
            export_data["sessions"].append(session_data)
        
        return {
            "success": True,
            "export_data": export_data,
            "session_count": len(sessions),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"导出患者数据失败: {e}")
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")

@therapy_router.get("/statistics/overview")
async def get_overall_statistics():
    """
    获取治疗环境整体统计
    """
    try:
        active_sessions = therapy_engine.get_active_sessions()
        all_profiles = therapy_engine.get_environment_profiles()
        
        # 计算统计数据
        total_sessions = len(therapy_engine.completed_sessions)
        completed_this_week = len([s for s in therapy_engine.completed_sessions.values() 
                                  if s.end_time and (datetime.now() - s.end_time).days <= 7])
        
        # 按环境类型统计
        environment_stats = {}
        for profile in all_profiles:
            env_type = profile.environment_type.value
            if env_type not in environment_stats:
                environment_stats[env_type] = {
                    "usage_count": profile.usage_count,
                    "profile_count": 0,
                    "avg_effectiveness": 0.0
                }
            environment_stats[env_type]["profile_count"] += 1
        
        # 按治疗类型统计
        therapy_stats = {}
        for profile in all_profiles:
            therapy_type = profile.therapy_type.value
            if therapy_type not in therapy_stats:
                therapy_stats[therapy_type] = {
                    "usage_count": profile.usage_count,
                    "profile_count": 0,
                    "avg_effectiveness": 0.0
                }
            therapy_stats[therapy_type]["profile_count"] += 1
        
        # 计算平均效果评分
        avg_effectiveness = sum(p.effectiveness_rating for p in all_profiles) / len(all_profiles) if all_profiles else 0.0
        
        statistics = {
            "active_sessions": len(active_sessions),
            "completed_sessions": total_sessions,
            "completed_this_week": completed_this_week,
            "environment_profiles": len(all_profiles),
            "average_effectiveness": avg_effectiveness,
            "environment_usage": environment_stats,
            "therapy_usage": therapy_stats,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "statistics": statistics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取统计失败: {str(e)}")

@therapy_router.get("/health")
async def therapy_environment_health():
    """
    治疗环境系统健康检查
    """
    try:
        health_status = {
            "status": "healthy",
            "active_sessions": len(therapy_engine.active_sessions),
            "completed_sessions": len(therapy_engine.completed_sessions),
            "environment_profiles": len(therapy_engine.environment_profiles),
            "timestamp": datetime.now().isoformat()
        }
        
        return health_status
    except Exception as e:
        logger.error(f"治疗环境系统健康检查失败: {e}")
        raise HTTPException(status_code=500, detail=f"健康检查失败: {str(e)}")

@therapy_router.get("/recommendations/{patient_id}")
async def get_treatment_recommendations(patient_id: str):
    """
    为患者获取治疗建议
    """
    try:
        patient_sessions = therapy_engine.get_patient_sessions(patient_id)
        
        if not patient_sessions:
            return {
                "success": True,
                "recommendations": [
                    "建议开始基础治疗会话",
                    "可考虑从放松环境开始"
                ],
                "timestamp": datetime.now().isoformat()
            }
        
        # 基于历史会话分析推荐
        recommendations = []
        
        # 分析最近的会话
        recent_session = patient_sessions[0]
        
        # 基于治疗类型推荐
        if recent_session.therapy_type.value == TherapyType.MINDFULNESS:
            recommendations.append("建议继续正念练习，可尝试不同的放松环境")
            recommendations.append("考虑延长治疗时间以增强效果")
        
        elif recent_session.therapy_type.value == TherapyType.EXPOSURE_THERAPY:
            recommendations.append("建议逐步增加暴露难度")
            recommendations.append("可考虑添加更多交互元素")
        
        # 基于环境类型推荐
        if recent_session.environment_type.value == EnvironmentType.VR:
            recommendations.append("VR体验良好，可尝试更多VR场景")
            recommendations.append("建议定期进行现实环境过渡训练")
        
        elif recent_session.environment_type.value == EnvironmentType.AR:
            recommendations.append("AR应用效果良好，可扩展到更多生活场景")
            recommendations.append("建议增加现实世界的应用练习")
        
        # 基于进度调整
        if recent_session.progress < 0.5:
            recommendations.append("当前进度较慢，建议增加治疗频率")
        elif recent_session.progress > 0.8:
            recommendations.append("治疗进展良好，可考虑增加难度")
        
        return {
            "success": True,
            "recommendations": recommendations,
            "based_on_sessions": len(patient_sessions),
            "latest_session_progress": recent_session.progress,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"获取治疗建议失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取建议失败: {str(e)}")

@therapy_router.get("/available-environments")
async def get_available_environments():
    """
    获取可用的治疗环境
    """
    try:
        profiles = therapy_engine.get_environment_profiles()
        
        available_envs = {}
        for profile in profiles:
            env_type = profile.environment_type.value
            if env_type not in available_envs:
                available_envs[env_type] = []
            
            available_envs[env_type].append({
                "profile_id": profile.profile_id,
                "name": profile.name,
                "description": profile.description,
                "therapy_types": [profile.therapy_type.value],
                "effectiveness_rating": profile.effectiveness_rating,
                "usage_count": profile.usage_count
            })
        
        return {
            "success": True,
            "available_environments": available_envs,
            "total_profiles": len(profiles),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"获取可用环境失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")

@therapy_router.post("/batch-session-update")
async def batch_update_sessions(update_data: List[Dict[str, Any]]):
    """
    批量更新治疗会话
    """
    try:
        results = []
        failed = []
        
        for i, update in enumerate(update_data):
            session_id = update.get("session_id")
            update_type = update.get("type")
            update_data = update.get("data", {})
            
            try:
                if update_type == "progress":
                    session = therapy_engine.update_session_progress(session_id, update_data)
                elif update_type == "pause":
                    session = therapy_engine.pause_session(session_id, update_data.get("reason", ""))
                elif update_type == "resume":
                    session = therapy_engine.resume_session(session_id)
                elif update_type == "complete":
                    session = therapy_engine.complete_session(session_id, update_data)
                else:
                    raise ValueError(f"不支持的更新类型: {update_type}")
                
                results.append({
                    "session_id": session_id,
                    "success": True,
                    "type": update_type
                })
                
            except Exception as e:
                results.append({
                    "session_id": session_id,
                    "success": False,
                    "error": str(e),
                    "type": update_type
                })
                failed.append(session_id)
        
        return {
            "success": True,
            "total_updates": len(update_data),
            "successful_updates": len([r for r in results if r["success"]]),
            "failed_updates": len(failed),
            "results": results,
            "failed_sessions": failed,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"批量更新会话失败: {e}")
        raise HTTPException(status_code=500, detail=f"批量更新失败: {str(e)}")