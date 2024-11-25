import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Game = () => {
  const [board, setBoard] = useState([]);
  const [currentTurn, setCurrentTurn] = useState("");
  const [gameStatus, setGameStatus] = useState("");
  const [startSquare, setStartSquare] = useState("");
  const [endSquare, setEndSquare] = useState("");
  const [gameTime, setGameTime] = useState(10); // Default game time in minutes
  const [increment, setIncrement] = useState(5); // Default increment in seconds
  const [isGameSetup, setIsGameSetup] = useState(false);
  const navigate = useNavigate();

  const API_BASE = "http://127.0.0.1:8000";

  // Fetch initial game state
  const fetchGameState = async () => {
    try {
      const response = await axios.get(`${API_BASE}/chess/state`);
      setBoard(response.data.board);
      setCurrentTurn(response.data.current_turn);
      setGameStatus(response.data.status);
    } catch (error) {
      console.error("Ошибка при получении состояния игры:", error);
    }
  };

  // Setup new game
  const setupGame = async () => {
    try {
      const response = await axios.post(`${API_BASE}/chess/setup`, {
        game_time: gameTime,
        increment: increment,
      });
      setIsGameSetup(true);
      console.log("Игра настроена:", response.data);
      fetchGameState(); // Fetch the initial state after setup
    } catch (error) {
      console.error("Ошибка при настройке игры:", error);
    }
  };

  // Make a move
  const makeMove = async () => {
    try {
      const response = await axios.post(`${API_BASE}/chess/move`, {
        start: startSquare,
        end: endSquare,
      });
      setBoard(response.data.board);
      setCurrentTurn(response.data.current_turn);
      setGameStatus(response.data.status);
      setStartSquare("");
      setEndSquare("");
    } catch (error) {
      console.error("Ошибка при выполнении хода:", error);
    }
  };

  // Restart the game
  const restartGame = async () => {
    try {
      const response = await axios.post(`${API_BASE}/chess/restart`);
      console.log("Игра перезапущена:", response.data);
      fetchGameState();
    } catch (error) {
      console.error("Ошибка при перезапуске игры:", error);
    }
  };

  useEffect(() => {
    if (isGameSetup) {
      fetchGameState();
    }
  }, [isGameSetup]);

  return (
    <div className="game-container">
      {!isGameSetup ? (
        <div className="game-setup">
          <h2>Настройка новой игры</h2>
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
      ) : (
        <div className="game-board">
          <h2>Шахматная игра</h2>
          <p>Текущий ход: {currentTurn}</p>
          <p>Статус игры: {gameStatus}</p>
          <div className="chess-board">
            {board.map((row, rowIndex) => (
              <div key={rowIndex} className="board-row">
                {row.map((cell, colIndex) => (
                  <div key={colIndex} className="board-cell">
                    {cell || ""}
                  </div>
                ))}
              </div>
            ))}
          </div>
          <div className="move-inputs">
            <input
              type="text"
              value={startSquare}
              placeholder="Начало (например, e2)"
              onChange={(e) => setStartSquare(e.target.value)}
            />
            <input
              type="text"
              value={endSquare}
              placeholder="Конец (например, e4)"
              onChange={(e) => setEndSquare(e.target.value)}
            />
            <button onClick={makeMove}>Сделать ход</button>
          </div>
          <button onClick={restartGame}>Перезапустить игру</button>
        </div>
      )}
    </div>
  );
};

export default Game;
