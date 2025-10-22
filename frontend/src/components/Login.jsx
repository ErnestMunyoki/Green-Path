import React, { useState, useEffect } from "react";
import { auth, googleProvider, githubProvider } from "../firebase";
import {
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  onAuthStateChanged,
} from "firebase/auth";
import { FcGoogle } from "react-icons/fc";
import { FaGithub } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import "../App.css";

function Login() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        localStorage.setItem(
          "user",
          JSON.stringify({
            name: user.displayName || "User",
            email: user.email,
            photo: user.photoURL,
          })
        );
        navigate("/dashboard");
      }
    });

    return () => unsubscribe();
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (!email || !password) {
        alert("Please fill in all fields.");
        return;
      }

      let userCredential;
      if (isLogin) {
        userCredential = await signInWithEmailAndPassword(auth, email, password);
        console.log("Login successful");
      } else {
        userCredential = await createUserWithEmailAndPassword(auth, email, password);
        console.log("Registration successful");
      }

      const user = userCredential.user;
      localStorage.setItem(
        "user",
        JSON.stringify({
          name: user.displayName || "User",
          email: user.email,
          photo: user.photoURL,
        })
      );

      navigate("/dashboard");
    } catch (error) {
      console.error("Authentication error:", error);
      switch (error.code) {
        case "auth/email-already-in-use":
          alert("This email is already registered. Try logging in instead.");
          break;
        case "auth/invalid-email":
          alert("Invalid email format.");
          break;
        case "auth/wrong-password":
          alert("Incorrect password. Try again.");
          break;
        case "auth/user-not-found":
          alert("No account found. Please register first.");
          break;
        case "auth/weak-password":
          alert("Password must be at least 6 characters long.");
          break;
        default:
          alert("Authentication failed. Please try again.");
      }
    }
  };

  const handleGoogleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      const user = result.user;

      localStorage.setItem(
        "user",
        JSON.stringify({
          name: user.displayName,
          email: user.email,
          photo: user.photoURL,
        })
      );

      console.log("Google login successful:", user.displayName);
      navigate("/dashboard");
    } catch (error) {
      console.error("Google login error:", error);
      alert("Google login failed. Please try again.");
    }
  };

  const handleGithubLogin = async () => {
    try {
      const result = await signInWithPopup(auth, githubProvider);
      const user = result.user;

      localStorage.setItem(
        "user",
        JSON.stringify({
          name: user.displayName || "GitHub User",
          email: user.email,
          photo: user.photoURL,
        })
      );

      console.log("GitHub login successful:", user.displayName);
      navigate("/dashboard");
    } catch (error) {
      console.error("GitHub login error:", error);
      alert("GitHub login failed. Please try again.");
    }
  };

  return (
    <div className="app-container">
      <div className="login-card">
        <h2>Welcome</h2>
        <p>Track your carbon footprint and make a positive impact 🌿</p>

        {/* Tabs for Login/Register */}
        <div className="tab-buttons">
          <button
            className={isLogin ? "active" : ""}
            onClick={() => setIsLogin(true)}
          >
            Login
          </button>
          <button
            className={!isLogin ? "active" : ""}
            onClick={() => setIsLogin(false)}
          >
            Register
          </button>
        </div>

        {/* Email Form */}
        <form onSubmit={handleSubmit}>
          <label>Email</label>
          <input
            type="email"
            placeholder="your@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Password</label>
          <input
            type="password"
            placeholder="•••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" className="signin-btn">
            {isLogin ? "Sign In" : "Register"}
          </button>
        </form>

        {/* Social Login */}
        <div className="divider">
          <span>OR CONTINUE WITH</span>
        </div>

        <div className="social-buttons">
          <button className="google-btn" onClick={handleGoogleLogin}>
            <FcGoogle size={20} />
            Google
          </button>

          <button className="github-btn" onClick={handleGithubLogin}>
            <FaGithub size={20} />
            GitHub
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;
