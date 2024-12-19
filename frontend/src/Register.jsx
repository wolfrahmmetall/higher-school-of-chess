import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Register = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    console.log("Регистрация началась:");
    console.log("Данные:", { login, password, email });

    try {
      const response = await axios.post("http://5.35.5.18/api/users/register", {
        login,
        password,
        email,
      });

      console.log("Ответ сервера:", response.data);

      if (response.data?.access_token) {
        localStorage.setItem("token", response.data.access_token);
        console.log("Токен сохранен в localStorage:", response.data.access_token);
        navigate("/dashboard");
        console.log("Перенаправление на /dashboard выполнено.");
      } else {
        console.error("Токен отсутствует в ответе сервера:", response.data);
        setError("Ошибка регистрации. Токен отсутствует.");
      }
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
