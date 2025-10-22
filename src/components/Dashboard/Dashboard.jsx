import React, { useEffect, useState } from "react";
import "./Dashboard.css";

export default function Dashboard() {
  const [weeklyEmissions, setWeeklyEmissions] = useState([]);
  const [achievements, setAchievements] = useState([]);
  const [aiInsights, setAiInsights] = useState(""); // AI insights state

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/emissions/weekly")
      .then((res) => res.json())
      .then((data) => {
        const formatted = Object.entries(data).map(([day, emission]) => ({
          day,
          emission,
        }));
        setWeeklyEmissions(formatted);
      })
      .catch((err) => console.error("Error fetching emissions:", err));
  }, []);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/achievements")
      .then((res) => res.json())
      .then((data) => setAchievements(data))
      .catch((err) => console.error("Error fetching achievements:", err));
  }, []);

  useEffect(() => {
    if (weeklyEmissions.length > 0) {
      fetch("http://127.0.0.1:5000/api/ai/insights", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ emissions: weeklyEmissions }),
      })
        .then((res) => res.json())
        .then((data) => setAiInsights(data.insights || "No insights available"))
        .catch((err) => console.error("Error fetching AI insights:", err));
    }
  }, [weeklyEmissions]);

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>GreenPath</h2>
        <nav className="nav">
          <ul className="nav-links">
            <li>
              <button onClick={() => console.log("Go to Dashboard")}>
                Dashboard
              </button>
            </li>
            <li>
              <button onClick={() => console.log("Go to Log Activity")}>
                Log Activity
              </button>
            </li>
            <li>
              <button onClick={() => console.log("Go to AI Insights")}>
                AI Insights
              </button>
            </li>
            <li>
              <button onClick={() => console.log("Go to Predictions")}>
                Predictions
              </button>
            </li>
            <li>
              <button onClick={() => console.log("Go to Community")}>
                Community
              </button>
            </li>
          </ul>
          <div className="logout">
            <button onClick={() => console.log("Logging out...")}>Logout</button>
          </div>
        </nav>
      </aside>

      <main className="main">
        <section className="summary">
          <div className="card">
            <h4>This Week</h4>
            <div className="value">
              {weeklyEmissions
                .reduce((acc, d) => acc + d.emission, 0)
                .toFixed(2)}{" "}
              kg CO₂
            </div>
            <div className="note">{weeklyEmissions.length} days tracked</div>
          </div>

          <div className="card">
            <h4>Achievements</h4>
            <div className="value">
              {achievements.filter((a) => a.unlocked).length} / {achievements.length}
            </div>
            <div className="note">Keep going!</div>
          </div>
        </section>

        <section className="charts">
          <div className="chart">
            <h4>Weekly Emissions</h4>
            <div className="bars">
              {weeklyEmissions.length > 0 ? (
                weeklyEmissions.map(({ day, emission }) => {
                  const height = `${Math.max(emission * 6, 10)}%`;
                  return (
                    <div className="bar" key={day}>
                      <small>{emission.toFixed(1)} kg</small>
                      <div className="bar-fill" style={{ height }}></div>
                      <small>{day}</small>
                    </div>
                  );
                })
              ) : (
                <p>No emissions data available</p>
              )}
            </div>
          </div>
        </section>

        <section className="ai-insights">
          <h3>AI Insights</h3>
          <div className="card">
            <p>{aiInsights || "Loading insights..."}</p>
          </div>
        </section>

        <section className="achievements">
          <h3>Your Achievements</h3>
          <div className="badge-grid">
            {achievements.map((badge) => (
              <div
                key={badge.title}
                className={`badge ${badge.unlocked ? "unlocked" : "locked"}`}
              >
                <h5>{badge.title}</h5>
                <p>{badge.unlocked ? "Unlocked" : "Locked"}</p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
