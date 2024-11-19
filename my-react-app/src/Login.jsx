import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "./AuthProvider";

const Login = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login: saveToken } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
  
    const payload = { login, password }; // Проверка формата данных
    console.log("Payload:", payload); // Логирование данных перед отправкой
  
    try {
      const response = await axios.post("http://127.0.0.1:8000/users/login", payload);
      saveToken(response.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      console.error("Error response:", err.response?.data); // Логирование ошибки сервера
      setError(err.response?.data?.detail || "Login failed");
    }
  };
  

  return (
    <div>
      <h2>Login</h2>
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
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
