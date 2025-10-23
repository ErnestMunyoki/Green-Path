import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ActivityForm() {
  const navigate = useNavigate();

  const [activities, setActivities] = useState([]);
  const [currentActivity, setCurrentActivity] = useState({
    category: "",
    description: "",
    date: ""
  });
  const [editingIndex, setEditingIndex] = useState(null);
  const [totalEmission, setTotalEmission] = useState(0);

  const quickSuggestions = [
    "Car commute (10km)",
    "Bus ride (15km)",
    "Train journey (20km)",
    "Flight to Nairobi",
    "Boiled water with charcoal",
    "Walked to work"
  ];

  const categories = [
    { label: "Commuting", icon: "🚗" },
    { label: "Meals", icon: "🍴" },
    { label: "Energy", icon: "⚡" },
    { label: "Shopping", icon: "🛒" },
    { label: "Travel", icon: "🧳" },
    { label: "Other", icon: "➕" }
  ];

  const estimateEmission = async (desc) => {
    const res = await fetch("http://127.0.0.1:5000/api/activities/estimate-emission", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description: desc }),
    });

    const data = await res.json();
    return data.emission;
  };

  const handleAddOrUpdateActivity = async () => {
    const { category, description, date } = currentActivity;
    if (!category || !date) {
      alert("Please select a category and date.");
      return;
    }

    const emission = await estimateEmission(description || category);
    const newActivity = { ...currentActivity, emission };

    let updatedActivities;
    if (editingIndex !== null) {
      updatedActivities = [...activities];
      updatedActivities[editingIndex] = newActivity;
      setEditingIndex(null);
    } else {
      updatedActivities = [...activities, newActivity];
    }

    setActivities(updatedActivities);
    setCurrentActivity({ category: "", description: "", date: "" });

    const newTotal = updatedActivities.reduce((sum, act) => sum + act.emission, 0);
    setTotalEmission(newTotal);
  };

  const handleEdit = (index) => {
    setCurrentActivity(activities[index]);
    setEditingIndex(index);
  };

  const handleRemove = (index) => {
    const updated = activities.filter((_, i) => i !== index);
    setActivities(updated);
    const newTotal = updated.reduce((sum, act) => sum + act.emission, 0);
    setTotalEmission(newTotal);
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
    user_id: 1,              
    name: activity.category,  
    duration: 30              
  }),
});



        if (!res.ok) {
          throw new Error("Failed to log activity");
        }
      }

      alert(` Activities logged!\nTotal emissions: ${totalEmission.toFixed(2)} kg CO₂`);
      navigate("/");

    } catch (err) {
      console.error("Error logging activities:", err);
      alert("Failed to log activities. Please try again.");
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

      <button type="button" className="add-activity" onClick={handleAddOrUpdateActivity}>
        {editingIndex !== null ? "Update Activity" : " Add Activity"}
      </button>

      <div className="quick-suggestions">
        <p>Quick Add Suggestions:</p>
        <div className="suggestion-list">
          {quickSuggestions.map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              onClick={() =>
                setCurrentActivity({
                  ...currentActivity,
                  category: "Commuting",
                  description: suggestion
                })
              }
            >
               {suggestion}
            </button>
          ))}
        </div>
      </div>

      <div className="activity-list">
        <h3>Today's Activities</h3>
        <ul>
          {activities.map((activity, index) => (
            <li key={index}>
              {activity.category}: {activity.description || "(no description)"} on {activity.date} — {activity.emission.toFixed(2)} kg CO₂
              <button onClick={() => handleEdit(index)}> Edit</button>
              <button onClick={() => handleRemove(index)}>Remove</button>
            </li>
          ))}
        </ul>
      </div>

      <div className="total-emission">
        <strong>Total Emissions:</strong> {totalEmission.toFixed(2)} kg CO₂
      </div>

      <button type="submit" className="submit">Log All Activities</button>
    </form>
  );
}





