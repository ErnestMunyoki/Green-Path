import React, { useState, useEffect } from "react";
import "../App.css";

const AiInsights = () => {
  const [insight, setInsight] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // ✅ Load the most recent AI insight from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("latest_ai_insight");
    if (saved) {
      setInsight(JSON.parse(saved));
    }
  }, []);

  // ✅ Fetch AI-generated sustainability insight (POST)
  const handleGenerateInsight = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/ai/estimate-emission", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        // 🧠 You can later replace this with real data from your activity log
        body: JSON.stringify({
          name: "Car commute (10km)",
          user_id: 1,
          distance_km: 10,
          vehicle_type: "petrol",
        }),
      });

      if (!response.ok) throw new Error("Failed to generate insight");

      const data = await response.json();

      // ✅ Save and display the AI-generated insight
      setInsight(data);
      localStorage.setItem("latest_ai_insight", JSON.stringify(data));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-container">
      <h2>AI Sustainability Insights</h2>
      <p>
        Let our AI analyze your recent activities and suggest how to reduce your
        carbon footprint.
      </p>

      <button
        onClick={handleGenerateInsight}
        className="generate-btn"
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Generate AI Insight"}
      </button>

      {error && <p className="error">⚠️ {error}</p>}

      {insight && (
        <div className="insight-box">
          <h3>AI Insight</h3>
          <p><strong>Activity:</strong> {insight.activity}</p>
          <p><strong>Emission:</strong> {insight.emission} kg CO₂</p>
          <p><strong>Problem:</strong> {insight.problem}</p>
          <p><strong>Recommendation:</strong> {insight.recommendation}</p>
          <p><strong>Solution:</strong> {insight.solution}</p>
        </div>
      )}
    </div>
  );
};

export default AiInsights;
