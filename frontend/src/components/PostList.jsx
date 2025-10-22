import React, { useEffect, useState } from "react";

function PostList() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/community") // your community route
      .then((res) => res.json())
      .then((data) => setPosts(data))
      .catch((err) => console.error("Error fetching posts:", err));
  }, []);

  return (
    <div className="post-list">
      {posts.length > 0 ? (
        posts.map((post) => (
          <div key={post.id} className="post">
            <h3>{post.title}</h3>
            <p>{post.content}</p>
            <small>By {post.author}</small>
          </div>
        ))
      ) : (
        <p>No community posts yet.</p>
      )}
    </div>
  );
}

export default PostList;
