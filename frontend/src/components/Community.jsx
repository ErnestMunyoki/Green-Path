import React from "react";
import { Routes, Route } from "react-router-dom";
import PostList from "./PostList";
import PostForm from "./PostForm";

function Community() {
  return (
    <div className="community">
      <h2>Community Posts</h2>
      <Routes>
        <Route path="/" element={<PostList />} />
        <Route path="/new" element={<PostForm />} />
      </Routes>
    </div>
  );
}

export default Community;
