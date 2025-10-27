import React, { useState, useEffect } from "react";
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

  const quickSuggestions = [
    "Car commute (10km)",
    "Bus ride (15km)",
    "Train journey (20km)",
    "Flight to Nairobi",
    "Boiled water with charcoal",
    "Walked to work",
  ];

  const categories = [
    { label: "Commuting", icon: "🚗" },
    { label: "Meals", icon: "🍴" },
    { label: "Energy", icon: "⚡" },
    { label: "Shopping", icon: "🛒" },
    { label: "Travel", icon: "🧳" },
    { label: "Other", icon: "➕" },
  ];

  // ✅ Load saved activities from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("activities");
    if (saved) {
      const parsed = JSON.parse(saved);
      setActivities(parsed);
      const total = parsed.reduce((sum, act) => sum + (act.emission || 0), 0);
      setTotalEmission(total);
    }
  }, []);

  // ✅ Save to localStorage whenever activities change
  useEffect(() => {
    localStorage.setItem("activities", JSON.stringify(activities));
  }, [activities]);

  // ✅ Fetch AI emission estimation
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
        distance_km: data.distance_km || 0,
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

  // ✅ Add or update activity
  const handleAddOrUpdateActivity = async () => {
    const { category, description, date } = currentActivity;
    if (!category || !date) {
      alert("Please select a category and date.");
      return;
    }

    const activityText = description || category;
    const aiData = await estimateEmission(activityText);

    const newActivity = { ...currentActivity, ...aiData };

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
    setTotalEmission(updatedActivities.reduce((sum, act) => sum + (act.emission || 0), 0));
  };

  const handleEdit = (index) => {
    setCurrentActivity(activities[index]);
    setEditingIndex(index);
  };

  const handleRemove = (index) => {
    const updated = activities.filter((_, i) => i !== index);
    setActivities(updated);
    setTotalEmission(updated.reduce((sum, act) => sum + (act.emission || 0), 0));
  };

  // ✅ Submit all activities to backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (activities.length === 0) {
      alert("Please add at least one activity.");
      return;
    }

    try {
      for (const activity of activities) {
        console.log("Logging activity:", activity);

        const res = await fetch("http://127.0.0.1:5000/api/log-activity", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: activity.description || activity.category,
            category: activity.category,
            date: activity.date,
            distance_km: activity.distance_km || 0,
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
      console.error(err);
      alert("Failed to log activities. Please check console for details.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="activity-form">
      <h2>Log Activity</h2>

      {/* CATEGORY SELECTION */}
      <div className="category-buttons">
        {categories.map(({ label, icon }) => (
          <button
            key={label}
            type="button"
            className={currentActivity.category === label ? "selected" : ""}
            onClick={() =>
              setCurrentActivity({ ...currentActivity, category: label })
            }
          >
            <span className="icon">{icon}</span> {label}
          </button>
        ))}
      </div>

      {/* DESCRIPTION */}
      <label>Description (optional):</label>
      <input
        type="text"
        value={currentActivity.description}
        onChange={(e) =>
          setCurrentActivity({ ...currentActivity, description: e.target.value })
        }
        placeholder="e.g. Drove 10km in petrol car or any activity"
      />

      {/* DATE */}
      <label>Date:</label>
      <input
        type="date"
        value={currentActivity.date}
        onChange={(e) =>
          setCurrentActivity({ ...currentActivity, date: e.target.value })
        }
      />

      {/* ADD OR UPDATE BUTTON */}
      <button
        type="button"
        onClick={handleAddOrUpdateActivity}
        disabled={loadingEmission || !currentActivity.category || !currentActivity.date}
      >
        {loadingEmission
          ? "Calculating..."
          : editingIndex !== null
          ? "Update Activity"
          : "Add Activity"}
      </button>

      {/* QUICK SUGGESTIONS */}
      <div className="quick-suggestions">
        <p>Quick Add Suggestions:</p>
        {quickSuggestions.map((suggestion) => (
          <button
            key={suggestion}
            type="button"
            onClick={() =>
              setCurrentActivity({
                ...currentActivity,
                description: suggestion,
                category: currentActivity.category || "Commuting",
                date:
                  currentActivity.date ||
                  new Date().toISOString().split("T")[0],
              })
            }
          >
            {suggestion}
          </button>
        ))}
      </div>

      {/* ACTIVITY LIST */}
      <div className="activity-list">
        <h3>Today's Activities</h3>
        <ul>
          {activities.map((activity, index) => (
            <li key={index}>
              {activity.category}: {activity.description} on {activity.date} —{" "}
              {activity.emission.toFixed(2)} kg CO₂
              <button type="button" onClick={() => handleEdit(index)}>
                Edit
              </button>
              <button type="button" onClick={() => handleRemove(index)}>
                Remove
              </button>
              <div className="ai-insight">
                <p>
                  <strong>Problem:</strong> {activity.problem}
                </p>
                <p>
                  <strong>Recommendation:</strong> {activity.recommendation}
                </p>
                <p>
                  <strong>Solution:</strong> {activity.solution}
                </p>
              </div>
            </li>
          ))}
        </ul>
      </div>

      {/* TOTAL EMISSIONS */}
      <div className="total-emission">
        <strong>Total Emissions:</strong> {totalEmission.toFixed(2)} kg CO₂
      </div>

      <button type="submit">Log All Activities</button>
    </form>
  );
}
