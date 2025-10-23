import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Dashboard from "./components/Dashboard/Dashboard";
import Community from "./components/Community";
import LogActivity from "./components/LogActivity/LogActivity";
import Login from "./components/Login";
import AiInsights from "./components/AiInsights"; // ✅ Import AI Insights

// ✅ Route guard for logged-in users
function ProtectedRoute({ children }) {
  const user = localStorage.getItem("user");
  return user ? children : <Navigate to="/login" replace />;
}

function App() {
  const [user, setUser] = useState(null);
  const [authChecked, setAuthChecked] = useState(false);

  useEffect(() => {
    // Delay to ensure we read user data correctly before rendering routes
    const storedUser = localStorage.getItem("user");
    setUser(storedUser);
    setAuthChecked(true);
  }, []);

  if (!authChecked) {
    // Prevent brief flash of login page before redirect
    return <div style={{ textAlign: "center", marginTop: "50px" }}>Loading...</div>;
  }

  return (
    <Router>
      <Routes>
        {/* ✅ Default route (goes to login if not logged in) */}
        <Route
          path="/"
          element={
            user ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />
          }
        />

        {/* ✅ Public route */}
        <Route path="/login" element={<Login />} />

        {/* ✅ Protected routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/community"
          element={
            <ProtectedRoute>
              <Community />
            </ProtectedRoute>
          }
        />

        <Route
          path="/log-activity"
          element={
            <ProtectedRoute>
              <LogActivity />
            </ProtectedRoute>
          }
        />

        {/* ✅ AI Insights Route */}
        <Route
          path="/ai-insights"
          element={
            <ProtectedRoute>
              <AiInsights />
            </ProtectedRoute>
          }
        />

        {/* ✅ Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
