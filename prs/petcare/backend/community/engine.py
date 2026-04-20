"""
Community - Core community features engine.
"""
import logging
from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class UserMatcher:
    """Intelligent user matching based on pet profiles and interests."""

    def find_matches(self, user_profile: Dict, all_users: List[Dict],
                     pet_type: Optional[str] = None, breed: Optional[str] = None,
                     interests: Optional[List[str]] = None, limit: int = 10) -> List[Dict]:
        scored = []
        for other in all_users:
            if other["id"] == user_profile["id"]:
                continue
            score, reasons = self._calculate_match(user_profile, other, pet_type, breed, interests)
            if score > 0.1:
                scored.append({"user_id": other["id"], "username": other["username"],
                              "avatar_url": other.get("avatar_url"), "location": other.get("location"),
                              "pets": other.get("pets", []), "match_score": round(score, 2),
                              "match_reasons": reasons})
        scored.sort(key=lambda x: x["match_score"], reverse=True)
        return scored[:limit]

    def _calculate_match(self, user: Dict, other: Dict, pet_type: Optional[str],
                         breed: Optional[str], interests: Optional[List[str]]) -> tuple:
        score = 0.0
        reasons = []
        user_pets = user.get("pets", [])
        other_pets = other.get("pets", [])

        # Same pet type
        user_types = {p.get("pet_type") for p in user_pets}
        other_types = {p.get("pet_type") for p in other_pets}
        if user_types & other_types:
            score += 0.3
            reasons.append(f"Both have {', '.join(user_types & other_types)}")

        # Same breed
        user_breeds = {p.get("breed") for p in user_pets if p.get("breed")}
        other_breeds = {p.get("breed") for p in other_pets if p.get("breed")}
        if user_breeds & other_breeds:
            score += 0.3
            reasons.append(f"Same breed: {', '.join(user_breeds & other_breeds)}")

        # Location proximity (simplified)
        if user.get("location") and other.get("location") and user["location"] == other["location"]:
            score += 0.2
            reasons.append("Same location")

        # Interest overlap
        if interests:
            other_interests = set(other.get("interests", []))
            overlap = set(interests) & other_interests
            if overlap:
                score += 0.2 * min(len(overlap) / max(len(interests), 1), 1.0)
                reasons.append(f"Shared interests: {', '.join(list(overlap)[:3])}")

        return score, reasons


class ContentEngine:
    """Manages community posts and Q&A."""

    def format_post(self, post: Dict, author: Dict) -> Dict:
        return {
            "id": str(post.get("id", "")), "author_username": author.get("username", "anonymous"),
            "author_avatar": author.get("avatar_url"), "title": post.get("title", ""),
            "content": post.get("content", ""), "post_type": post.get("post_type", "experience"),
            "tags": post.get("tags", []), "images": post.get("images", []),
            "likes_count": post.get("likes_count", 0), "comments_count": post.get("comments_count", 0),
            "created_at": post.get("created_at", datetime.utcnow()),
        }

    def format_question(self, question: Dict, author: Dict, answers: Optional[List[Dict]] = None) -> Dict:
        return {
            "id": str(question.get("id", "")), "author_username": author.get("username", "anonymous"),
            "title": question.get("title", ""), "content": question.get("content", ""),
            "tags": question.get("tags", []), "images": question.get("images", []),
            "is_resolved": question.get("is_resolved", False),
            "expert_answered": question.get("expert_answered", False),
            "views_count": question.get("views_count", 0),
            "answers_count": question.get("answers_count", len(answers or [])),
            "created_at": question.get("created_at", datetime.utcnow()),
            "answers": answers or [],
        }


user_matcher = UserMatcher()
content_engine = ContentEngine()
