import React, { useState, useEffect } from "react";
import axios from "axios";
import "../App.css";
import { signOut } from "firebase/auth";
import { auth } from "../firebase";
import { useNavigate } from "react-router-dom";

const Community = () => {
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState("");
  const [category, setCategory] = useState("Tip");
  const [commentText, setCommentText] = useState("");
  const [openComments, setOpenComments] = useState({});

  const navigate = useNavigate();
  const API_BASE = "http://127.0.0.1:5000/api";

  const fetchPosts = async () => {
    try {
      const res = await axios.get(`${API_BASE}/posts`);
      const data = res.data.map((p) => ({ ...p, liked: false }));
      setPosts(data);
    } catch (err) {
      console.error("Error loading posts:", err);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  const handlePost = async () => {
    if (!newPost.trim()) return;
    await axios.post(`${API_BASE}/posts`, {
      author: "EcoUser",
      category,
      content: newPost,
    });
    setNewPost("");
    fetchPosts();
  };

  const handleLike = async (id) => {
    try {
      await axios.post(`${API_BASE}/posts/${id}/like`);
      setPosts((prevPosts) =>
        prevPosts.map((p) =>
          p.id === id
            ? {
                ...p,
                liked: !p.liked,
                likes: p.liked ? p.likes - 1 : p.likes + 1,
              }
            : p
        )
      );
    } catch (err) {
      console.error("Error liking post:", err);
    }
  };

  const handleComment = async (id) => {
    if (!commentText.trim()) return;
    try {
      await axios.post(`${API_BASE}/posts/${id}/comments`, {
        author: "EcoUser",
        content: commentText,
      });
      setCommentText("");
      fetchPosts();
    } catch (err) {
      console.error("Error posting comment:", err);
    }
  };

  // 🗑 Delete Post
  const handleDeletePost = async (id) => {
    await axios.delete(`${API_BASE}/posts/${id}`);
    fetchPosts();
  };

  const handleDeleteComment = async (postId, commentId) => {
    await axios.delete(`${API_BASE}/posts/${postId}/comments/${commentId}`);
    fetchPosts();
  };

  const toggleComments = (id) => {
    setOpenComments((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const handleLogout = async () => {
    const confirmLogout = window.confirm("Are you sure you want to log out?");
    if (!confirmLogout) return;

    try {
      await signOut(auth);
      alert("You’ve been logged out successfully.");
      navigate("/"); 
    } catch (error) {
      console.error("Logout error:", error);
      alert("Failed to log out. Please try again.");
    }
  };

  return (
    <div className="community-page">
      <aside className="sidebar">
        <h2 className="logo">GreenPath</h2>
        <nav>
          <ul>
            <li>Dashboard</li>
            <li>Community</li>
          </ul>
        </nav>
        <button className="logout-btn" onClick={handleLogout}>
           Logout
        </button>
      </aside>

      {/* ===== MAIN CONTENT ===== */}
      <div className="community-container">
        <div className="community-header">
          <h1>Community</h1>
          <p>Share tips, celebrate milestones, and learn from fellow eco-warriors 🌱</p>
        </div>

        <div className="join-banner">
          <div className="banner-overlay">
            <div className="join-content">
              <i className="fa-solid fa-people-group"></i>
              <h3>Join the Movement</h3>
            </div>
          </div>
        </div>

        <div className="stats-section">
          <div className="stat-card">
            <h3>1,234</h3>
            <p>Members</p>
          </div>
          <div className="stat-card">
            <h3 className="green">45.6K</h3>
            <p>CO₂ Saved Together</p>
          </div>
          <div className="stat-card">
            <h3 className="blue">892</h3>
            <p>Tips Shared</p>
          </div>
        </div>

        <div className="post-input">
          <h3>Share with Community</h3>
          <p>Post a milestone, tip, or question</p>
          <textarea
            placeholder="What sustainability insight would you like to share?"
            value={newPost}
            onChange={(e) => setNewPost(e.target.value)}
          />
          <div className="post-tags">
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
          <button onClick={handlePost} className="submit-btn">
            Post
          </button>
        </div>

        <div className="posts-section">
          {posts.map((post) => (
            <div className="post-card" key={post.id}>
              <div className="post-header">
                <h4>{post.author}</h4>
                <span>{post.created_at}</span>
              </div>

              <span className={`category ${post.category.toLowerCase()}`}>
                {post.category}
              </span>

              <p>{post.content}</p>

              <div className="post-actions">
                <button
                  onClick={() => handleLike(post.id)}
                  className={post.liked ? "liked" : ""}
                >
                  <i
                    className={
                      post.liked ? "fa-solid fa-heart" : "fa-regular fa-heart"
                    }
                    style={{ color: post.liked ? "red" : "black" }}
                  ></i>{" "}
                  {post.likes}
                </button>

                <button onClick={() => toggleComments(post.id)}>
                  <i className="fa-regular fa-comment"></i>{" "}
                  {post.comments?.length || 0}
                </button>

                <button>
                  <i className="fa-solid fa-share"></i> Share
                </button>

                {post.author === "EcoUser" && (
                  <button
                    className="delete-btn"
                    onClick={() => handleDeletePost(post.id)}
                  >
                     Delete
                  </button>
                )}
              </div>

              {openComments[post.id] && (
                <div className="comments-section">
                  <h5>Comments:</h5>
                  <div className="comments-list">
                    {post.comments?.map((c) => (
                      <div key={c.id} className="comment-card">
                        <div className="comment-header">
                          <img
                            src="/images/default-avatar.png"
                            alt="user avatar"
                            className="comment-avatar"
                          />
                          <div className="comment-info">
                            <h4 className="comment-name">
                              {c.author || "Anonymous"}
                            </h4>
                            <p className="comment-date">
                              {new Date(c.created_at).toLocaleDateString()}
                            </p>
                          </div>
                        </div>

                        <p className="comment-text">{c.content}</p>

                        <div className="comment-footer">
                          {c.author === "EcoUser" && (
                            <button
                              className="comment-delete"
                              onClick={() =>
                                handleDeleteComment(post.id, c.id)
                              }
                            >
                              <i className="fa-solid fa-trash"></i>
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="comment-box">
                    <input
                      type="text"
                      placeholder="Write a comment..."
                      value={commentText}
                      onChange={(e) => setCommentText(e.target.value)}
                    />
                    <button onClick={() => handleComment(post.id)}>
                      Comment
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="trending-section">
          <h3>Trending Tips This Week</h3>
          <div className="trend-card">
            <h4>Reusable Shopping Bags</h4>
            <p>Using reusable bags can save 500 plastic bags per year</p>
            <span>234 likes • 45 comments</span>
          </div>
          <div className="trend-card">
            <h4>LED Lighting Switch</h4>
            <p>Reduce electricity use by 75% with LED bulbs</p>
            <span>189 likes • 32 comments</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Community;
