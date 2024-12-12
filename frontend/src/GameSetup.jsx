import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const GameSetup = () => {
  const [gameTime, setGameTime] = useState(10); // Default game time in minutes
  const [increment, setIncrement] = useState(5); // Default increment in seconds
  const [error, setError] = useState(""); // Для отображения ошибок
  const navigate = useNavigate();

  const API_BASE = "http://127.0.0.1:8000";

  const setupGame = async () => {
    setError(""); // Сброс предыдущей ошибки
    try {
      const response = await axios.post(`${API_BASE}/setup`, {
        game_time: 10,
        increment: 5,
      });
      console.log("Ответ от сервера:", response.data);
      
      if (response.status === 200) {
        console.log("Игра настроена:", response.data);

        await axios.post(`${API_BASE}/games`, {
          uuid: response.data.uuid, // Предполагается, что uuid возвращается от сервера
          white: response.data.white_player_id, // ID белого игрока
          black: response.data.black_player_id, // ID черного игрока
          result: null, // Изначально результат неизвестен
          moves: [], // Изначально список ходов пуст
      });

        navigate("/game"); // Перенаправление на `/game`
      } else {
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
      <button onClick={setupGame}>Начать игру</button>
    </div>
  );
};

export default GameSetup;
