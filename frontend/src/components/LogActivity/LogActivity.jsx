import React from "react";
import { useNavigate } from "react-router-dom";
import "./LogActivity.css";
import ActivityForm from "./ActivityForm";

export default function LogActivity() {
  const navigate = useNavigate();

  return (
    <div className="log-activity">
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
            <button onClick={() => {
              localStorage.clear();
              sessionStorage.clear();
              alert("Logged out successfully.");
              navigate("/login", { replace: true });
              window.location.reload();
            }}>
              Logout
            </button>
          </div>
        </nav>
      </aside>

      <main className="main">
        <section className="form-panel">
          <h3>Log a New Activity</h3>
          <ActivityForm />
        </section>
      </main>
    </div>
  );
}
