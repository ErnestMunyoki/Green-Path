import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler 
} from "chart.js";
import "./predictions.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const Predictions = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPredictions = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch("https://green-path.onrender.com/api/predictions");
        if (!response.ok) {
          const text = await response.text();
          throw new Error(`Failed to fetch predictions: ${response.statusText} — ${text}`);
        }
        const data = await response.json();
        setPredictions(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchPredictions();
  }, []);

  const totalEmission = predictions.reduce((sum, p) => sum + (p.emission || 0), 0);
  const avgEmission = predictions.length > 0 ? totalEmission / predictions.length : 0;
  const nextWeek = avgEmission * 7;
  const nextMonth = avgEmission * 30;

  const labels = predictions.length > 0
    ? predictions.map(p => p.date)
    : ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  const emissions = predictions.length > 0
    ? predictions.map(p => p.emission || 0)
    : [12, 12.5, 13, 14.5, 13.8, 14, 13.9];

  const chartData = {
    labels,
    datasets: [
      {
        label: "Predicted CO₂ Emissions (kg)",
        data: emissions,
        fill: true,
        backgroundColor: "rgba(33, 150, 243, 0.15)",
        borderColor: "rgba(33, 150, 243, 0.9)",
        tension: 0.4,
        pointRadius: 0
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: { display: false }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { color: "#555" },
        grid: { color: "#eee" }
      },
      x: {
        ticks: { color: "#555" },
        grid: { display: false }
      }
    }
  };

  return (
    <div className="analytics-container">
      <h2>Predictive Analytics</h2>
      <p className="subtitle">Machine learning–powered forecasts of your carbon footprint</p>

      <div className="summary-cards">
        <div className="card">
          <h3>Predicted Next Week</h3>
          <p className="value">{nextWeek.toFixed(1)} kg CO₂</p>
          <p className="status improving">Improving trend</p>
        </div>

        <div className="card">
          <h3>Predicted Next Month</h3>
          <p className="value">{nextMonth.toFixed(1)} kg CO₂</p>
          <p className="status above">Above target</p>
        </div>

        <div className="card">
          <h3>Predicted Daily Avg</h3>
          <p className="value">{avgEmission.toFixed(1)} kg CO₂</p>
          <p className="status neutral">Based on recent data</p>
        </div>
      </div>

      <div className="chart-section">
        <h4>7-Day Forecast</h4>
        <Line options={options} data={chartData} />
      </div>

      <div className="prediction-insight">
        <strong>Prediction Insight:</strong> Based on your current trends, you are projected to emit about
        <span> {nextWeek.toFixed(1)} kg CO₂</span> next week. Try adopting cleaner transport or reducing energy use.
      </div>

      {loading && <p>Loading predictions...</p>}
      {error && <p className="error">Error: {error} ⚠️</p>}
    </div>
  );
};

export default Predictions;
