import React, { useState } from "react";
import "../App.css";

const AiInsights = () => {
  const [insight, setInsight] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateInsight = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/ai/estimate-emission", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: 1, // can be replaced by actual logged-in user
        }),
      });

      if (!response.ok) throw new Error("Failed to generate insight");

      const data = await response.json();
      setInsight(data.insight);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-container">
      <h2>🌿 AI Sustainability Insights</h2>
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
          <h3>Insight Result:</h3>
          <p>{insight}</p>
        </div>
      )}
    </div>
  );
};

export default AiInsights;
