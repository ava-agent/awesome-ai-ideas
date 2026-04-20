"""个性化财务教育引擎"""
import uuid
from backend.financial_education.models import LearningModule, QuizQuestion, AssessmentRequest, ProgressResponse


MODULES = [
    LearningModule(module_id="basics-budgeting", title="预算基础", level="beginner",
        description="学习如何创建和管理个人预算，掌握收支平衡的基本技巧",
        content="## 什么是预算？\n\n预算是你告诉钱该去哪里的计划，而不是事后 wondering 钱去了哪里。\n\n### 50/30/20 法则\n- **50%** 需求（房租、食物、交通、保险）\n- **30%** 想要（娱乐、外出、购物）\n- **20%** 储蓄和还债\n\n### 步骤\n1. 列出所有月收入来源\n2. 记录一个月的所有支出\n3. 分类为需求/想要/储蓄\n4. 调整比例使其接近50/30/20\n5. 每周回顾并调整",
        estimated_minutes=20,
        quiz=[
            QuizQuestion(question_id="b1", question="根据50/30/20法则，房租属于哪个类别？",
                options=["想要", "需求", "储蓄"], correct_answer=1,
                explanation="房租是基本生活必需品，属于'需求'类别，应占总收入的50%以内。"),
            QuizQuestion(question_id="b2", question="50/30/20法则建议储蓄多少比例？",
                options=["10%", "20%", "30%"], correct_answer=1,
                explanation="建议将至少20%的收入用于储蓄和还债，为未来建立安全垫。"),
        ]),
    LearningModule(module_id="basics-debt", title="理解债务", level="beginner",
        description="了解不同类型的债务及其影响，学会区分好债和坏债",
        content="## 债务不全是坏事\n\n### 好债 vs 坏债\n- **好债**：帮你增加价值的债务（教育贷款、合理房贷）\n- **坏债**：贬值消费的债务（高息信用卡、消费贷款）\n\n### 关键概念\n- **利率(APR)**：借钱的成本，越高越贵\n- **最低还款**：只还最低会让你陷入利息陷阱\n- **DTI(债务收入比)**：月还款/月收入，健康值<36%",
        estimated_minutes=15,
        quiz=[
            QuizQuestion(question_id="d1", question="以下哪种通常被认为是'好债'？",
                options=["高息信用卡", "教育贷款", "发薪日贷款"], correct_answer=1,
                explanation="教育贷款投资于你的未来收入能力，属于'好债'。"),
        ]),
    LearningModule(module_id="intermediate-saving", title="建立应急基金", level="intermediate",
        description="学习如何建立和维护应急基金，应对突发财务状况",
        content="## 应急基金是你的财务安全网\n\n### 目标金额\n- 初级目标：1个月生活费用\n- 中级目标：3个月生活费用\n- 终极目标：6个月生活费用\n\n### 存钱策略\n1. 自动转账：每月工资日自动转入储蓄\n2. 减少订阅：审查并取消不必要的订阅\n3. 副业收入：将额外收入100%存入应急基金",
        estimated_minutes=15),
]


class EducationEngine:
    """个性化财务教育引擎"""

    def get_modules(self, level: str = None) -> list[LearningModule]:
        if level:
            return [m for m in MODULES if m.level == level]
        return MODULES

    def get_module(self, module_id: str) -> LearningModule | None:
        for m in MODULES:
            if m.module_id == module_id:
                return m
        return None

    def assess_level(self, request: AssessmentRequest) -> ProgressResponse:
        correct = 0
        for ans in request.answers:
            for m in MODULES:
                for q in m.quiz:
                    if q.question_id == ans.get("question_id") and q.correct_answer == ans.get("answer_index"):
                        correct += 1
        total = len(request.answers) or 1
        score_pct = correct / total
        if score_pct >= 0.8:
            level = "advanced"
        elif score_pct >= 0.5:
            level = "intermediate"
        else:
            level = "beginner"

        next_mod = self.get_modules(level)
        return ProgressResponse(
            user_id=request.user_id,
            current_level=level,
            completed_modules=[],
            next_module=next_mod[0].module_id if next_mod else None,
            streak_days=0,
            quiz_scores=[{"date": "today", "score": round(score_pct * 100), "total": len(request.answers), "correct": correct}],
        )
