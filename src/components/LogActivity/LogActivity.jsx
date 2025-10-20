import React from "react";
import "./LogActivity.css";
import ActivityForm from "./ActivityForm";

export default function LogActivity() {
  return (
    <div className="log-activity">
      <h2>Log New Activity</h2>
      <ActivityForm />
    </div>
  );
}
