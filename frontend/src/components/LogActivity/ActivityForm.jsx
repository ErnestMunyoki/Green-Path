import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function ActivityForm({ onActivityLogged }) {
  const navigate = useNavigate();
  const [activities, setActivities] = useState([]);
  const [currentActivity, setCurrentActivity] = useState({
    category: "",
    description: "",
    date: "",
  });
  const [editingIndex, setEditingIndex] = useState(null);
  const [totalEmission, setTotalEmission] = useState(0);
  const [loadingEmission, setLoadingEmission] = useState(false);

  const categories = [
    { label: "Commuting", icon: "🚗" },
    { label: "Meals", icon: "🍴" },
    { label: "Energy", icon: "⚡" },
    { label: "Shopping", icon: "🛒" },
    { label: "Travel", icon: "🧳" },
    { label: "Other", icon: "➕" },
  ];

  // Load saved activities from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem("activities");
    if (saved) {
      const parsed = JSON.parse(saved);
      setActivities(parsed);
      setTotalEmission(parsed.reduce((sum, a) => sum + (a.emission || 0), 0));
    }
  }, []);

  // Save activities to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem("activities", JSON.stringify(activities));
  }, [activities]);

  // AI emission estimate
  const estimateEmission = async (activityDesc) => {
    setLoadingEmission(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/api/ai/estimate-emission", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: activityDesc }),
      });
      if (!res.ok) throw new Error("AI service error");
      const data = await res.json();
      return {
        emission: data.emission ?? 0,
        problem: data.problem || "No problem generated.",
        recommendation: data.recommendation || "No recommendation.",
        solution: data.solution || "No solution provided.",
        distance_km: data.distance_km ?? 0,
        vehicle_type: data.vehicle_type || "other",
      };
    } catch (err) {
      console.error("AI fetch error:", err);
      return {
        emission: 0,
        problem: "AI service unavailable.",
        recommendation: "Try again later.",
        solution: "Service temporarily unavailable.",
        distance_km: 0,
        vehicle_type: "other",
      };
    } finally {
      setLoadingEmission(false);
    }
  };

  // Add or update activity
  const handleAddOrUpdateActivity = async () => {
    const { category, description, date } = currentActivity;
    if (!description && !category) {
      alert("Enter a description or select a category.");
      return;
    }

    const name = description || category || "Unnamed Activity";
    const activityDate = date || new Date().toISOString().split("T")[0];
    const aiData = await estimateEmission(name);

    const newActivity = { ...currentActivity, name, date: activityDate, ...aiData };

    const updatedActivities =
      editingIndex !== null
        ? activities.map((a, i) => (i === editingIndex ? newActivity : a))
        : [...activities, newActivity];

    setActivities(updatedActivities);
    setEditingIndex(null);
    setCurrentActivity({ category: "", description: "", date: "" });
    setTotalEmission(updatedActivities.reduce((sum, a) => sum + (a.emission || 0), 0));
  };

  // Edit activity
  const handleEdit = (index) => {
    setCurrentActivity(activities[index]);
    setEditingIndex(index);
  };

  // Remove activity
  const handleRemove = (index) => {
    const updated = activities.filter((_, i) => i !== index);
    setActivities(updated);
    setTotalEmission(updated.reduce((sum, a) => sum + (a.emission || 0), 0));
  };

  // Submit all activities to backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (activities.length === 0) {
      alert("Add at least one activity.");
      return;
    }

    try {
      await Promise.all(
        activities.map((activity) =>
          fetch("http://127.0.0.1:5000/api/activities/log-activity", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              name: activity.name,
              category: activity.category || "Uncategorized",
              date: activity.date,
              emission: activity.emission ?? 0,
              distance_km: activity.distance_km ?? 0,
              vehicle_type: activity.vehicle_type || "other",
              problem: activity.problem || "",
              solution: activity.solution || "",
            }),
          }).then((res) => {
            if (!res.ok) throw new Error("Failed to log activity");
            return res.json();
          })
        )
      );

      if (onActivityLogged) onActivityLogged();

      alert(`Activities logged!\nTotal emissions: ${totalEmission.toFixed(2)} kg CO₂`);

      // Clear activities locally and in localStorage
      setActivities([]);
      setTotalEmission(0);
      localStorage.removeItem("activities");

      navigate("/"); // back to dashboard
    } catch (err) {
      console.error("Submit error:", err);
      alert("Failed to log activities. Check console.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="activity-form">
      <h2>Log Any Activity</h2>

      <label>Description:</label>
      <input
        type="text"
        value={currentActivity.description}
        onChange={(e) => setCurrentActivity({ ...currentActivity, description: e.target.value })}
        placeholder="e.g. Drove 10km, Cooked dinner..."
      />

      <label>Category:</label>
      <div className="category-buttons">
        {categories.map(({ label, icon }) => (
          <button
            key={label}
            type="button"
            className={currentActivity.category === label ? "selected" : ""}
            onClick={() => setCurrentActivity({ ...currentActivity, category: label })}
          >
            <span className="icon">{icon}</span> {label}
          </button>
        ))}
      </div>

      <label>Date:</label>
      <input
        type="date"
        value={currentActivity.date}
        onChange={(e) => setCurrentActivity({ ...currentActivity, date: e.target.value })}
      />

      <button type="button" onClick={handleAddOrUpdateActivity} disabled={loadingEmission}>
        {loadingEmission ? "Calculating..." : editingIndex !== null ? "Update Activity" : "Add Activity"}
      </button>

      <h3>Activities</h3>
      <ul>
        {activities.map((activity, i) => (
          <li key={i}>
            <strong>{activity.name}</strong> ({activity.category || "Uncategorized"}) on {activity.date} —{" "}
            {activity.emission.toFixed(2)} kg CO₂
            <button type="button" onClick={() => handleEdit(i)}>Edit</button>
            <button type="button" onClick={() => handleRemove(i)}>Remove</button>
            <div>
              <p><strong>Problem:</strong> {activity.problem}</p>
              <p><strong>Solution:</strong> {activity.solution}</p>
            </div>
          </li>
        ))}
      </ul>

      <div><strong>Total Emissions:</strong> {totalEmission.toFixed(2)} kg CO₂</div>
      <button type="submit">Log All Activities</button>
    </form>
  );
}
