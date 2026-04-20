"""资源智能匹配引擎"""
import uuid
from backend.resource_matcher.models import UserProfile, ResourceItem, ResourceMatchRequest


# 内置资源数据库 (MVP版本)
RESOURCE_DATABASE = [
    ResourceItem(name="SNAP食品援助", category="food", provider="USDA",
        description="联邦食品援助项目，为低收入家庭提供食品购买资金",
        eligibility=["月收入低于联邦贫困线130%", "美国公民或合法居民", "有社会安全号"],
        benefit_value=250, benefit_period="monthly",
        application_url="https://www.fns.usda.gov/snap", phone="1-800-221-5689",
        documents_required=["身份证明", "收入证明", "居住证明", "社会安全号"], processing_time="7-30天"),
    ResourceItem(name="Section 8住房券", category="housing", provider="HUD",
        description="联邦住房选择券项目，帮助低收入家庭支付租金",
        eligibility=["收入不超过地区中位数的50%", "美国公民或合资格非公民", "无严重犯罪记录"],
        benefit_value=800, benefit_period="monthly",
        application_url="https://www.hud.gov/topics/housing_choice_voucher_program_section_8", phone="1-800-569-4287",
        documents_required=["身份证明", "收入证明", "家庭组成证明", "租赁历史"], processing_time="30-90天"),
    ResourceItem(name="LIHEAP能源援助", category="utility", provider="HHS",
        description="低收入家庭能源援助项目，帮助支付供暖和制冷费用",
        eligibility=["收入不超过联邦贫困线150%或60%州中位数收入", "面临能源费用困难"],
        benefit_value=300, benefit_period="yearly",
        application_url="https://www.acf.hhs.gov/ocs/programs/liheap", phone="1-866-674-6327",
        documents_required=["最近能源账单", "收入证明", "身份证明"], processing_time="15-45天"),
    ResourceItem(name="Medicaid医疗援助", category="healthcare", provider="CMS",
        description="联邦和州联合医疗援助项目，为低收入人群提供医疗保障",
        eligibility=["收入符合州标准", "美国公民或合资格非公民", "州居民"],
        benefit_value=500, benefit_period="monthly",
        application_url="https://www.medicaid.gov", phone="1-800-633-4227",
        documents_required=["身份证明", "收入证明", "居住证明", "社会安全号"], processing_time="15-45天"),
    ResourceItem(name="WIC营养项目", category="food", provider="USDA",
        description="妇女、婴儿和儿童特别营养补充项目",
        eligibility=["孕妇、产后或哺乳期妇女", "5岁以下儿童", "收入不超过185%联邦贫困线"],
        benefit_value=150, benefit_period="monthly",
        application_url="https://www.fns.usda.gov/wic", phone="1-800-311-2229",
        documents_required=["身份证明", "收入证明", "居住证明"], processing_time="7-14天"),
    ResourceItem(name="失业救济金", category="employment", provider="州就业部门",
        description="为失业工人提供临时收入支持",
        eligibility=["非因个人原因失业", "满足最低工资和工时要求", "积极寻找工作"],
        benefit_value=400, benefit_period="weekly",
        application_url="https://www.careeronestop.org", phone="1-877-US2-JOBS",
        documents_required=["就业记录", "身份证明", "银行信息"], processing_time="7-21天"),
]


class ResourceMatcherEngine:
    """智能资源匹配引擎"""

    def match(self, request: ResourceMatchRequest) -> list[ResourceItem]:
        user = request.user
        scored = []
        for resource in RESOURCE_DATABASE:
            if request.categories and resource.category not in request.categories:
                continue
            score = self._calculate_match_score(user, resource)
            if score > 0.3:
                item = resource.model_copy()
                item.match_score = round(score, 2)
                scored.append(item)
        scored.sort(key=lambda r: r.match_score, reverse=True)
        return scored

    def _calculate_match_score(self, user: UserProfile, resource: ResourceItem) -> float:
        score = 0.5  # base score
        # Category relevance boost
        if user.monthly_income < 2000:
            if resource.category in ("food", "housing", "utility"):
                score += 0.2
        if user.employment_status == "unemployed":
            if resource.category == "employment":
                score += 0.3
            elif resource.category == "food":
                score += 0.15
        if user.has_children:
            if "children" in " ".join(resource.eligibility).lower() or resource.category == "food":
                score += 0.1
        if user.is_disabled and resource.category == "healthcare":
            score += 0.15
        if user.is_veteran:
            score += 0.05
        return min(1.0, score)
