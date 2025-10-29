import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { signOut } from "firebase/auth";
import { auth } from "../../firebase";
import Community from "../Community";
import LogActivity from "../LogActivity/LogActivity";
import AiInsights from "../AiInsights";
import Predictions from "../Predictions";
import "./Dashboard.css";

export default function Dashboard({ currentUser }) {
  const navigate = useNavigate();
  const location = useLocation();

  const [activeSection, setActiveSection] = useState("dashboard");
  const [weeklyEmissions, setWeeklyEmissions] = useState([]);
  const [monthlyStats, setMonthlyStats] = useState({
    week_emissions: 0,
    month_emissions: 0,
    daily_average: 0,
    activity_count: 0,
  });
  const [achievements, setAchievements] = useState([]);
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(false);

  const API_BASE = "http://127.0.0.1:5000/api";

  // 🔁 Refresh dashboard data
  const refreshDashboardData = async () => {
    setLoading(true);
    try {
      
      const weeklyRes = await fetch(`${API_BASE}/stats/weekly-emissions`);
      const weeklyData = await weeklyRes.json();
      const formattedWeekly = Object.entries(weeklyData).map(([day, emission]) => ({
        day,
        emission,
      }));
      setWeeklyEmissions(formattedWeekly);

      const statsRes = await fetch(`${API_BASE}/stats/`);
      const statsData = await statsRes.json();
      setMonthlyStats({
        week_emissions: statsData.total_emission,
        month_emissions: statsData.total_emission,
        daily_average: statsData.average_emission,
        activity_count: statsData.total_activities,
      });

      const achievementsRes = await fetch(`${API_BASE}/achievements/`);
      const achievementsData = await achievementsRes.json();
      setAchievements(achievementsData);

      const activitiesRes = await fetch(`${API_BASE}/activities/`);
      const activitiesData = await activitiesRes.json();
      setActivities(activitiesData);
    } catch (err) {
      console.error("Error refreshing dashboard data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshDashboardData();
  }, [location]);
const handleClearAllData = async () => {
  if (!window.confirm("Clear all emissions and activity data?")) return;

  try {
    const res = await fetch(`${API_BASE}/activities/clear`, {  // <-- updated URL
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });

    if (!res.ok) throw new Error("Failed to clear data");

    const data = await res.json();
    alert(data.message || "Data cleared successfully!");
    setWeeklyEmissions([]);
    setMonthlyStats({
      week_emissions: 0,
      month_emissions: 0,
      daily_average: 0,
      activity_count: 0,
    });
    setAchievements([]);
    setActivities([]);
  } catch (err) {
    console.error("Error clearing data:", err);
    alert("Failed to clear data.");
  }
};

  const handleLogout = async () => {
    if (!window.confirm("Are you sure you want to log out?")) return;
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

            {/* Weekly Emissions Chart */}
            <section className="charts">
              <div className="chart">
                <h4>Weekly Emissions</h4>
                <div className="bars">
                  {weeklyEmissions.length > 0 ? (
                    weeklyEmissions.map(({ day, emission }) => (
                      <div className="bar" key={day}>
                        <small>{emission.toFixed(1)} kg</small>
                        <div
                          className="bar-fill"
                          style={{ height: `${Math.min(emission * 6, 100)}%` }}
                        ></div>
                        <small>{day}</small>
                      </div>
                    ))
                  ) : (
                    <p>No emissions data available</p>
                  )}
                </div>
              </div>
            </section>

            {/* Activities List */}
            <section className="activity-list">
              <h3>Recent Activities</h3>
              {activities.length > 0 ? (
                <ul>
                  {activities.map((a) => (
                    <li key={a.id}>
                      {a.date} — {a.category} — {a.emission} kg CO₂
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No activities logged yet.</p>
              )}
            </section>

            {/* Achievements */}
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
                          {badge.unlocked ? " Unlocked" : " Locked"}
                        </span>
                      </div>
                      <p className="badge-description">{badge.description}</p>
                    </div>
                  ))
                ) : (
                  <p>No achievements yet.</p>
                )}
              </div>
            </section>

            <section className="clear-section">
              <button className="clear-data" onClick={handleClearAllData}>
                 Clear All Data
              </button>
            </section>
          </>
        );

      case "log-activity":
        return <LogActivity currentUser={currentUser} onActivityLogged={refreshDashboardData} />;

      case "ai-insights":
        return <AiInsights currentUser={currentUser} />;

      case "predictions":
        return <Predictions currentUser={currentUser} />;

      case "community":
        return <Community currentUser={currentUser} />;

      default:
        return <p>Section not found.</p>;
    }
  };

  if (loading) return <p>Loading Dashboard...</p>;

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
