"""财务教育包"""
from backend.financial_education.engine import EducationEngine
from backend.financial_education.api import router

__all__ = ["EducationEngine", "router"]
