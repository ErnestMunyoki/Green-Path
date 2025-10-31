
import { initializeApp } from "firebase/app";
import {
  getAuth,
  GoogleAuthProvider,
  GithubAuthProvider,
} from "firebase/auth";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyB4eRHT0PKJQuvVT7xTP2a8iZG6z-tiazk",
  authDomain: "greenpath-5093d.firebaseapp.com",
  projectId: "greenpath-5093d",
  storageBucket: "greenpath-5093d.firebasestorage.app",
  messagingSenderId: "970505821819",
  appId: "1:970505821819:web:ea5c286c2796000d674cde",
  measurementId: "G-L04NTDZMMQ",
};

const app = initializeApp(firebaseConfig);

let analytics;
if (typeof window !== "undefined") {
  analytics = getAnalytics(app);
}

const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();
const githubProvider = new GithubAuthProvider();

export { auth, googleProvider, githubProvider };
