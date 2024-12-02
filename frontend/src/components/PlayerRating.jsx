import { useState } from "react";

const PlayerRating = () => {
  const [filter, setFilter] = useState("all");

  const players = [
    { name: "Игрок 1", rating: 1500, type: "пуля" },
    { name: "Игрок 2", rating: 1600, type: "блиц" },
    { name: "Игрок 3", rating: 1550, type: "классика" },
    { name: "Игрок 4", rating: 1450, type: "пуля" },
  ];

  const filteredPlayers = filter === "all" ? players : players.filter(player => player.type === filter);

  return (
    <div className="component-container">
      <h3>Рейтинг игроков</h3>
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
        {filteredPlayers.map((player, index) => (
          <li key={index}>
            {player.name} - Рейтинг: {player.rating} ({player.type})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PlayerRating;