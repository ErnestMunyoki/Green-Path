# services/ai_insights.py
import random

class AIInsightsService:
    """
    Simple AI logic to estimate emissions, identify problems,
    and provide helpful sustainability recommendations.
    """

    # Default emission factors for simple estimation
    EMISSION_FACTORS = {
        "car": 0.23,    # kg CO2 per km
        "bus": 0.1,
        "bike": 0.0,
        "walking": 0.0,
        "other": 0.05,
    }

    @staticmethod
    def estimate_emission(activity_name, distance_km=0, vehicle_type="other"):
        """
        Estimate emission based on activity and vehicle type.
        """
        # Base emission from distance
        base_factor = AIInsightsService.EMISSION_FACTORS.get(vehicle_type.lower(), 0.05)
        emission = round(float(distance_km) * base_factor, 2)

        # For random lifestyle activities like "watching TV" or "farting"
        random_low_emissions = {
            "watching tv": 0.02,
            "farting": 0.001,
            "sleeping": 0.0,
            "cooking": 0.3,
            "showering": 0.4,
            "eating meat": 1.5,
            "using phone": 0.05,
        }
        for key, val in random_low_emissions.items():
            if key in activity_name.lower():
                emission = val

        return emission

    @staticmethod
    def analyze_activity(activity_name, emission):
        """
        Determine the problem and suggest a recommendation.
        """
        # Simple AI logic: classify emission level
        if emission == 0:
            problem = f"No carbon emissions detected from '{activity_name}'."
            solution = "Great! Keep engaging in low-carbon activities."
        elif emission < 0.5:
            problem = f"'{activity_name}' has a small carbon impact."
            solution = "Good job! Consider reducing energy use where possible."
        elif emission < 2:
            problem = f"'{activity_name}' contributes moderately to CO₂ emissions."
            solution = "You could reduce this by using greener habits or alternatives."
        else:
            problem = f"'{activity_name}' has a high carbon footprint."
            solution = "Consider replacing it with low-emission activities."

        return problem, solution

    @staticmethod
    def generate_insight(activity_name, distance_km=0, vehicle_type="other"):
        """
        Full pipeline: estimate emission + analyze + return recommendation.
        """
        emission = AIInsightsService.estimate_emission(
            activity_name, distance_km, vehicle_type
        )

        problem, solution = AIInsightsService.analyze_activity(activity_name, emission)

        return {
            "activity": activity_name,
            "emission": emission,
            "problem": problem,
            "solution": solution,
            "recommendation": solution,
        }
