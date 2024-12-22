import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import './Game.css';
import whitepawn from './assets/white-pawn.png';
import whiteknight from './assets/white-knight.png';
import whitebishop from './assets/white-bishop.png';
import whiterook from './assets/white-rook.png';
import whitequeen from './assets/white-queen.png';
import whiteking from './assets/white-king.png';
import blackpawn from './assets/black-pawn.png';
import blackknight from './assets/black-knight.png';
import blackbishop from './assets/black-bishop.png';
import blackrook from './assets/black-rook.png';
import blackqueen from './assets/black-queen.png';
import blackking from './assets/black-king.png';

const pieceMapping = {
  '♙': whitepawn,
  '♘': whiteknight,
  '♗': whitebishop,
  '♖': whiterook,
  '♕': whitequeen,
  '♔': whiteking,
  '♟': blackpawn,
  '♞': blackknight,
  '♝': blackbishop,
  '♜': blackrook,
  '♛': blackqueen,
  '♚': blackking,
};

const Game = () => {
  const { uuid } = useParams(); // Получаем UUID из параметров маршрута
  const [board, setBoard] = useState([]);
  const [currentTurn, setCurrentTurn] = useState("");
  const [gameStatus, setGameStatus] = useState("");
  const [startSquare, setStartSquare] = useState("");
  const [endSquare, setEndSquare] = useState("");
  const [selectedSquare, setSelectedSquare] = useState(null);
  const [gameResult, setGameResult] = useState(null);

  // const API_BASE = "http://5.35.5.18/api";
  const API_BASE = "http://127.0.0.1:8000"

  const prepareBoard = (board) => {
    console.log("Preparing board:", board); // Лог текущей доски
    return board.map((row) =>
      row.map((cell) => (cell && typeof cell === "object" ? cell.name : cell || ""))
    );
  };

  const fetchGameState = async () => {
    console.log("Fetching game state for UUID:", uuid);
    try {
      const response = await axios.get(`${API_BASE}/chess/${uuid}/state`);
      console.log("Game state fetched successfully:", response.data);
      setBoard(prepareBoard(response.data.board));
      setCurrentTurn(response.data.current_turn);
      console.log(response.data.message)
    } catch (error) {
      console.error("Error fetching game state:", error);
    }
  };


  useEffect(() => {
    console.log("Component mounted, fetching game state.");
    fetchGameState();
  }, []);
  
  const makeMove = async (start, end) => {
    console.log("Making move from:", start, "to:", end);
    try {
      const token = localStorage.getItem("authToken"); // Токен аутентификации из localStorage
      console.log("Токен из localStorage:", token);
      if (!token) {
        throw new Error("Вы не авторизованы.");
      }

      const headers = { Authorization: `Bearer ${token}` }; // Передаем токен в заголовке

      if (start && end) {
        const response = await axios.post(`${API_BASE}/chess/${uuid}/move`, {
          start: start,
          end: end,
        }, {headers});
        console.log("Move successful, response:", response.data);
        setBoard(prepareBoard(response.data.board));
        setCurrentTurn(response.data.current_turn);
        setGameResult(response.data.result);
        setStartSquare("");
        setEndSquare("");
        setSelectedSquare(null);
      }
    } catch (error) {
      console.error("Error making move:", error);
    }
  };

  const handleSquareClick = (rowIndex, colIndex) => {
    const file = String.fromCharCode(97 + colIndex); // a-h
    const rank = 8 - rowIndex; // 8-1
    const square = `${file}${rank}`;

    console.log("Square clicked:", square);

    if (!startSquare) {
      console.log("Start square selected:", square);
      setStartSquare(square);
      setSelectedSquare(square);
    } else {
      if (square !== startSquare) {
        console.log("End square selected:", square);
        setEndSquare(square);
        makeMove(startSquare, square);
      }
    }
  };


  return (
    <div className="game-container">
      <h2>Шахматная игра</h2>
      {gameResult ? (
        <p className="game-result">
          Результат игры: {gameResult === "draw" ? "Ничья" : `${gameResult}`}
        </p>
      ) : (
        <p>Текущий ход: {currentTurn}</p>
      )}
      <div className="chess-board-container">
        <div className="notation-row">
          <div className="notation-cell"></div>
          {"ABCDEFGH".split("").map((letter) => (
            <span key={letter} className="notation-cell">
              {letter}
            </span>
          ))}
        </div>
        {board.map((row, rowIndex) => (
          <div key={rowIndex} className="board-row">
            <span className="notation-cell">{8 - rowIndex}</span>
            {row.map((cell, colIndex) => (
              <span
                key={colIndex}
                className={`board-cell ${
                  (rowIndex + colIndex) % 2 === 0 ? "light-cell" : "dark-cell"
                } ${selectedSquare === `${String.fromCharCode(97 + colIndex)}${8 - rowIndex}` ? "selected-cell" : ""}`}
                onClick={() => handleSquareClick(rowIndex, colIndex)}
              >
                {cell && pieceMapping[cell] ? (
                  <img src={pieceMapping[cell]} className="chess-piece" alt={cell} />
                ) : '\u00A0'}
              </span>
            ))}
          </div>
        ))}
      </div>
      {!gameResult && (
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
          <button onClick={() => makeMove(startSquare, endSquare)}>Сделать ход</button>
        </div>
      )}
    </div>
  );
};

export default Game;
