import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ActivityForm() {
  const navigate = useNavigate();

  const [category, setCategory] = useState("");
  const [emission, setEmission] = useState("");
  const [date, setDate] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!category || !emission || !date) {
      alert("Please fill in all fields.");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:5000/api/activities", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          category,
          emission: parseFloat(emission),
          date
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to log activity");
      }

      const data = await res.json();
      alert(data.message || "Activity logged successfully!");
      navigate("/");

    } catch (err) {
      console.error("Error logging activity:", err);
      alert("Failed to log activity. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Log New Activity</h2>

      <label>Category:</label>
      <input
        type="text"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        placeholder="e.g. Transport"
      />

      <label>Date:</label>
      <input
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
      />

      <label>Emission (kg CO₂):</label>
      <input
        type="number"
        value={emission}
        onChange={(e) => setEmission(e.target.value)}
        placeholder="e.g. 0.5"
        step="0.01"
        min="0"
      />

      <button type="submit" className="submit">Log Activity</button>
    </form>
  );
}

