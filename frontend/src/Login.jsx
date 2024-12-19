import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "./AuthProvider";

const Login = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login: authenticate } = useAuth();
  const navigate = useNavigate();

  const API_BASE = "http://127.0.0.1:8000";
  // const API_BASE = "http://5.35.5.18/api";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    console.log("Попытка входа с данными:");
    console.log("Логин:", login);
    console.log("Пароль:", password);

    try {
      const response = await axios.post(`${API_BASE}/users/login`, {
        login,
        password,
      });

      console.log("Ответ от сервера:", response);

      if (response.data.access_token) {
        const token = response.data.access_token;
        console.log("Токен получен:", token);

        // Сохраняем токен через AuthProvider для синхронизации состояния
        authenticate(token);

        // Перенаправляем пользователя на защищенную страницу
        console.log("Перенаправление на /dashboard");
        navigate("/dashboard");
      } else {
        console.error("Токен отсутствует в ответе сервера");
        setError("Авторизация не удалась. Токен отсутствует.");
      }
    } catch (err) {
      console.error("Ошибка при логине:", err.response?.data || err.message);
      setError(err.response?.data?.detail || "Ошибка авторизации. Проверьте введенные данные.");
    }
  };

  return (
    <div>
      <h2>Авторизация</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Логин"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit">Войти</button>
      </form>
      <p>
        Не зарегистрированы? <a href="/register">Зарегистрируйтесь</a>
      </p>
    </div>
  );
};

export default Login;
