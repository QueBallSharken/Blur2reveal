import React, { useState } from "react";
import Gallery from "./Gallery";

const API_URL = "http://localhost:8000";

function App() {
  const [user, setUser] = useState(null);
  const [mode, setMode] = useState("login");

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isCreator, setIsCreator] = useState(false);
  const [message, setMessage] = useState("");

  const handleAuth = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      if (mode === "register") {
        const res = await fetch(`${API_URL}/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email,
            password,
            is_creator: isCreator,
          }),
        });
        const data = await res.json();
        if (!res.ok) {
          setMessage(data.detail || "Error registering");
        } else {
          setUser(data);
          setMessage("Registered and logged in.");
        }
      } else {
        const params = new URLSearchParams({ email, password });
        const res = await fetch(`${API_URL}/auth/login?${params.toString()}`, {
          method: "POST",
        });
        const data = await res.json();
        if (!res.ok) {
          setMessage(data.detail || "Error logging in");
        } else {
          setUser(data);
          setMessage("Logged in.");
        }
      }
    } catch (err) {
      console.error(err);
      setMessage("Network error");
    }
  };

  if (!user) {
    return (
      <div style={{ maxWidth: "400px", margin: "2rem auto", fontFamily: "sans-serif" }}>
        <h2>Pay-Per-Reveal Demo</h2>

        <button onClick={() => setMode("login")} disabled={mode === "login"}>
          Login
        </button>
        <button onClick={() => setMode("register")} disabled={mode === "register"}>
          Register
        </button>

        <form onSubmit={handleAuth}>
          <label>Email:
            <input type="email" value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{ width: "100%" }} />
          </label>

          <label>Password:
            <input type="password" value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ width: "100%" }} />
          </label>

          {mode === "register" && (
            <label>
              <input type="checkbox"
                checked={isCreator}
                onChange={(e) => setIsCreator(e.target.checked)} />
              I am a creator
            </label>
          )}

          <button type="submit">{mode === "login" ? "Login" : "Register"}</button>
        </form>

        {message && <p>{message}</p>}
      </div>
    );
  }

  return (
    <div style={{ fontFamily: "sans-serif" }}>
      <header style={{ display: "flex", justifyContent: "space-between", padding: "1rem" }}>
        <div>
          <strong>Pay-Per-Reveal Demo</strong>
          <div style={{ fontSize: "0.9rem" }}>{user.email}</div>
        </div>
        <button onClick={() => setUser(null)}>Log out</button>
      </header>

      <Gallery user={user} />
    </div>
  );
}

export default App;
