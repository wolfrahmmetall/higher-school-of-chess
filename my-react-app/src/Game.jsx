import React, { useEffect, useState } from "react";
import axios from "axios";

const Game = () => {
  const [board, setBoard] = useState([]);
  const [currentTurn, setCurrentTurn] = useState("");
  const [gameStatus, setGameStatus] = useState("");
  const [startSquare, setStartSquare] = useState("");
  const [endSquare, setEndSquare] = useState("");

  const API_BASE = "http://127.0.0.1:8000";

  // Fetch the game state from the server
  const fetchGameState = async () => {
    try {
      const response = await axios.get(`${API_BASE}/chess/state`);
      setBoard(response.data.board);
      setCurrentTurn(response.data.current_turn);
    } catch (error) {
      console.error("Ошибка при получении состояния игры:", error);
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
      setStartSquare("");
      setEndSquare("");
    } catch (error) {
      console.error("Ошибка при выполнении хода:", error);
    }
  };

  useEffect(() => {
    fetchGameState(); // Fetch the initial game state when the component loads
  }, []);

  return (
    <div className="game-container">
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
    </div>
  );
};

export default Game;
