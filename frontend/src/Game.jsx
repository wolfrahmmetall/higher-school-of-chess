import React, { useEffect, useState } from "react";
import axios from "axios";

const Game = () => {
  const [board, setBoard] = useState([]);
  const [currentTurn, setCurrentTurn] = useState("");
  const [gameStatus, setGameStatus] = useState("");
  const [startSquare, setStartSquare] = useState("");
  const [endSquare, setEndSquare] = useState("");

  const API_BASE = "http://127.0.0.1:8000";

  const prepareBoard = (board) => {
    return board.map((row) =>
      row.map((cell) => (cell && typeof cell === "object" ? cell.name : cell || ""))
    );
  };

  const fetchGameState = async () => {
    try {
      const response = await axios.get(`${API_BASE}/chess/state`);
      setBoard(prepareBoard(response.data.board));
      setCurrentTurn(response.data.current_turn);
    } catch (error) {
      console.error("Ошибка при получении состояния игры:", error);
    }
  };

  const makeMove = async () => {
    try {
      const response = await axios.post(`${API_BASE}/chess/move`, {
        start: startSquare,
        end: endSquare,
      });
      setBoard(prepareBoard(response.data.board));
      setCurrentTurn(response.data.current_turn);
      setStartSquare("");
      setEndSquare("");
    } catch (error) {
      console.error("Ошибка при выполнении хода:", error);
    }
  };

  useEffect(() => {
    fetchGameState();
  }, []);

  return (
    <div className="game-container">
      <h2>Шахматная игра</h2>
      <p>Текущий ход: {currentTurn}</p>
      <p>Статус игры: {gameStatus}</p>
      
      <div className="chess-board-container">
        {/* Доска с левой нотацией */}
        {board.map((row, rowIndex) => (
          <div key={rowIndex} className="board-row">
            {/* Нотация слева */}
            <span className="notation-cell">{8 - rowIndex}</span>
            {row.map((cell, colIndex) => (
              <span
                key={colIndex}
                className={`board-cell ${
                  (rowIndex + colIndex) % 2 === 0 ? "light-cell" : "dark-cell"
                }`}
              >
                {cell || ""}
              </span>
            ))}
          </div>
        ))}
        {/* Нотация сверху */}
        <div className="notation-row">
          <span className="notation-cell"></span>
          {"ABCDEFGH".split("").map((letter) => (
            <span key={letter} className="notation-cell">
              {letter}
            </span>
          ))}
        </div>
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
