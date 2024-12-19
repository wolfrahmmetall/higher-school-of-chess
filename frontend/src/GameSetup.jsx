import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const GameSetup = () => {
  const [gameTime, setGameTime] = useState(10); // Default game time in minutes
  const [increment, setIncrement] = useState(5); // Default increment in seconds
  const [error, setError] = useState(""); // Для отображения ошибок
  const [playerSide, setPlayerSide] = useState("white"); // Выбранная сторона: "white" или "black"
  const navigate = useNavigate();

  // const API_BASE = "http://5.35.5.18/api/chess";
  const API_BASE = "http://127.0.0.1:8000/chess";

  const setupGame = async () => {
    setError(""); // Сброс предыдущей ошибки
    console.log("Настройка игры начата:");
    console.log("Параметры игры:", { gameTime, increment, playerSide });

    try {
      const token = localStorage.getItem("authToken"); // Токен аутентификации из localStorage
      console.log("Токен из localStorage:", token);
      if (!token) {
        throw new Error("Вы не авторизованы.");
      }

      const headers = { Authorization: `Bearer ${token}` }; // Передаем токен в заголовке

      const response = await axios.post(
        `${API_BASE}/setup`,
        {
          game_time: gameTime,
          increment: increment,
          white: playerSide === "white", // Отправляем, за кого хочет играть пользователь
          black: playerSide === "black",
        },
        { headers }
      );

      console.log("Ответ сервера на настройку игры:", response);

      if (response.status === 200) {
        const { uuid } = response.data; // Получаем UUID игры из ответа
        console.log("Игра настроена. UUID:", uuid);
        localStorage.setItem("game_uuid", uuid);
        console.log("UUID игры сохранён в localStorage.");
        navigate(`/chess/${uuid}/`); // Перенаправляем на страницу с UUID
      } else {
        console.error("Ответ сервера не OK. Код:", response.status);
        throw new Error("Не удалось настроить игру");
      }
    } catch (error) {
      console.error("Ошибка при настройке игры:", error);
      setError("Не удалось настроить игру. Проверьте сервер.");
    }
  };

  return (
    <div className="game-setup">
      <h2>Настройка новой игры</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <label>
        Время на партию (минуты):
        <input
          type="number"
          value={gameTime}
          onChange={(e) => setGameTime(parseInt(e.target.value))}
          min="1"
        />
      </label>
      <label>
        Инкремент (секунды):
        <input
          type="number"
          value={increment}
          onChange={(e) => setIncrement(parseInt(e.target.value))}
          min="0"
        />
      </label>
      <label>
        Выберите сторону:
        <select value={playerSide} onChange={(e) => setPlayerSide(e.target.value)}>
          <option value="white">Белые</option>
          <option value="black">Черные</option>
        </select>
      </label>
      <button onClick={setupGame}>Начать игру</button>
    </div>
  );
};

export default GameSetup;
