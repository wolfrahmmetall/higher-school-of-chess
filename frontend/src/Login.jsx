import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login = () => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/users/login", {
        login,
        password,
      });

      const token = response.data.access_token;

      // Сохраняем токен в локальном хранилище
      localStorage.setItem("token", token);
      console.log(localStorage.getItem("token"))

      // Перенаправляем пользователя на защищенную страницу
      navigate("/dashboard");
    } catch (err) {
      console.error("Ошибка при логине:", err.response?.data);
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