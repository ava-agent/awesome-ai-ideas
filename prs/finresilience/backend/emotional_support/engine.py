"""情感支持引擎 - 提供压力管理和情感支持"""
import uuid
from backend.emotional_support.models import MoodCheckIn, SupportResponse


COPING_STRATEGIES = {
    (1, 3): ["继续你正在做的，一切都在改善的路上", "今天有什么小事让你感到开心？", "试试写三件感恩的事情"],
    (4, 6): ["深呼吸练习可以帮助缓解紧张", "和朋友或家人聊聊你的感受", "设定小目标，庆祝每个成就"],
    (7, 8): ["这是暂时的，你已经克服过困难", "现在最重要的是照顾好自己", "考虑寻求专业心理咨询"],
    (9, 10): ["你不是一个人，有很多人愿意帮助你", "请拨打危机热线获得即时支持", "允许自己休息，这不是软弱"],
}

VALIDATION_MESSAGES = {
    (1, 4): "你今天的状态不错，继续保持！记住，稳定的情绪是财务决策的基础。",
    (5, 7): "感到有压力是正常的，尤其是在面对财务挑战时。你主动寻求帮助，这本身就是一种力量。",
    (8, 10): "我知道现在感觉非常艰难。财务压力可以让人感到窒息，但请记住：这个困难的时刻会过去的。你已经迈出了寻求帮助的第一步。",
}


class EmotionalSupportEngine:
    """情感支持引擎"""

    def process_check_in(self, check_in: MoodCheckIn) -> SupportResponse:
        stress = check_in.stress_level
        validation = self._get_validation(stress)
        strategies = self._get_strategies(stress)
        exercise = self._recommend_exercise(stress)
        follow_up = self._determine_follow_up(stress)
        resources = self._get_resources(stress)
        crisis_line = "988 生命线 (拨打988)" if stress >= 9 else None

        return SupportResponse(
            session_id=str(uuid.uuid4()),
            validation_message=validation,
            coping_strategies=strategies,
            recommended_exercise=exercise,
            follow_up_days=follow_up,
            resources=resources,
            crisis_hotline=crisis_line,
        )

    def _get_validation(self, stress: int) -> str:
        for (low, high), msg in VALIDATION_MESSAGES.items():
            if low <= stress <= high:
                return msg
        return VALIDATION_MESSAGES[(5, 7)]

    def _get_strategies(self, stress: int) -> list[str]:
        for (low, high), strategies in COPING_STRATEGIES.items():
            if low <= stress <= high:
                return strategies
        return COPING_STRATEGIES[(4, 6)]

    def _recommend_exercise(self, stress: int) -> dict:
        if stress >= 7:
            return {
                "type": "breathing",
                "name": "4-7-8 呼吸法",
                "pattern": "4-7-8",
                "description": "通过控制呼吸激活副交感神经系统，快速降低焦虑",
                "steps": ["用鼻子吸气4秒", "屏住呼吸7秒", "用嘴缓慢呼气8秒", "重复4次"],
            }
        elif stress >= 4:
            return {
                "type": "grounding",
                "name": "5-4-3-2-1 接地法",
                "description": "通过五感将注意力拉回当下，减少焦虑感",
                "steps": ["说出5样你看到的东西", "说出4样你能触摸到的东西", "说出3样你听到的声音", "说出2样你闻到的气味", "说出1样你可以尝到的味道"],
            }
        return {
            "type": "gratitude",
            "name": "三件好事练习",
            "description": "关注积极事物，培养感恩心态",
            "steps": ["回想今天发生的一件好事", "写下它为什么让你感到开心", "想想你能怎样创造更多这样的时刻", "连续练习21天形成习惯"],
        }

    def _determine_follow_up(self, stress: int) -> int:
        if stress >= 9: return 1
        if stress >= 7: return 2
        if stress >= 5: return 3
        return 7

    def _get_resources(self, stress: int) -> list[str]:
        resources = ["https://www.nami.org - 全国精神疾病联盟"]
        if stress >= 7:
            resources.extend([
                "拨打 988 获取24/7危机支持",
                "https://www.7cups.com - 在线情感支持",
            ])
        return resources
