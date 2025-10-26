import React from "react";
import { useNavigate } from "react-router-dom";
import "./LogActivity.css";
import ActivityForm from "./ActivityForm";
import { signOut } from "firebase/auth";
import { auth } from "../../firebase";

export default function LogActivity() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    if (window.confirm("Are you sure you want to log out?")) {
      await signOut(auth);
      localStorage.removeItem("user");
      navigate("/login");
    }
  };

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
            <button onClick={handleLogout}>Logout</button>
          </div>
        </nav>
      </aside>

      <main className="main">
        <section className="form-panel">
          <ActivityForm />
        </section>
      </main>
    </div>
  );
}
