"""
Knowledge Graph - Core engine for veterinary knowledge graph.
"""
import logging
from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

DISEASE_DATABASE: Dict[str, List[Dict]] = {
    "dog": [
        {
            "name": "Canine Parvovirus",
            "symptoms": ["vomiting", "diarrhea", "lethargy", "loss_of_appetite", "fever", "dehydration"],
            "severity": "severe", "urgency": "emergency",
            "description": "A highly contagious viral illness affecting dogs, especially puppies.",
            "common_symptoms": ["severe bloody diarrhea", "vomiting", "lethargy", "fever"],
            "actions": ["Immediate veterinary care required", "IV fluid therapy", "Antiemetic medication", "Antibiotic therapy"],
        },
        {
            "name": "Kennel Cough",
            "symptoms": ["cough", "sneezing", "runny_nose", "lethargy", "loss_of_appetite"],
            "severity": "mild", "urgency": "medium",
            "description": "A highly contagious respiratory disease in dogs.",
            "common_symptoms": ["dry hacking cough", "retching", "runny nose"],
            "actions": ["Rest and isolation", "Ensure adequate hydration", "Humidify the environment", "Consult vet if symptoms persist"],
        },
        {
            "name": "Hip Dysplasia",
            "symptoms": ["limping", "difficulty_standing", "reluctance_to_exercise", "bunny_hopping", "stiffness"],
            "severity": "moderate", "urgency": "medium",
            "description": "An abnormal formation of the hip socket causing arthritis and lameness.",
            "common_symptoms": ["decreased activity", "bunny hopping gait", "difficulty rising", "hind limb lameness"],
            "actions": ["Weight management", "Controlled exercise", "Joint supplements", "Anti-inflammatory medication"],
        },
        {
            "name": "Skin Allergies",
            "symptoms": ["itching", "scratching", "red_skin", "hair_loss", "ear_infections", "hot_spots"],
            "severity": "mild", "urgency": "low",
            "description": "Allergic dermatitis caused by food, environmental, or flea allergies.",
            "common_symptoms": ["excessive scratching", "red irritated skin", "hair loss"],
            "actions": ["Identify and remove allergen", "Medicated shampoo", "Antihistamines", "Flea prevention"],
        },
        {
            "name": "Gastric Dilatation-Volvulus (Bloat)",
            "symptoms": ["distended_abdomen", "restlessness", "unproductive_vomiting", "excessive_drooling", "rapid_breathing"],
            "severity": "severe", "urgency": "emergency",
            "description": "A life-threatening condition where the stomach fills with gas and twists.",
            "common_symptoms": ["swollen abdomen", "non-productive retching", "restlessness", "rapid breathing"],
            "actions": ["EMERGENCY: Go to vet immediately", "Do not give food or water", "Time is critical"],
        },
    ],
    "cat": [
        {
            "name": "Feline Upper Respiratory Infection",
            "symptoms": ["sneezing", "runny_nose", "eye_discharge", "lethargy", "loss_of_appetite", "fever"],
            "severity": "mild", "urgency": "low",
            "description": "Common viral infection in cats, usually self-limiting.",
            "common_symptoms": ["sneezing", "nasal discharge", "conjunctivitis"],
            "actions": ["Keep warm and comfortable", "Ensure hydration", "Gentle nasal cleaning", "Consult vet if worsens"],
        },
        {
            "name": "Feline Lower Urinary Tract Disease (FLUTD)",
            "symptoms": ["frequent_urination", "straining_to_urinate", "blood_in_urine", "crying_while_urinating"],
            "severity": "moderate", "urgency": "high",
            "description": "Common condition affecting bladder and urethra. Life-threatening if blockage occurs.",
            "common_symptoms": ["straining in litter box", "blood in urine", "vocalizing while urinating"],
            "actions": ["Consult vet immediately if male cat", "Increase water intake", "Canned food diet", "Monitor closely"],
        },
    ],
}

