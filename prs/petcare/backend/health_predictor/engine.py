"""
Health Predictor - Core prediction engine.
"""
import logging
from datetime import datetime, timedelta, date
from uuid import uuid4
from typing import List, Dict, Any, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class RiskAssessmentEngine:
    """Assesses pet health risks based on historical data."""

    def assess_risk(self, pet_data: Dict, period_days: int = 30) -> Dict:
        risk_factors = []
        total_score = 0.0
        weight_factor = self._analyze_weight_risk(pet_data.get("weight_history", []))
        if weight_factor:
            risk_factors.append(weight_factor)
            total_score += weight_factor["score"] * 0.3

        activity_factor = self._analyze_activity_risk(pet_data.get("activity_history", []))
        if activity_factor:
            risk_factors.append(activity_factor)
            total_score += activity_factor["score"] * 0.25

        diet_factor = self._analyze_diet_risk(pet_data.get("diet_history", []))
        if diet_factor:
            risk_factors.append(diet_factor)
            total_score += diet_factor["score"] * 0.25

        behavior_factor = self._analyze_behavior_risk(pet_data.get("behavior_history", []))
        if behavior_factor:
            risk_factors.append(behavior_factor)
            total_score += behavior_factor["score"] * 0.2

        overall = min(total_score, 1.0)
        risk_level = "low" if overall < 0.3 else "medium" if overall < 0.6 else "high" if overall < 0.8 else "critical"

        recommendations = self._generate_recommendations(risk_factors, overall)

        return {
            "assessment_id": str(uuid4()), "timestamp": datetime.utcnow(),
            "overall_risk_score": round(overall, 2), "risk_level": risk_level,
            "risk_factors": risk_factors,
            "trend_analysis": {"period_days": period_days, "data_points": sum(len(pet_data.get(k, [])) for k in ["weight_history", "activity_history", "diet_history"])},
            "recommendations": recommendations,
            "next_assessment_date": (date.today() + timedelta(days=7)).isoformat(),
        }

    def _analyze_weight_risk(self, weight_history: List[Dict]) -> Optional[Dict]:
        if len(weight_history) < 2:
            return None
        recent = weight_history[-7:] if len(weight_history) >= 7 else weight_history
        first, last = recent[0]["value"], recent[-1]["value"]
        change_pct = abs(last - first) / first if first > 0 else 0
        if change_pct > 0.05:
            return {"factor_name": "weight_fluctuation", "risk_level": "medium" if change_pct < 0.1 else "high",
                    "score": min(change_pct * 2, 1.0), "description": f"Weight changed {change_pct:.1%} in recent period",
                    "contributing_data": {"change_pct": round(change_pct, 3), "start": first, "end": last}}
        return {"factor_name": "weight_stable", "risk_level": "low", "score": 0.1,
                "description": "Weight is stable", "contributing_data": {}}

    def _analyze_activity_risk(self, activity_history: List[Dict]) -> Optional[Dict]:
        if not activity_history:
            return None
        recent_durations = [a.get("duration_minutes", 0) for a in activity_history[-7:]]
        avg_duration = sum(recent_durations) / len(recent_durations) if recent_durations else 0
        if avg_duration < 20:
            return {"factor_name": "low_activity", "risk_level": "medium", "score": 0.5,
                    "description": f"Average daily activity only {avg_duration:.0f} minutes",
                    "contributing_data": {"avg_duration": round(avg_duration)}}
        return {"factor_name": "activity_normal", "risk_level": "low", "score": 0.15,
                "description": f"Activity level normal ({avg_duration:.0f} min/day)",
                "contributing_data": {"avg_duration": round(avg_duration)}}

    def _analyze_diet_risk(self, diet_history: List[Dict]) -> Optional[Dict]:
        if not diet_history:
            return None
        recent_calories = [d.get("calories", 0) or 0 for d in diet_history[-7:]]
        avg_cal = sum(recent_calories) / len(recent_calories) if recent_calories else 0
        if avg_cal < 400:
            return {"factor_name": "underfeeding", "risk_level": "medium", "score": 0.5,
                    "description": f"Average daily calories ({avg_cal:.0f}) below recommended",
                    "contributing_data": {"avg_calories": round(avg_cal)}}
        elif avg_cal > 1200:
            return {"factor_name": "overfeeding", "risk_level": "medium", "score": 0.4,
                    "description": f"Average daily calories ({avg_cal:.0f}) above recommended",
                    "contributing_data": {"avg_calories": round(avg_cal)}}
        return {"factor_name": "diet_normal", "risk_level": "low", "score": 0.1,
                "description": "Diet within normal range", "contributing_data": {}}

    def _analyze_behavior_risk(self, behavior_history: List[Dict]) -> Optional[Dict]:
        if not behavior_history:
            return None
        anomalies = [b for b in behavior_history[-14:] if b.get("is_anomaly")]
        anomaly_rate = len(anomalies) / max(len(behavior_history[-14:]), 1)
        if anomaly_rate > 0.3:
            return {"factor_name": "behavior_anomalies", "risk_level": "high", "score": min(anomaly_rate, 1.0),
                    "description": f"{anomaly_rate:.0%} of recent behaviors flagged as anomalous",
                    "contributing_data": {"anomaly_rate": round(anomaly_rate, 2)}}
        return {"factor_name": "behavior_normal", "risk_level": "low", "score": 0.1,
                "description": "Behavior patterns normal", "contributing_data": {}}

    def _generate_recommendations(self, risk_factors: List[Dict], overall: float) -> List[str]:
        recs = []
        for f in risk_factors:
            if f["risk_level"] in ("high", "critical"):
                recs.append(f"⚠️ {f['description']} - consider consulting a veterinarian")
            elif f["risk_level"] == "medium":
                recs.append(f"Monitor: {f['description']}")
        if overall < 0.3:
            recs.append("✅ Overall health risk is low. Keep up the good care!")
        return recs


