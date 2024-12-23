import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Register = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // const API_BASE = "http://127.0.0.1:8000";
  const API_BASE = "http://5.35.5.18/api"

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    console.log("Регистрация началась:");
    console.log("Данные:", { login, password, email });

    try {
      const response = await axios.post(`${API_BASE}/users/register`, {
        login,
        password,
        email,
      });
      console.log("Ответ сервера:", response.data);
      navigate("/login");
      console.log("Перенаправление на /dashboard выполнено.");
    } catch (err) {
      console.error("Ошибка регистрации:", err.response?.data || err.message);
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Login"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit">Register</button>
      </form>
      <p>
        Уже есть аккаунт? <a href="http://5.35.5.18/login">Войдите</a>
      </p>
    </div>
  );
};

export default Register;
