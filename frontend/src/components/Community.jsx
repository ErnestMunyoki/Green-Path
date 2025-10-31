import React, { useState, useEffect } from "react";
import axios from "axios";
import "../App.css";

const Community = () => {
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState("");
  const [category, setCategory] = useState("Tip"); 
  const [commentText, setCommentText] = useState({}); 
  const [openComments, setOpenComments] = useState({});
  const [likedPosts, setLikedPosts] = useState([]);

  const API_BASE = "https://green-path.onrender.com/api";

  const fetchPosts = async () => {
    try {
      const res = await axios.get(`${API_BASE}/posts`);
      setPosts(res.data);
    } catch (err) {
      console.error("Error loading posts:", err);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  const handlePost = async () => {
    if (!newPost.trim()) return;
    try {
      await axios.post(`${API_BASE}/posts`, {
        content: newPost,
        user_id: 1, 
      });
      setNewPost("");
      setCategory("Tip");
      fetchPosts();
    } catch (err) {
      console.error("Error posting:", err);
    }
  };

  const handleLike = async (id) => {
    try {
      const alreadyLiked = likedPosts.includes(id);
      await axios.post(`${API_BASE}/posts/${id}/like`);
      setPosts((prev) =>
        prev.map((p) =>
          p.id === id
            ? { ...p, likes: alreadyLiked ? (p.likes || 1) - 1 : (p.likes || 0) + 1 }
            : p
        )
      );
      setLikedPosts((prev) =>
        alreadyLiked ? prev.filter((pid) => pid !== id) : [...prev, id]
      );
    } catch (err) {
      console.error("Error liking post:", err);
    }
  };

  const handleComment = async (postId) => {
    const text = commentText[postId];
    if (!text?.trim()) return;

    try {
      await axios.post(`${API_BASE}/posts/${postId}/comments`, {
        content: text,
        user_id: 1,
      });
      setCommentText((prev) => ({ ...prev, [postId]: "" }));
      fetchPosts();
    } catch (err) {
      console.error("Error posting comment:", err);
    }
  };

  const handleDeletePost = async (id) => {
    try {
      await axios.delete(`${API_BASE}/posts/${id}`);
      fetchPosts();
    } catch (err) {
      console.error("Error deleting post:", err);
    }
  };

  const handleDeleteComment = async (postId, commentId) => {
    try {
      await axios.delete(`${API_BASE}/posts/${postId}/comments/${commentId}`);
      fetchPosts();
    } catch (err) {
      console.error("Error deleting comment:", err);
    }
  };

  const toggleComments = (id) => {
    setOpenComments((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <div className="community-wrapper">
      <div className="community-header">
        <h1>Community</h1>
        <p>Post a milestone, tip, or question to inspire others </p>
      </div>

      <div className="post-creator">
        <textarea
          placeholder="What sustainability insight would you like to share?"
          value={newPost}
          onChange={(e) => setNewPost(e.target.value)}
        />
        <div className="category-buttons">
          {["Milestone", "Tip", "Question"].map((tag) => (
            <button
              key={tag}
              onClick={() => setCategory(tag)}
              className={category === tag ? "active" : ""}
            >
              {tag}
            </button>
          ))}
        </div>
        <button className="post-btn" onClick={handlePost}>
          Post
        </button>
      </div>

      <div className="posts-list">
        {posts.length === 0 ? (
          <p className="no-posts">No posts yet. Be the first to share </p>
        ) : (
          posts.map((post) => (
            <div key={post.id} className="post-card">
              <div className="post-header">
                <div className="user-info">
                  <img
                    src="/images/default-avatar.png"
                    alt="avatar"
                    className="avatar"
                  />
                  <div>
                    <h4>{post.user?.username || "EcoUser"}</h4>
                    <p>{new Date(post.date_created).toLocaleDateString()}</p>
                  </div>
                </div>
                <span className={`tag ${category.toLowerCase()}`}>{category}</span>
              </div>

              <p className="post-content">{post.content}</p>

              <div className="post-actions">
                <button
                  className={`like-btn ${likedPosts.includes(post.id) ? "liked" : ""}`}
                  onClick={() => handleLike(post.id)}
                >
                  <i
                    className={
                      likedPosts.includes(post.id)
                        ? "fa-solid fa-heart"
                        : "fa-regular fa-heart"
                    }
                  ></i>{" "}
                  {post.likes || 0}
                </button>

                <button onClick={() => toggleComments(post.id)}>
                  <i className="fa-regular fa-comment"></i>{" "}
                  {post.comments?.length || 0}
                </button>

                <button className="share-btn">
                  <i className="fa-solid fa-share"></i> Share
                </button>

                <button
                  className="delete-post"
                  onClick={() => handleDeletePost(post.id)}
                >
                  Delete
                </button>
              </div>

              {openComments[post.id] && (
                <div className="comments-section">
                  {post.comments?.map((c) => (
                    <div key={c.id} className="comment-card">
                      <div className="comment-info">
                        <strong>{c.user?.username || "EcoUser"}</strong>
                        <p>{c.content}</p>
                      </div>
                      <button
                        className="delete-comment"
                        onClick={() =>
                          handleDeleteComment(post.id, c.id)
                        }
                      >
                        Delete
                      </button>
                    </div>
                  ))}

                  <div className="comment-input">
                    <input
                      type="text"
                      placeholder="Write a comment..."
                      value={commentText[post.id] || ""}
                      onChange={(e) =>
                        setCommentText((prev) => ({
                          ...prev,
                          [post.id]: e.target.value,
                        }))
                      }
                    />
                    <button onClick={() => handleComment(post.id)}>
                      Comment
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Community;
