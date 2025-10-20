import React from "react"; 
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./components/Dashboard/Dashboard";
import LogActivity from "./components/LogActivity/LogActivity";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/log-activity" element={<LogActivity />} />
      </Routes>
    </Router>
  );
}

export default App;




