import React, { useState, useEffect } from "react";
import "../App.css";

const AiInsights = () => {
  const [insight, setInsight] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // ✅ Load last AI insight from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("latest_ai_insight");
    if (saved) {
      setInsight(JSON.parse(saved));
    }
  }, []);

  const handleGenerateInsight = async () => {
    setLoading(true);
    setError(null);

    try {
      // ✅ Use your real AI backend route
      const response = await fetch("http://127.0.0.1:5000/api/log-activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          category: "Commuting",
          emission: 0.3,
          date: "2025-10-24",
          description: "Boiled water with charcoal",
        }),
      });

      if (!response.ok) throw new Error("Failed to generate insight");

      const data = await response.json();

      // ✅ Handle Gemini-style response
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
          <p><strong>Activity:</strong> {insight.activity || "Boiled water with charcoal"}</p>
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
