import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ActivityForm() {
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

  const estimateEmission = async (activityDesc) => {
    setLoadingEmission(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/api/ai/estimate-emission", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: activityDesc }),
      });
      if (!res.ok) throw new Error("Failed to fetch AI insight");
      const data = await res.json();
      return {
        emission: data.emission || 0,
        problem: data.problem || "No problem generated.",
        recommendation: data.recommendation || "No recommendation.",
        solution: data.solution || "No solution.",
        distance_km: data.distance_km ?? 0,
        vehicle_type: data.vehicle_type || "other",
      };
    } catch (err) {
      console.error("AI fetch failed:", err);
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

  const handleAddOrUpdateActivity = async () => {
    const { category, description, date } = currentActivity;
    if (!category || !date) {
      alert("Please select a category and date.");
      return;
    }
    const activityText = description || category;
    const aiData = await estimateEmission(activityText);

    const newActivity = {
      ...currentActivity,
      name: activityText,
      ...aiData,
    };

    const updatedActivities = editingIndex !== null
      ? activities.map((act, i) => (i === editingIndex ? newActivity : act))
      : [...activities, newActivity];

    setActivities(updatedActivities);
    setEditingIndex(null);
    setCurrentActivity({ category: "", description: "", date: "" });
    setTotalEmission(updatedActivities.reduce((sum, act) => sum + act.emission, 0));
  };

  const handleEdit = (index) => setCurrentActivity(activities[index]);
  const handleRemove = (index) => {
    const updated = activities.filter((_, i) => i !== index);
    setActivities(updated);
    setTotalEmission(updated.reduce((sum, act) => sum + act.emission, 0));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (activities.length === 0) {
      alert("Please add at least one activity.");
      return;
    }

    try {
      for (const activity of activities) {
        const res = await fetch("http://127.0.0.1:5000/api/log-activity", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: activity.name,
            category: activity.category,
            date: activity.date,
            distance_km: activity.distance_km ?? 0,
            vehicle_type: activity.vehicle_type || "other",
          }),
        });

        if (!res.ok) {
          const errText = await res.text();
          throw new Error(`Failed to log activity: ${errText}`);
        }
      }

      alert(`Activities logged!\nTotal emissions: ${totalEmission.toFixed(2)} kg CO₂`);
      navigate("/");
    } catch (err) {
      console.error("Submit error:", err);
      alert("Failed to log activities. Check console for details.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="activity-form">
      <h2>Log Activity</h2>

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

      <label>Description (optional):</label>
      <input
        type="text"
        value={currentActivity.description}
        onChange={(e) => setCurrentActivity({ ...currentActivity, description: e.target.value })}
        placeholder="e.g. Drove 10km in petrol car"
      />

      <label>Date:</label>
      <input
        type="date"
        value={currentActivity.date}
        onChange={(e) => setCurrentActivity({ ...currentActivity, date: e.target.value })}
      />

      <button
        type="button"
        onClick={handleAddOrUpdateActivity}
        disabled={loadingEmission || !currentActivity.category || !currentActivity.date}
      >
        {loadingEmission ? "Calculating..." : editingIndex !== null ? "Update Activity" : "Add Activity"}
      </button>

      <h3>Today's Activities</h3>
      <ul>
        {activities.map((activity, index) => (
          <li key={index}>
            {activity.category}: {activity.description} on {activity.date} — {activity.emission.toFixed(2)} kg CO₂
            <button type="button" onClick={() => handleEdit(index)}>Edit</button>
            <button type="button" onClick={() => handleRemove(index)}>Remove</button>
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
