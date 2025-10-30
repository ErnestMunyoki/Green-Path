import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function ActivityForm({ currentUser, onActivityLogged }) {
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

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem("activities");
    if (saved) {
      const parsed = JSON.parse(saved);
      setActivities(parsed);
      setTotalEmission(parsed.reduce((sum, a) => sum + (a.emission || 0), 0));
    }
  }, []);

  // Save to localStorage whenever activities change
  useEffect(() => {
    localStorage.setItem("activities", JSON.stringify(activities));
    setTotalEmission(activities.reduce((sum, a) => sum + (a.emission || 0), 0));
  }, [activities]);

  const estimateEmission = async (activityName) => {
    setLoadingEmission(true);
    try {
      const res = await fetch("https://green-path.onrender.com/api/ai/estimate-emission", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: activityName }),
      });
      if (!res.ok) throw new Error("AI service error");
      const data = await res.json();
      return {
        emission: data.emission ?? 0,
        problem: data.problem || "No problem generated.",
        solution: data.solution || "No solution provided.",
        distance_km: data.distance_km ?? 0,
        vehicle_type: data.vehicle_type || "other",
      };
    } catch (err) {
      console.error("AI fetch error:", err);
      return {
        emission: 0,
        problem: "AI service unavailable.",
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
    if (!category) {
      alert("Please select a category first.");
      return;
    }

    const name = description || category || "Unnamed Activity";
    const activityDate = date || new Date().toISOString().split("T")[0];
    const aiData = await estimateEmission(name);

    const newActivity = {
      ...currentActivity,
      name,
      date: activityDate,
      ...aiData,
    };

    const updatedActivities =
      editingIndex !== null
        ? activities.map((a, i) => (i === editingIndex ? newActivity : a))
        : [...activities, newActivity];

    setActivities(updatedActivities);
    setEditingIndex(null);
    setCurrentActivity({ category: "", description: "", date: "" });
  };

  const handleEdit = (index) => {
    setCurrentActivity(activities[index]);
    setEditingIndex(index);
  };

  const handleRemove = (index) => {
    const updated = activities.filter((_, i) => i !== index);
    setActivities(updated);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Log Activity Button Clicked");
    console.log("Current user:", currentUser);

   if (!currentUser?.uid) {
  alert("User not logged in!");
  return;
}


    if (activities.length === 0) {
      alert("Add at least one activity before logging.");
      return;
    }

    try {
      await Promise.all(
        activities.map((activity) => {
          const payload = {
  name: activity.name,
  category: activity.category,
  description: activity.description,
  date: activity.date || new Date().toISOString().split("T")[0],
  user_id: currentUser.uid,
  emission: activity.emission || 0,
  problem: activity.problem || "No problem provided.",
  solution: activity.solution || "No solution provided."
};


          console.log("Sending activity:", payload);

          return fetch("https://green-path.onrender.com/api/activities/log-activity", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          })
            .then(async (res) => {
              const data = await res.json();
              console.log("Response from backend:", data);
              if (!res.ok) throw new Error(data.error || "Failed to log activity");
              return data;
            })
            .catch((err) => console.error("Error logging activity:", err));
        })
      );

      if (onActivityLogged) onActivityLogged();

      alert(`Activities logged!\nTotal emissions: ${totalEmission.toFixed(2)} kg CO₂`);
      setActivities([]);
      setTotalEmission(0);
      localStorage.removeItem("activities");
      navigate("/dashboard");
    } catch (err) {
      console.error("Submit error:", err);
      alert("Failed to log activities. Check console for details.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="activity-form">
      <h2>Log Your Activity</h2>

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

      <label>Description:</label>
      <input
        type="text"
        value={currentActivity.description}
        onChange={(e) =>
          setCurrentActivity({ ...currentActivity, description: e.target.value })
        }
        placeholder="e.g. Drove 10km, Cooked dinner..."
      />

      <label>Date:</label>
      <input
        type="date"
        value={currentActivity.date}
        onChange={(e) =>
          setCurrentActivity({ ...currentActivity, date: e.target.value })
        }
      />

      <button
        type="button"
        onClick={handleAddOrUpdateActivity}
        disabled={loadingEmission}
      >
        {loadingEmission
          ? "Calculating..."
          : editingIndex !== null
          ? "Update Activity"
          : "Add Activity"}
      </button>

      <h3>Activities</h3>
      <ul>
        {activities.map((activity, i) => (
          <li key={i}>
            <strong>{activity.name}</strong> ({activity.category}) —{" "}
            {activity.date} — {activity.emission.toFixed(2)} kg CO₂
            <button type="button" onClick={() => handleEdit(i)}>Edit</button>
            <button type="button" onClick={() => handleRemove(i)}>Remove</button>
            <div>
              <p><strong>Problem:</strong> {activity.problem}</p>
              <p><strong>Solution:</strong> {activity.solution}</p>
            </div>
          </li>
        ))}
      </ul>

      <div>
        <strong>Total Emissions:</strong> {totalEmission.toFixed(2)} kg CO₂
      </div>

      <button type="submit">Log All Activities</button>
    </form>
  );
}
