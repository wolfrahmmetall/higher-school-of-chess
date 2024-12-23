import React, { useEffect, useState } from "react";
import axios from "axios";

const GameList = ({ onConnect }) => {
  const [games, setGames] = useState([]);
  const [filter, setFilter] = useState("all");

  // const API_BASE = "http://127.0.0.1:8000/chess";
  const API_BASE = "http://5.35.5.18/api/chess";

  useEffect(() => {
    const fetchGames = async () => {
      console.log("Загрузка активных игр...");
      try {
        const response = await axios.get(`${API_BASE}/active-games`);
        console.log("Активные игры получены:", response.data);
        setGames(response.data);
      } catch (err) {
        console.error("Ошибка при загрузке активных игр:", err);
      }
    };

    fetchGames();
  }, []);

  const filteredGames =
    filter === "all" ? games : games.filter((game) => game.type === filter);

  return (
    <div className="component-container">
      <h3>Список игр</h3>
      <label>
        Фильтр по типу игры:
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">Все</option>
          <option value="пуля">Пуля</option>
          <option value="блиц">Блиц</option>
          <option value="классика">Классика</option>
        </select>
      </label>
      <ul>
        {filteredGames.map((game) => (
          <li key={game.uuid}>
            <div>
              <strong>UUID:</strong> {game.uuid}
              <br />
              <strong>Создатель:</strong> {game.white || "Неизвестно"}
              <br />
              <strong>Ход:</strong> {game.current_turn}
            </div>
            <button onClick={() => onConnect(game.uuid)}>Подключиться</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GameList;