class TrendAnalyzer:
    """Analyzes trends in pet health metrics over time."""

    def analyze_metric(self, data_points: List[Dict], metric_name: str, unit: str) -> Dict:
        if len(data_points) < 2:
            return {"metric_name": metric_name, "unit": unit, "current_value": data_points[-1]["value"] if data_points else 0,
                    "trend_direction": "insufficient_data", "trend_slope": 0, "data_points": [],
                    "anomaly_count": 0, "is_concerning": False}

        values = [p["value"] for p in data_points]
        mean_val = sum(values) / len(values)
        std_val = (sum((v - mean_val) ** 2 for v in values) / len(values)) ** 0.5 if len(values) > 1 else 0

        # Simple linear regression for slope
        n = len(values)
        x_mean = (n - 1) / 2
        numerator = sum((i - x_mean) * (values[i] - mean_val) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        slope = numerator / denominator if denominator != 0 else 0

        direction = "increasing" if slope > 0.01 else "decreasing" if slope < -0.01 else "stable"

        # Detect anomalies (values > 2 std from mean)
        anomalies = [i for i, v in enumerate(values) if std_val > 0 and abs(v - mean_val) / std_val > 2]

        trend_points = [{"date": p.get("date", ""), "value": p["value"], "baseline": round(mean_val, 2)} for p in data_points]

        is_concerning = abs(slope) > std_val * 0.5 if std_val > 0 else False

        return {
            "metric_name": metric_name, "unit": unit, "current_value": values[-1],
            "trend_direction": direction, "trend_slope": round(slope, 4),
            "data_points": trend_points, "anomaly_count": len(anomalies), "is_concerning": is_concerning,
        }


class AlertEngine:
    """Generates health alerts based on predictions and anomaly detection."""

    def generate_alerts(self, pet_id_str: str, risk_assessment: Dict) -> List[Dict]:
        alerts = []
        for factor in risk_assessment.get("risk_factors", []):
            if factor["risk_level"] in ("high", "critical"):
                alerts.append({
                    "alert_id": str(uuid4()), "pet_id": pet_id_str,
                    "alert_type": factor["factor_name"], "severity": factor["risk_level"],
                    "title": f"Health Alert: {factor['factor_name'].replace('_', ' ').title()}",
                    "description": factor["description"],
                    "recommendation": "Consult your veterinarian for a professional evaluation.",
                    "risk_score": factor["score"], "created_at": datetime.utcnow(),
                })
        return alerts


risk_engine = RiskAssessmentEngine()
trend_analyzer = TrendAnalyzer()
alert_engine = AlertEngine()
