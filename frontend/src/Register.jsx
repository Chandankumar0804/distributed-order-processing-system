import { useState } from "react";
import "./Register.css";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("viewer");
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();

    setMessage("");
    setSuccess(false);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/auth/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username,
            password,
            role,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Registration failed");
        return;
      }

      setSuccess(true);
      setMessage("Registration successful! Please login.");

      setUsername("");
      setPassword("");
      setRole("viewer");
    } catch {
      setMessage("Backend server is not running");
    }
  };

  return (
    <div className="register-page">

      <div className="register-card">

        <div className="register-header">
            <img src="/Logo.png" alt="Order Processing System" className="register-logo"/>
          <h1>Create Account</h1>
          <p>Register for Order Processing System</p>
        </div>

        <form onSubmit={handleRegister}>

          <div className="register-form-group">
            <label>Username</label>

            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
            />
          </div>

          <div className="register-form-group">
            <label>Password</label>

            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </div>

          <div className="register-form-group">
            <label>Role</label>

            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              <option value="viewer">Viewer</option>
              <option value="operator">Operator</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <button
            type="submit"
            className="register-button"
          >
            Register
          </button>

        </form>

        {message && (
          <p
            className={
              success
                ? "register-success"
                : "register-error"
            }
          >
            {message}
          </p>
        )}

        <div className="login-link">
          Already have an account?
          <button
            onClick={() => {
              window.location.href = "/";
            }}
          >
            Login
          </button>
        </div>

      </div>

    </div>
  );
}

export default Register;