NUTRITION_DATABASE: Dict[str, Dict] = {
    "dog": {
        "puppy": {
            "calorie_multiplier": 2.0, "protein_pct": 25, "fat_pct": 15,
            "key_nutrients": [
                {"nutrient": "Protein", "amount": "56g/day (for 10kg)", "importance": "essential", "notes": "High-quality animal protein for growth"},
                {"nutrient": "Calcium", "amount": "0.5-0.8% of diet", "importance": "essential", "notes": "Critical for bone development"},
                {"nutrient": "DHA", "amount": "0.1-0.3% of diet", "importance": "essential", "notes": "Brain and eye development"},
            ],
            "foods_to_avoid": ["chocolate", "grapes", "raisins", "onions", "garlic", "xylitol", "macadamia nuts"],
            "feeding_schedule": {"meals_per_day": "3-4", "timing": "Every 4-6 hours"},
        },
        "adult": {
            "calorie_multiplier": 1.0, "protein_pct": 18, "fat_pct": 10,
            "key_nutrients": [
                {"nutrient": "Protein", "amount": "25g/day (for 10kg)", "importance": "essential", "notes": "Maintain muscle mass"},
                {"nutrient": "Fiber", "amount": "2-5% of diet", "importance": "recommended", "notes": "Digestive health"},
                {"nutrient": "Omega-3 Fatty Acids", "amount": "0.1% of diet", "importance": "recommended", "notes": "Skin, coat, and joint health"},
            ],
            "foods_to_avoid": ["chocolate", "grapes", "raisins", "onions", "garlic", "xylitol", "alcohol", "coffee"],
            "feeding_schedule": {"meals_per_day": "2", "timing": "Morning and evening"},
        },
        "senior": {
            "calorie_multiplier": 0.8, "protein_pct": 20, "fat_pct": 8,
            "key_nutrients": [
                {"nutrient": "Protein", "amount": "25g/day (for 10kg)", "importance": "essential", "notes": "Prevent muscle wasting"},
                {"nutrient": "Glucosamine", "amount": "20mg/kg body weight", "importance": "recommended", "notes": "Joint support"},
            ],
            "foods_to_avoid": ["high-fat foods", "excessive sodium", "raw eggs", "small bones"],
            "feeding_schedule": {"meals_per_day": "2-3", "timing": "Regular schedule"},
        },
    },
    "cat": {
        "adult": {
            "calorie_multiplier": 1.0, "protein_pct": 30, "fat_pct": 12,
            "key_nutrients": [
                {"nutrient": "Taurine", "amount": "250mg/day", "importance": "essential", "notes": "Heart and eye health"},
                {"nutrient": "Protein", "amount": "40g/day (for 4kg)", "importance": "essential", "notes": "Obligate carnivore"},
                {"nutrient": "Vitamin A", "amount": "3333 IU/kg diet", "importance": "essential", "notes": "Cannot convert beta-carotene"},
            ],
            "foods_to_avoid": ["onions", "garlic", "chocolate", "grapes", "lily plants", "dog food"],
            "feeding_schedule": {"meals_per_day": "3-5", "timing": "Throughout the day"},
        },
    },
}


class SymptomChecker:
    """AI-powered symptom checker using veterinary knowledge graph."""

    def analyze_symptoms(self, symptoms: List[str], pet_type: str, breed: Optional[str] = None,
                         age_years: Optional[float] = None, duration_days: Optional[int] = None,
                         severity: Optional[str] = None) -> Tuple[List[Dict], str]:
        diseases = DISEASE_DATABASE.get(pet_type, DISEASE_DATABASE.get("dog", []))
        symptom_set = set(s.lower().replace(" ", "_") for s in symptoms)
        matches = []
        for disease in diseases:
            disease_symptoms = set(disease["symptoms"])
            overlap = symptom_set & disease_symptoms
            if overlap:
                union = symptom_set | disease_symptoms
                confidence = len(overlap) / len(union) if union else 0
                severity_multiplier = 1.0
                if severity == "severe" and disease["urgency"] in ("high", "emergency"):
                    severity_multiplier = 1.2
                if duration_days and duration_days > 7:
                    severity_multiplier *= 1.1
                confidence = min(confidence * severity_multiplier, 1.0)
                if confidence > 0.1:
                    matches.append({
                        "disease_name": disease["name"], "confidence": round(confidence, 2),
                        "description": disease["description"], "common_symptoms": disease["common_symptoms"],
                        "severity": disease["severity"], "urgency": disease["urgency"],
                        "recommended_actions": disease["actions"],
                        "veterinary_consult_recommended": disease["urgency"] in ("high", "emergency"),
                    })
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        summary = self._generate_summary(matches, symptoms, severity)
        return matches[:5], summary

    def _generate_summary(self, matches: List[Dict], symptoms: List[str], severity: Optional[str]) -> str:
        if not matches:
            return "No matching conditions found. Monitor your pet and consult a veterinarian if symptoms persist."
        top = matches[0]
        urgent = any(m["urgency"] == "emergency" for m in matches)
        if urgent:
            return (f"⚠️ URGENT: Based on symptoms '{', '.join(symptoms)}', there may be a serious condition "
                    f"requiring immediate veterinary attention. Top match: {top['disease_name']} ({top['confidence']:.0%}).")
        return (f"Based on symptoms '{', '.join(symptoms)}', most likely: {top['disease_name']} ({top['confidence']:.0%}). "
                f"{'Consult a veterinarian.' if top['veterinary_consult_recommended'] else 'Monitor closely.'}")


