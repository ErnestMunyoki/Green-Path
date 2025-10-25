from services.ai_insights import AIInsightsService

# Test a sample activity
result = AIInsightsService.generate_insight(
    "Car commute 10km",
    distance_km=10,
    vehicle_type="car"
)

print("AI Insight Test Result:")
print(result)

