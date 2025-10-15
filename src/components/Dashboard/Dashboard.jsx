import React from "react";
import "./Dashboard.css";
import {
  weeklyEmissions,
  categoryEmissions,
  achievements
} from "../../utils/mockData";

export default function Dashboard() {
  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>GreenPath</h2>
        <ul>
          <li>Dashboard</li>
          <li>Log Activity</li>
          <li>AI Insights</li>
          <li>Predictions</li>
          <li>Community</li>
          <li>Logout</li>
        </ul>
      </aside>

      <main className="main">
        <section className="summary">
          <div className="card">
            <h4>This Week</h4>
            <div className="value">
              {weeklyEmissions.reduce((acc, d) => acc + d.emission, 0).toFixed(2)} kg CO₂
            </div>
            <div className="note">{weeklyEmissions.length} days tracked</div>
          </div>
          <div className="card">
            <h4>This Month</h4>
            <div className="value">313.90 kg CO₂</div>
            <div className="note">Target: 1000 kg</div>
          </div>
          <div className="card">
            <h4>Daily Average</h4>
            <div className="value">13.19 kg CO₂</div>
            <div className="note">24 activities logged</div>
          </div>
          <div className="card">
            <h4>Achievements</h4>
            <div className="value">{achievements.filter(a => a.unlocked).length} / {achievements.length}</div>
            <div className="note">Keep going!</div>
          </div>
        </section>

        <section className="charts">
          <div className="chart">
            <h4>Weekly Emissions</h4>
            <div className="bars">
              {weeklyEmissions.map((day) => {
                const rawHeight = day.emission * 2;
                const height = `${Math.max(Math.min(rawHeight, 100), 4)}%`;
                return (
                  <div className="bar" key={day.day}>
                    <div className="bar-fill" style={{ height }}></div>
                    <small>{day.day}</small>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="chart">
            <h4>Emissions by Category</h4>
            <ul className="pie-list">
              {categoryEmissions.map((cat) => (
                <li key={cat.category}>
                  {cat.category}: {cat.value} kg
                </li>
              ))}
            </ul>
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


