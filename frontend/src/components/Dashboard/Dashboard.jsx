import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

export default function Dashboard() {
  const navigate = useNavigate();

  const API_BASE = "http://127.0.0.1:5000/api";

  const [weeklyEmissions, setWeeklyEmissions] = useState([]);
  const [monthlyStats, setMonthlyStats] = useState({
    week_emissions: 0,
    month_emissions: 0,
    daily_average: 0,
    activity_count: 0,
  });
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);

  // Generic fetch helper
  const fetchData = async (endpoint, setState) => {
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
      const data = await res.json();
      setState(data);
    } catch (err) {
      console.error(`Error fetching ${endpoint}:`, err);
    }
  };

  // Fetch weekly emissions
  useEffect(() => {
    fetchData("/emissions/weekly", (data) => {
      const formatted = Object.entries(data).map(([day, emission]) => ({
        day,
        emission,
      }));
      setWeeklyEmissions(formatted);
    });
  }, []);

  // Fetch monthly stats
  useEffect(() => {
    fetchData("/stats", setMonthlyStats);
  }, []);

  // Fetch achievements
  useEffect(() => {
    fetchData("/achievements/", setAchievements); // <-- Added trailing slash
    setLoading(false);
  }, []);

  // Clear all data handler
  const handleClearAllData = async () => {
    const confirmClear = window.confirm("Clear all emissions and activity data?");
    if (!confirmClear) return;

    try {
      const res = await fetch(`${API_BASE}/clear`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });

      const data = await res.json();
      alert(data.message || "Data cleared successfully!");

      // Reset all states
      setWeeklyEmissions([]);
      setMonthlyStats({
        week_emissions: 0,
        month_emissions: 0,
        daily_average: 0,
        activity_count: 0,
      });
      setAchievements([]);
    } catch (err) {
      console.error("Error clearing data:", err);
      alert("Failed to clear data.");
    }
  };

  if (loading) return <p>Loading Dashboard...</p>;

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>GreenPath</h2>
        <nav className="nav">
          <ul className="nav-links">
            <li><button onClick={() => navigate("/")}>Dashboard</button></li>
            <li><button onClick={() => navigate("/ai-insights")}>AI Insights</button></li>
            <li><button onClick={() => navigate("/log-activity")}>Log Activity</button></li>
            <li><button onClick={() => navigate("/predictions")}>Predictions</button></li>
            <li><button onClick={() => navigate("/community")}>Community</button></li>
          </ul>
          <div className="logout">
            <button onClick={() => console.log("Logging out...")}>Logout</button>
          </div>
        </nav>
      </aside>

      <main className="main">
        {/* Summary Cards */}
        <section className="summary">
          <div className="card">
            <h4>This Week</h4>
            <div className="value">{monthlyStats.week_emissions} kg CO₂</div>
            <div className="note">7 days tracked</div>
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
              {achievements.filter(a => a.unlocked).length} / {achievements.length}
            </div>
            <div className="note">Keep going!</div>
          </div>
        </section>

        {/* Weekly Emissions Chart */}
        <section className="charts">
          <div className="chart">
            <h4>Weekly Emissions</h4>
            <div className="bars">
              {weeklyEmissions.length > 0 ? (
                weeklyEmissions.map(({ day, emission }) => {
                  const height = `${Math.min(emission * 6, 100)}%`;
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

        {/* Achievements Section */}
        <section className="achievements">
          <h3>Your Achievements</h3>
          <div className="badge-grid">
            {achievements.length > 0 ? (
              achievements.map((badge) => (
                <div
                  key={badge.title}
                  className={`badge ${badge.unlocked ? "unlocked" : "locked"}`}
                >
                  <div className="badge-header">
                    <h5>{badge.title}</h5>
                    <span className="status">
                      {badge.unlocked ? "✅ Unlocked" : "🔒 Locked"}
                    </span>
                  </div>
                  <p className="badge-description">{badge.description}</p>
                </div>
              ))
            ) : (
              <p>No achievements available yet.</p>
            )}
          </div>
        </section>

        {/* Clear All Data */}
        <section className="clear-section">
          <button className="clear-data" onClick={handleClearAllData}>
            🧹 Clear All Data
          </button>
        </section>
      </main>
    </div>
  );
}
