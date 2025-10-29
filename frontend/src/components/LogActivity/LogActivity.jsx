import React from "react";
import { useNavigate } from "react-router-dom";
import "./LogActivity.css";
import ActivityForm from "./ActivityForm";
import { signOut } from "firebase/auth";
import { auth } from "../../firebase";

export default function LogActivity({ currentUser, onActivityLogged }) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    if (window.confirm("Are you sure you want to log out?")) {
      await signOut(auth);
      localStorage.clear();
      sessionStorage.clear();
      alert("Logged out successfully.");
      navigate("/login", { replace: true });
      window.location.reload();
    }
  };

  return (
    <div className="log-activity">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2>GreenPath</h2>
        <nav className="nav">
          <ul className="nav-links">
            <li><button onClick={() => navigate("/dashboard")}>Dashboard</button></li>
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

      {/* Main content */}
      <main className="main">
        <section className="form-panel">
          <h3>Log a New Activity</h3>
          {/* Pass currentUser down to ActivityForm */}
          <ActivityForm currentUser={currentUser} onActivityLogged={onActivityLogged} />
        </section>
      </main>
    </div>
  );
}
