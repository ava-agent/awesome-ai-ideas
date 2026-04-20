"""债务优化引擎 - 分析债务结构并制定还款策略"""
import uuid
from backend.debt_optimizer.models import (
    DebtItem, DebtOptimizationRequest, DebtOptimizationResponse,
    DebtStrategy, PaymentStep, NegotiationTemplate
)


class DebtOptimizerEngine:
    """智能债务优化引擎"""

    def optimize(self, req: DebtOptimizationRequest) -> DebtOptimizationResponse:
        debts = [d.model_copy() for d in req.debts]
        total_debt = sum(d.balance for d in debts)
        monthly_min = sum(d.minimum_payment for d in debts)
        extra = max(0, req.available_monthly - monthly_min)

        if req.strategy == DebtStrategy.AVALANCHE:
            debts.sort(key=lambda d: d.interest_rate, reverse=True)
        elif req.strategy == DebtStrategy.SNOWBALL:
            debts.sort(key=lambda d: d.balance)

        # Simulate payoff
        schedule = self._simulate_payoff(debts, monthly_min, extra)
        total_interest = sum(s.total_paid - total_debt for s in schedule if schedule)

        # Compare vs minimum-only
        min_interest = self._calc_min_only_interest(debts, monthly_min)
        saved = min_interest - total_interest

        payoff_months = len(schedule) if schedule else 0

        templates = self._generate_templates(debts)
        recommendations = self._generate_recommendations(debts, req.strategy, saved, payoff_months)

        return DebtOptimizationResponse(
            optimization_id=str(uuid.uuid4()),
            strategy_used=req.strategy,
            total_debt=round(total_debt, 2),
            monthly_minimum=round(monthly_min, 2),
            extra_payment=round(extra, 2),
            estimated_payoff_months=payoff_months,
            total_interest=round(max(0, total_interest), 2),
            total_interest_saved=round(max(0, saved), 2),
            payment_schedule=schedule,
            negotiation_templates=templates,
            recommendations=recommendations,
        )

    def _simulate_payoff(self, debts, monthly_min, extra, max_months=600) -> list[PaymentStep]:
        schedule = []
        balances = {d.name: d.balance for d in debts}
        rates = {d.name: d.interest_rate for d in debts}
        minimums = {d.name: d.minimum_payment for d in debts}
        remaining = list(balances.keys())

        for month in range(1, max_months + 1):
            if not remaining:
                break
            payments = []
            extra_pool = extra
            for name in remaining[:]:
                bal = balances[name]
                if bal <= 0:
                    remaining.remove(name)
                    continue
                monthly_rate = rates[name] / 100 / 12
                interest = bal * monthly_rate
                bal += interest
                payment = min(minimums[name], bal)
                bal -= payment
                balances[name] = bal
                if bal <= 0:
                    remaining.remove(name)
                    payments.append({"name": name, "amount": round(payment, 2), "remaining": 0.0})
                else:
                    payments.append({"name": name, "amount": round(payment, 2), "remaining": round(bal, 2)})

            # Apply extra to first remaining debt
            if extra_pool > 0 and remaining:
                target = remaining[0]
                bal = balances[target]
                pay = min(extra_pool, bal)
                bal -= pay
                balances[target] = bal
                if bal <= 0:
                    remaining.remove(target)
                # Update last payment entry
                for p in payments:
                    if p["name"] == target:
                        p["amount"] = round(p["amount"] + pay, 2)
                        p["remaining"] = round(bal, 2)
                        break

            total_rem = sum(balances.values())
            total_paid_month = sum(p["amount"] for p in payments)
            schedule.append(PaymentStep(
                month=month,
                payments=payments,
                total_paid=round(total_paid_month, 2),
                total_remaining=round(total_rem, 2),
            ))

        return schedule

    def _calc_min_only_interest(self, debts, monthly_min, max_months=600) -> float:
        balances = {d.name: d.balance for d in debts}
        rates = {d.name: d.interest_rate for d in debts}
        remaining = list(balances.keys())
        total_paid = 0.0
        for month in range(1, max_months + 1):
            if not remaining: break
            for name in remaining[:]:
                bal = balances[name]
                monthly_rate = rates[name] / 100 / 12
                interest = bal * monthly_rate
                bal += interest
                payment = min(bal, monthly_min / max(len(remaining), 1))
                bal -= payment
                total_paid += payment
                balances[name] = bal
                if bal <= 0.01: remaining.remove(name)
        return total_paid - sum(d.balance for d in debts)

    def _generate_templates(self, debts: list[DebtItem]) -> list[NegotiationTemplate]:
        templates = []
        for d in debts:
            if d.interest_rate > 15 or d.is_collection:
                templates.append(NegotiationTemplate(
                    creditor=d.creditor or d.name,
                    debt_type=d.debt_type.value,
                    template_subject=f"关于 {d.name} 账户的还款安排协商",
                    template_body=(
                        f"尊敬的 {d.creditor or d.name} 团队：\n\n"
                        f"我是账户 {d.name} 的持有人。由于近期的财务困难，"
                        f"我希望能与贵方协商一个可行的还款方案。\n\n"
                        f"当前欠款余额：${d.balance:.2f}\n"
                        f"当前利率：{d.interest_rate}%\n\n"
                        f"我希望能探讨以下选项：\n"
                        f"1. 降低利率至合理水平\n"
                        f"2. 制定分期还款计划\n"
                        f"3. 一次性结算折扣\n\n"
                        f"期待您的回复。\n"
                    ),
                    tips=[
                        "保持专业和礼貌的语气",
                        "清楚说明你的困难和还款意愿",
                        "不要承诺你无法实现的还款金额",
                        "所有协商结果要求书面确认",
                    ],
                ))
        return templates

    def _generate_recommendations(self, debts, strategy, saved, months) -> list[str]:
        recs = []
        high_interest = [d for d in debts if d.interest_rate > 20]
        if high_interest:
            recs.append(f"⚠️ 有{len(high_interest)}笔高息债务(>20%)，优先处理可显著减少利息支出")
        if strategy == DebtStrategy.AVALANCHE:
            recs.append("📊 使用雪崩法（高息优先），这是数学上最优的策略，可节省最多利息")
        elif strategy == DebtStrategy.SNOWBALL:
            recs.append("❄️ 使用雪球法（小额优先），通过快速消除小额债务获得心理动力")
        if saved > 100:
            recs.append(f"💰 通过优化还款策略，预计可节省${saved:.0f}利息支出")
        if months > 60:
            recs.append("⏰ 预计还款时间超过5年，建议考虑债务合并或寻求专业咨询")
        if any(d.is_collection for d in debts):
            recs.append("📞 有催收债务，建议优先协商并了解你的合法权益")
        return recs