class NutritionEngine:
    """Provides personalized nutrition recommendations."""

    def get_recommendations(self, pet_type: str, breed: Optional[str] = None,
                            age_years: Optional[float] = None, weight_kg: Optional[float] = None,
                            activity_level: Optional[str] = None, health_conditions: Optional[List[str]] = None,
                            life_stage: Optional[str] = None) -> Dict:
        if not life_stage:
            life_stage = self._estimate_life_stage(pet_type, age_years)
        base = NUTRITION_DATABASE.get(pet_type, {}).get(life_stage, NUTRITION_DATABASE.get(pet_type, {}).get("adult", {}))
        if weight_kg:
            rer = 70 * (weight_kg ** 0.75)
            multiplier = base.get("calorie_multiplier", 1.0)
            if activity_level == "high": multiplier *= 1.4
            elif activity_level == "low": multiplier *= 0.8
            daily_calories = round(rer * multiplier, 1)
        else:
            daily_calories = 800.0
        nutrients = [{"nutrient": n["nutrient"], "recommended_daily_amount": n["amount"], "unit": "varies",
                       "importance": n["importance"], "notes": n.get("notes")} for n in base.get("key_nutrients", [])]
        food_suggestions = [
            {"food_category": "High-quality commercial food", "examples": [f"Premium {pet_type} food for {life_stage}"],
             "benefits": ["Balanced nutrition", "Convenient"]},
            {"food_category": "Lean proteins", "examples": ["Chicken breast", "Turkey", "Fish"],
             "benefits": ["Muscle maintenance", "Omega-3"]},
        ]
        special_notes = []
        if health_conditions:
            for c in health_conditions:
                special_notes.append(f"Adjust diet for {c} - consult veterinarian")
        return {
            "pet_profile": {"pet_type": pet_type, "breed": breed, "age_years": age_years,
                            "weight_kg": weight_kg, "activity_level": activity_level, "life_stage": life_stage},
            "daily_calorie_target": daily_calories, "nutrient_recommendations": nutrients,
            "food_suggestions": food_suggestions, "foods_to_avoid": base.get("foods_to_avoid", []),
            "feeding_schedule": base.get("feeding_schedule", {}), "special_notes": special_notes,
        }

    def _estimate_life_stage(self, pet_type: str, age_years: Optional[float]) -> str:
        if not age_years: return "adult"
        thresholds = {"dog": (1.0, 7.0), "cat": (1.0, 10.0)}
        puppy_max, senior_min = thresholds.get(pet_type, (1.0, 7.0))
        if age_years < puppy_max: return "puppy"
        elif age_years >= senior_min: return "senior"
        return "adult"


class KnowledgeSearchEngine:
    """Search engine for veterinary knowledge base."""

    def search(self, query: str, pet_type: Optional[str] = None,
               category: Optional[str] = None, limit: int = 10) -> Tuple[List[Dict], List[str]]:
        results = []
        query_lower = query.lower()
        keywords = query_lower.split()
        all_articles = [
            {"id": "art-001", "title": "Understanding Canine Vaccination Schedule",
             "content": "Core vaccines for dogs include rabies, distemper, parvovirus, and adenovirus...",
             "category": "general", "tags": ["vaccination", "puppy", "prevention"],
             "pet_types": ["dog"], "source": "Veterinary Medicine Guide", "last_updated": datetime(2024, 1, 15)},
            {"id": "art-002", "title": "Cat Nutrition: Complete Guide",
             "content": "Cats are obligate carnivores requiring specific nutrients like taurine...",
             "category": "nutrition", "tags": ["nutrition", "cat", "diet"],
             "pet_types": ["cat"], "source": "Feline Health Institute", "last_updated": datetime(2024, 2, 20)},
            {"id": "art-003", "title": "Pet First Aid Essentials",
             "content": "Every pet owner should know basic first aid: CPR, wound care, poisoning response...",
             "category": "first_aid", "tags": ["first_aid", "emergency", "cpr"],
             "pet_types": ["dog", "cat"], "source": "Red Cross Pet Safety", "last_updated": datetime(2024, 3, 10)},
        ]
        for article in all_articles:
            if category and article["category"] != category: continue
            if pet_type and pet_type not in article["pet_types"]: continue
            score = sum(1 for kw in keywords if kw in article["title"].lower() or kw in article["content"].lower())
            score /= max(len(keywords), 1)
            if score > 0:
                article["relevance_score"] = round(score, 2)
                results.append(article)
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        suggestions = [] if len(results) >= 3 else ["Try more specific keywords"]
        return results[:limit], suggestions


symptom_checker = SymptomChecker()
nutrition_engine = NutritionEngine()
knowledge_search = KnowledgeSearchEngine()
