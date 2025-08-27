# src/analyzer/project_estimator.py
from typing import Dict, List
import json
import logging
from src.analyzer.business_analyzer import BusinessInsights

class ProjectEstimatorError(Exception):
    pass

class ProjectEstimator:
    def __init__(self):
        self.base_rates = {
            'ui_design': 150,  # per hour
            'frontend_dev': 120,
            'backend_dev': 140,
            'project_management': 100,
            'testing': 80
        }
        
        self.complexity_multipliers = {
            'simple': 1.0,
            'moderate': 1.5,
            'complex': 2.2,
            'enterprise': 3.0
        }
    
    def estimate_project_scope(self, business_insights: BusinessInsights, 
                             company_data: Dict) -> Dict:
        try:
            if not business_insights or not company_data:
                raise ProjectEstimatorError("Missing business insights or company data.")
            
            # Determine complexity based on company profile
            complexity = self._assess_complexity(company_data)
            
            # Base hour estimates for different phases
            base_hours = {
                'research_planning': 16,
                'ui_design': 40,
                'frontend_development': 60,
                'backend_development': 45,
                'testing_qa': 25,
                'project_management': 30
            }
            
            # Apply complexity multiplier
            multiplier = self.complexity_multipliers[complexity]
            adjusted_hours = {phase: int(hours * multiplier) 
                             for phase, hours in base_hours.items()}
            
            # Calculate costs
            total_cost = self._calculate_total_cost(adjusted_hours)
            
            return {
                'complexity_level': complexity,
                'phase_breakdown': adjusted_hours,
                'total_hours': sum(adjusted_hours.values()),
                'estimated_cost': total_cost,
                'timeline_weeks': max(4, sum(adjusted_hours.values()) // 40),
                'team_composition': self._recommend_team(complexity),
                'deliverables': self._generate_deliverables_list(complexity)
            }
        except ProjectEstimatorError as e:
            logging.error(f"ProjectEstimator error: {e}")
            return {"error": str(e)}
        except Exception as e:
            logging.error(f"Unexpected error in ProjectEstimator: {e}")
            return {"error": "Failed to estimate project scope."}
    
    def _assess_complexity(self, company_data: Dict) -> str:
        """Assess project complexity based on company characteristics"""
        complexity_score = 0
        
        # Factor in tech stack sophistication
        tech_stack = company_data.get('tech_stack', [])
        if any(tech.lower() in ['react', 'vue', 'angular'] for tech in tech_stack):
            complexity_score += 2
        
        # Factor in services complexity
        services = company_data.get('services', [])
        if len(services) > 5:
            complexity_score += 1
        
        # Factor in estimated team size
        team_size = company_data.get('team_size', 0)
        if team_size > 50:
            complexity_score += 2
        elif team_size > 10:
            complexity_score += 1
        
        if complexity_score >= 4:
            return 'enterprise'
        elif complexity_score >= 2:
            return 'complex'
        elif complexity_score >= 1:
            return 'moderate'
        else:
            return 'simple'
