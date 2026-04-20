"""危机分析引擎 - 评估财务紧急程度并生成行动计划"""
import uuid
from datetime import datetime, timezone
from backend.crisis_analyzer.models import (
    FinancialSnapshot, CrisisAssessmentResponse, SeverityLevel, ActionPlan
)


class CrisisAnalyzerEngine:
    """AI驱动的财务危机分析引擎"""

    def analyze(self, snapshot: FinancialSnapshot) -> CrisisAssessmentResponse:
        cash_flow_score = self._calc_cash_flow_score(snapshot)
        debt_burden_score = self._calc_debt_burden_score(snapshot)
        savings_buffer = self._calc_savings_buffer(snapshot)
        severity = self._determine_severity(cash_flow_score, debt_burden_score, savings_buffer)
        risk_factors = self._identify_risks(snapshot, cash_flow_score, debt_burden_score, savings_buffer)
        strengths = self._identify_strengths(snapshot)

        return CrisisAssessmentResponse(
            assessment_id=str(uuid.uuid4()),
            severity=severity,
            cash_flow_score=round(cash_flow_score, 2),
            debt_burden_score=round(debt_burden_score, 2),
            savings_buffer_months=round(savings_buffer, 1),
            risk_factors=risk_factors,
            strengths=strengths,
            action_plan_3m=self._generate_plan(snapshot, severity, 3),
            action_plan_6m=self._generate_plan(snapshot, severity, 6),
            action_plan_9m=self._generate_plan(snapshot, severity, 9),
            ai_analysis=self._generate_analysis(snapshot, severity, risk_factors, strengths),
        )

    def _calc_cash_flow_score(self, s: FinancialSnapshot) -> float:
        if s.monthly_income <= 0:
            return 0.0
        surplus = s.monthly_income - s.monthly_expenses - s.monthly_debt_payments
        ratio = surplus / s.monthly_income
        return max(0.0, min(100.0, 50 + ratio * 100))

    def _calc_debt_burden_score(self, s: FinancialSnapshot) -> float:
        if s.monthly_income <= 0:
            return 100.0 if s.total_debt > 0 else 0.0
        dti = (s.monthly_debt_payments / s.monthly_income) * 100
        return min(100.0, dti * 2)

    def _calc_savings_buffer(self, s: FinancialSnapshot) -> float:
        monthly_burn = s.monthly_expenses + s.monthly_debt_payments
        if monthly_burn <= 0:
            return 999.0 if s.total_savings > 0 else 0.0
        return s.total_savings / monthly_burn

    def _determine_severity(self, cf: float, db: float, buf: float) -> SeverityLevel:
        score = 0
        if cf < 30: score += 3
        elif cf < 50: score += 2
        elif cf < 70: score += 1
        if db > 70: score += 3
        elif db > 40: score += 2
        elif db > 20: score += 1
        if buf < 1: score += 3
        elif buf < 3: score += 2
        elif buf < 6: score += 1
        if score >= 7: return SeverityLevel.CRISIS
        if score >= 5: return SeverityLevel.HIGH
        if score >= 3: return SeverityLevel.MEDIUM
        return SeverityLevel.LOW

    def _identify_risks(self, s: FinancialSnapshot, cf: float, db: float, buf: float) -> list[str]:
        risks = []
        if s.employment_status == "unemployed": risks.append("当前失业，无稳定收入来源")
        if s.monthly_income <= 0: risks.append("月收入为零，面临生存危机")
        if cf < 30: risks.append("现金流严重不足，月度赤字")
        if db > 60: risks.append("债务负担过重，DTI超过健康水平")
        if buf < 1: risks.append("储蓄不足支撑1个月开支")
        if not s.insurance_coverage: risks.append("缺乏保险保障，意外风险敞口大")
        if "medical" in str(s.recent_life_events).lower(): risks.append("近期医疗事件可能导致额外支出")
        if s.dependents > 0 and cf < 50: risks.append(f"有{s.dependents}名受抚养人，但收入紧张")
        return risks

    def _identify_strengths(self, s: FinancialSnapshot) -> list[str]:
        strengths = []
        if s.monthly_income > s.monthly_expenses + s.monthly_debt_payments:
            surplus = s.monthly_income - s.monthly_expenses - s.monthly_debt_payments
            strengths.append(f"月度盈余${surplus:.0f}，有改善空间")
        if s.total_savings > 0: strengths.append(f"有${s.total_savings:.0f}储蓄作为安全垫")
        if s.employment_status == "employed": strengths.append("目前有稳定就业")
        if s.insurance_coverage: strengths.append("已有保险保障")
        if s.total_debt == 0: strengths.append("无负债负担")
        if not strengths: strengths.append("已迈出寻求帮助的第一步，这是改变的开始")
        return strengths

    def _generate_plan(self, s: FinancialSnapshot, severity: SeverityLevel, months: int) -> ActionPlan:
        plans = {
            (SeverityLevel.CRISIS, 3): ActionPlan(
                timeline_months=3, title="生存稳定计划",
                priorities=["立即联系债权人协商延期", "申请紧急救助金", "削减非必要开支至最低", "寻找临时收入来源"],
                estimated_savings=s.monthly_expenses * 0.3,
                milestones=[{"month": 1, "goal": "稳定基本生活开支"}, {"month": 2, "goal": "建立紧急联系清单"}, {"month": 3, "goal": "现金流转正"}],
            ),
            (SeverityLevel.HIGH, 3): ActionPlan(
                timeline_months=3, title="快速修复计划",
                priorities=["制定严格预算并执行", "联系债权人协商利率", "申请适用的政府援助", "开始副业/临时工作"],
                estimated_savings=s.monthly_expenses * 0.2,
                milestones=[{"month": 1, "goal": "完成预算制定"}, {"month": 2, "goal": "至少一项援助申请提交"}, {"month": 3, "goal": "债务减少10%"}],
            ),
            (SeverityLevel.MEDIUM, 3): ActionPlan(
                timeline_months=3, title="巩固改善计划",
                priorities=["优化支出结构", "建立应急基金", "开始偿还高息债务", "提升财务知识"],
                estimated_savings=s.monthly_expenses * 0.15,
                milestones=[{"month": 1, "goal": "削减不必要开支20%"}, {"month": 2, "goal": "应急基金达到1个月开支"}, {"month": 3, "goal": "完成一个教育模块"}],
            ),
            (SeverityLevel.LOW, 3): ActionPlan(
                timeline_months=3, title="预防强化计划",
                priorities=["完善应急基金(3-6个月)", "优化投资组合", "建立长期财务目标", "学习进阶财务知识"],
                estimated_savings=s.monthly_expenses * 0.1,
                milestones=[{"month": 1, "goal": "评估并优化保险覆盖"}, {"month": 2, "goal": "应急基金达到3个月"}, {"month": 3, "goal": "制定5年财务路线图"}],
            ),
        }
        return plans.get((severity, months), plans.get((severity, 3), plans[(SeverityLevel.MEDIUM, 3)]))

    def _generate_analysis(self, s: FinancialSnapshot, severity: SeverityLevel, risks: list[str], strengths: list[str]) -> str:
        severity_desc = {"low": "良好", "medium": "需要关注", "high": "需要紧急行动", "crisis": "需要立即干预"}
        desc = severity_desc.get(severity.value, "未知")
        analysis = (
            f"## 财务健康分析\n\n"
            f"**综合评级：{desc}**\n\n"
            f"基于您的财务状况分析，当前月收入为${s.monthly_income:.0f}，"
            f"月支出${s.monthly_expenses:.0f}，月债务还款${s.monthly_debt_payments:.0f}。\n\n"
            f"**识别的风险因素：**\n"
        )
        for r in risks:
            analysis += f"- {r}\n"
        analysis += f"\n**您的优势：**\n"
        for st in strengths:
            analysis += f"- {st}\n"
        analysis += "\n建议立即查看下方行动计划，从第一个优先事项开始行动。记住，寻求帮助是力量的体现。"
        return analysis
