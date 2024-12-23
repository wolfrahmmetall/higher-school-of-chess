
import React, { useEffect, useState } from "react";
import { useAuth } from "./AuthProvider";
import { useNavigate } from "react-router-dom";
import PlayerRating from "./components/PlayerRating";
import axios from "axios";
import './App.css';

const Dashboard = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("Гость");
  const [activeGames, setActiveGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const API_BASE = "http://127.0.0.1:8000";

  useEffect(() => {
    const fetchUsername = async () => {
      console.log("Загрузка данных пользователя...");
      try {
        const token = localStorage.getItem("authToken");
        console.log("Токен для запроса имени пользователя:", token);
        if (!token) throw new Error("Вы не авторизованы.");

        const headers = { Authorization: `Bearer ${token}` };
        const response = await axios.get(`${API_BASE}/users/me`, { headers });
        console.log("Данные пользователя получены:", response.data);
        setUsername(response.data.login);
      } catch (err) {
        console.error("Ошибка при загрузке данных пользователя:", err);
        setUsername("Гость");
      }
    };

    const fetchActiveGames = async () => {
      console.log("Загрузка активных игр...");
      try {
        setLoading(true);
        const response = await axios.get(`${API_BASE}/chess/active-games`);
        console.log("Активные игры получены:", response.data);
        setActiveGames(response.data);
      } catch (err) {
        console.error("Ошибка при загрузке активных игр:", err);
        setError("Не удалось загрузить список игр.");
      } finally {
        setLoading(false);
      }
    };

    fetchUsername();
    fetchActiveGames();
  }, []);

  const handleLogout = () => {
    console.log("Логаут: Выход пользователя.");
    logout();
    navigate("/login");
    console.log("Перенаправление на /login.");
  };

  const handleNewGame = () => {
    console.log("Создание новой игры.");
    navigate("/game/setup");
    console.log("Перенаправление на /game/setup.");
  };

  const handleConnectToGame = async (uuid) => {
    console.log(`Попытка подключиться к игре с UUID: ${uuid}`);
    try {
      const token = localStorage.getItem("authToken");
      console.log("Токен для подключения:", token);
      if (!token) throw new Error("Вы не авторизованы.");

      const headers = { Authorization: `Bearer ${token}` };
      const response = await axios.post(`${API_BASE}/chess/${uuid}/connect`, {}, { headers });
      console.log("Подключение к игре успешно:", response.data);
      navigate(`/chess/${response.data.uuid}/`);
    } catch (err) {
      console.error("Ошибка подключения к игре:", err);
      alert("Не удалось подключиться к игре. Проверьте доступность сервера.");
    }
  };

  console.log("Отображение дашборда.");


  return (
    <div className="container">
      <h2>Добро пожаловать в Дашборд, {username}</h2>
      <button onClick={handleLogout}>Logout</button>
      <div className="dashboard-container">
        <div className="component-container">
          <button onClick={handleNewGame}>Создать новую игру</button>
        </div>
      </div>
      <div className="dashboard-container">
        {loading ? (
          <p>Загрузка списка игр...</p>
        ) : error ? (
          <p style={{ color: "red" }}>{error}</p>
        ) : (
          <div className="component-container">
            <h3>Список активных игр</h3>
            <ul>
              {activeGames.map((game) => (
                <li key={game.uuid}>
                  <div>
                    <strong>Игра UUID: {game.uuid}</strong><br />
                    Создана: {game.created_by}<br />
                    Время игры: {game.game_time} минут<br />
                    Инкремент: {game.increment} секунд
                  </div>
                  <button onClick={() => handleConnectToGame(game.uuid)}>Подключиться</button>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
