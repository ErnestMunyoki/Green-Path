import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function PostForm() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [author, setAuthor] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const newPost = { title, content, author };

    fetch("http://localhost:5000/community", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newPost),
    })
      .then(() => {
        alert("Post added successfully!");
        navigate("/community");
      })
      .catch((err) => console.error("Error adding post:", err));
  };

  return (
    <form className="post-form" onSubmit={handleSubmit}>
      <h3>Share a Community Post</h3>
      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <textarea
        placeholder="Content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Your Name"
        value={author}
        onChange={(e) => setAuthor(e.target.value)}
      />
      <button type="submit">Post</button>
    </form>
  );
}

export default PostForm;
