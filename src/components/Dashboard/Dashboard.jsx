import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

export default function Dashboard() {
  const navigate = useNavigate();

  const [weeklyEmissions, setWeeklyEmissions] = useState([]);
  const [monthlyStats, setMonthlyStats] = useState({
    week_emissions: 0,
    month_emissions: 0,
    daily_average: 0,
    activity_count: 0
  });
  const [achievements, setAchievements] = useState([]);
  const [aiInsights, setAiInsights] = useState("");

  // Fetch weekly emissions
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

  // Fetch monthly stats
  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/stats")
      .then((res) => res.json())
      .then((data) => setMonthlyStats(data))
      .catch((err) => console.error("Error fetching monthly stats:", err));
  }, []);

  // Fetch achievements
  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/achievements")
      .then((res) => res.json())
      .then((data) => setAchievements(data))
      .catch((err) => console.error("Error fetching achievements:", err));
  }, []);

  // Fetch AI insights
  useEffect(() => {
    if (weeklyEmissions.length > 0) {
      fetch("http://127.0.0.1:5000/api/ai/insights", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ emissions: weeklyEmissions }),
      })
        .then((res) => res.json())
        .then((data) => setAiInsights(data.insights))
        .catch((err) => console.error("Error fetching AI insights:", err));
    }
  }, [weeklyEmissions]);

  // Clear all data
  const handleClearAllData = async () => {
    const confirmClear = window.confirm("Clear all emissions and activity data?");
    if (!confirmClear) return;

    try {
      const res = await fetch("http://127.0.0.1:5000/api/clear", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });

      const data = await res.json();
      alert(data.message || "Data cleared successfully!");

      // Reset frontend state
      setWeeklyEmissions([]);
      setMonthlyStats({
        week_emissions: 0,
        month_emissions: 0,
        daily_average: 0,
        activity_count: 0
      });
      setAiInsights("");
    } catch (err) {
      console.error("Error clearing data:", err);
      alert("Failed to clear data.");
    }
  };

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>GreenPath</h2>
        <nav className="nav">
          <ul className="nav-links">
            <li><button onClick={() => navigate("/")}>Dashboard</button></li>
            <li><button onClick={() => navigate("/log-activity")}>Log Activity</button></li>
            <li><button onClick={() => navigate("/ai-insights")}>AI Insights</button></li>
            <li><button onClick={() => navigate("/predictions")}>Predictions</button></li>
            <li><button onClick={() => navigate("/community")}>Community</button></li>
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
            <div className="value">{monthlyStats.week_emissions} kg CO₂</div>
          </div>

          <div className="card">
            <h4>This Month</h4>
            <div className="value">{monthlyStats.month_emissions} kg CO₂</div>
            <div className="note">
              Daily Avg: {monthlyStats.daily_average} kg CO₂<br />
              {monthlyStats.activity_count} activities logged
            </div>
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

        <section className="clear-section">
          <button className="clear-data" onClick={handleClearAllData}>
            🧹 Clear All Data
          </button>
        </section>
      </main>
    </div>
  );
}





