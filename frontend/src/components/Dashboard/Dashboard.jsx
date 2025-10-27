import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { signOut } from "firebase/auth";
import { auth } from "../../firebase";
import Community from "../Community";
import LogActivity from "../LogActivity/LogActivity";
import AiInsights from "../AiInsights";
import Predictions from "../Predictions";
import "./Dashboard.css";

export default function Dashboard() {
  const navigate = useNavigate();

  const [activeSection, setActiveSection] = useState("dashboard");
  const [weeklyEmissions, setWeeklyEmissions] = useState([]);
  const [monthlyStats, setMonthlyStats] = useState({
    week_emissions: 0,
    month_emissions: 0,
    daily_average: 0,
    activity_count: 0,
  });
  const [achievements, setAchievements] = useState([]);
  const [aiInsights, setAiInsights] = useState("");
  const [loading, setLoading] = useState(false);

  const refreshDashboardData = async () => {
    setLoading(true);
    try {
      const weeklyRes = await fetch("http://127.0.0.1:5000/api/emissions/weekly");
      const weeklyData = await weeklyRes.json();
      const formattedWeekly = Object.entries(weeklyData).map(([day, emission]) => ({
        day,
        emission,
      }));
      setWeeklyEmissions(formattedWeekly);

      const statsRes = await fetch("http://127.0.0.1:5000/api/stats");
      const statsData = await statsRes.json();
      setMonthlyStats(statsData);

      const achievementsRes = await fetch("http://127.0.0.1:5000/api/achievements")
      const achievementsData = await achievementsRes.json();
      setAchievements(achievementsData);
    } catch (err) {
      console.error("Error refreshing dashboard data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshDashboardData();
  }, []);


  const handleClearAllData = async () => {
    const confirmClear = window.confirm("Clear all emissions and activity data?");
    if (!confirmClear) return;

    try {
      const res = await fetch("http://127.0.0.1:5000/api/clear", {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
      });

      const data = await res.json();
      alert(data.message || "Data cleared successfully!");

      setWeeklyEmissions([]);
      setMonthlyStats({
        week_emissions: 0,
        month_emissions: 0,
        daily_average: 0,
        activity_count: 0,
      });
      setAiInsights("");
      setAchievements([]);
    } catch (err) {
      console.error("Error clearing data:", err);
      alert("Failed to clear data.");
    }
  };
  const handleLogout = async () => {
    const confirmLogout = window.confirm("Are you sure you want to log out?");
    if (!confirmLogout) return;

    try {
      await signOut(auth);
      localStorage.removeItem("user");
      sessionStorage.clear();
      alert("You’ve been logged out successfully.");
      navigate("/login", { replace: true });
    } catch (error) {
      console.error("Logout failed:", error);
      alert("Failed to log out. Please try again.");
    }
  };

  const renderSection = () => {
    switch (activeSection) {
      case "dashboard":
        return (
          <>
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
                Clear All Data
              </button>
            </section>

            {loading && <p style={{ textAlign: "center" }}>Updating dashboard...</p>}
          </>
        );

      case "log-activity":
        return <LogActivity onActivityLogged={refreshDashboardData} />;

      case "ai-insights":
        return <AiInsights />;

      case "predictions":
        return <Predictions />;

      case "community":
        return <Community />;

      default:
        return <p>Section not found.</p>;
    }
  };

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>GreenPath</h2>
        <nav className="nav">
          <ul className="nav-links">
            <li><button onClick={() => setActiveSection("dashboard")}>Dashboard</button></li>
            <li><button onClick={() => setActiveSection("log-activity")}>Log Activity</button></li>
            <li><button onClick={() => setActiveSection("ai-insights")}>AI Insights</button></li>
            <li><button onClick={() => setActiveSection("predictions")}>Predictions</button></li>
            <li><button onClick={() => setActiveSection("community")}>Community</button></li>
          </ul>

          <div className="logout">
            <button onClick={handleLogout}>Logout</button>
          </div>
        </nav>
      </aside>

      <main className="main">{renderSection()}</main>
    </div>
  );
}
