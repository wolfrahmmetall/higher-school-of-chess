import { useState } from "react";

const GameList = () => {
  const [filter, setFilter] = useState("all");

  const games = [
    { id: 1, name: "Игра 1", type: "пуля", creator: "Игрок 1", rating: 1500 },
    { id: 2, name: "Игра 2", type: "блиц", creator: "Игрок 2", rating: 1600 },
    { id: 3, name: "Игра 3", type: "классика", creator: "Игрок 3", rating: 1550 },
    { id: 4, name: "Игра 4", type: "пуля", creator: "Игрок 4", rating: 1450 },
  ];

  const filteredGames = filter === "all" ? games : games.filter(game => game.type === filter);

  const handleJoinGame = (gameId) => {
    console.log(`Подключение к игре с ID: ${gameId}`);
  };

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
          <li key={game.id}>
            <div>
              <strong>{game.name}</strong> ({game.type})<br />
              Создатель: {game.creator} - Рейтинг: {game.rating}
            </div>
            <button onClick={() => handleJoinGame(game.id)}>Подключиться к игре</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GameList;