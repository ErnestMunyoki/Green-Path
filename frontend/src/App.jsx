// src/App.jsx
import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from "react-router-dom";

// Pages / Components
import Dashboard from "./components/Dashboard/Dashboard";
import Community from "./components/Community";
import LogActivity from "./components/LogActivity/LogActivity";
import Login from "./components/Login";
import AiInsights from "./components/AiInsights";
import Predictions from "./components/Predictions";

// Firebase
import { auth } from "./firebase";                // your exported auth
import { onAuthStateChanged } from "firebase/auth"; // import directly from Firebase SDK

// Protected route wrapper
function ProtectedRoute({ user, children }) {
  return user ? children : <Navigate to="/login" replace />;
}

// Home redirect based on auth state
function HomeRedirect({ user, authChecked }) {
  const navigate = useNavigate();

  useEffect(() => {
    if (!authChecked) return;

    if (user) navigate("/dashboard", { replace: true });
    else navigate("/login", { replace: true });
  }, [user, authChecked, navigate]);

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      Loading...
    </div>
  );
}

function App() {
  const [user, setUser] = useState(null);
  const [authChecked, setAuthChecked] = useState(false);

  useEffect(() => {
    // Listen to Firebase auth state changes
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      if (currentUser) {
        setUser({
          uid: currentUser.uid,
          email: currentUser.email,
        });
        localStorage.setItem(
          "user",
          JSON.stringify({
            uid: currentUser.uid,
            email: currentUser.email,
          })
        );
      } else {
        setUser(null);
        localStorage.removeItem("user");
      }

      setAuthChecked(true);
    });

    return () => unsubscribe();
  }, []);

  if (!authChecked) {
    return (
      <div style={{ textAlign: "center", marginTop: "50px" }}>
        Loading...
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        {/* Home route */}
        <Route
          path="/"
          element={<HomeRedirect user={user} authChecked={authChecked} />}
        />

        {/* Public login */}
        <Route path="/login" element={<Login setUser={setUser} />} />

        {/* Protected routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute user={user}>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/community"
          element={
            <ProtectedRoute user={user}>
              <Community />
            </ProtectedRoute>
          }
        />
        <Route
          path="/log-activity"
          element={
            <ProtectedRoute user={user}>
              <LogActivity />
            </ProtectedRoute>
          }
        />
        <Route
          path="/ai-insights"
          element={
            <ProtectedRoute user={user}>
              <AiInsights />
            </ProtectedRoute>
          }
        />
        <Route
          path="/predictions"
          element={
            <ProtectedRoute user={user}>
              <Predictions />
            </ProtectedRoute>
          }
        />

        {/* Fallback route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
