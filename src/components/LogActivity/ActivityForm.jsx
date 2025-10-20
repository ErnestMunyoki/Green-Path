import React, { useState } from "react";

export default function ActivityForm() {
  const [name, setName] = useState("");
  const [date, setDate] = useState("");
  const [emission, setEmission] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    const payload = { name, date, emission: parseFloat(emission) };

    fetch("http://127.0.0.1:5000/api/activities", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then((data) => {
        alert("✅ Activity logged!");
        setName("");
        setDate("");
        setEmission("");
      })
      .catch((err) => {
        console.error("Error logging activity:", err);
        alert("❌ Failed to log activity.");
      });
  };

  return (
    <form className="activity-form" onSubmit={handleSubmit}>
      <label>
        Activity Name:
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </label>

      <label>
        Date:
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
        />
      </label>

      <label>
        Emission (kg CO₂):
        <input
          type="number"
          step="0.01"
          value={emission}
          onChange={(e) => setEmission(e.target.value)}
          required
        />
      </label>

      <button type="submit">Log Activity</button>
    </form>
  );
}
