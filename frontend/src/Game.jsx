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
  const { uuid } = useParams();
  const [board, setBoard] = useState([]);
  const [currentTurn, setCurrentTurn] = useState("");
  const [gameStatus, setGameStatus] = useState("");
  const [startSquare, setStartSquare] = useState("");
  const [endSquare, setEndSquare] = useState("");
  const [selectedSquare, setSelectedSquare] = useState(null);
  const [gameResult, setGameResult] = useState(null);
  const [whitePlayer, setWhitePlayer] = useState(null);
  const [blackPlayer, setBlackPlayer] = useState(null);
  const [theme, setTheme] = useState("light"); // Default theme
  
  // const API_BASE = "http://127.0.0.1:8000";
  const API_BASE = "http://5.35.5.18/api/";
  const prepareBoard = (board) => {
    return board.map((row) =>
      row.map((cell) => (cell && typeof cell === "object" ? cell.name : cell || ""))
    );
  };

  const fetchGameState = async () => {
    try {
      const response = await axios.get(`${API_BASE}/chess/${uuid}/`);
      setBoard(prepareBoard(response.data.board));
      setCurrentTurn(response.data.current_turn);
    } catch (error) {
      console.error("Error fetching game state:", error);
    }
  };

  const fetchPlayers = async () => {
    try {
      const whiteResponse = await axios.get(`${API_BASE}/chess/${uuid}/white-player`);
      setWhitePlayer(whiteResponse.data.white_player);

      const blackResponse = await axios.get(`${API_BASE}/chess/${uuid}/black-player`);
      setBlackPlayer(blackResponse.data.black_player);
    } catch (error) {
      console.error("Error fetching player data:", error);
    }
  };
  const toggleTheme = () => {
    const nextTheme =
      theme === "light"
        ? "dark"
        : theme === "dark"
        ? "yellow"
        : theme === "yellow"
        ? "purple"
        : "light";
    setTheme(nextTheme);
  };



  useEffect(() => {
    fetchGameState();
    fetchPlayers(); 
    document.body.className = theme;
  }, [theme]);

  const makeMove = async (start, end) => {
    try {
      const token = localStorage.getItem("authToken");
      if (!token) {
        throw new Error("Вы не авторизованы.");
      }

      const headers = { Authorization: `Bearer ${token}` };
      if (start && end) {
        const response = await axios.post(
          `${API_BASE}/chess/${uuid}/move`,
          { start, end },
          { headers }
        );
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
    const file = String.fromCharCode(97 + colIndex);
    const rank = 8 - rowIndex;
    const square = `${file}${rank}`;

    if (!startSquare) {
      setStartSquare(square);
      setSelectedSquare(square);
    } else {
      setEndSquare(square);
      makeMove(startSquare, square);
    }
  };

  return (
    <div className="game-container">
      <h2 className="player-info">Шахматная игра</h2>
      <button onClick={toggleTheme} className="theme-toggle">
        Переключить тему ({theme === "light" ? "Светлая" : theme === "dark" ? "Ночная" : theme === "yellow" ? "Желтая" : "Фиолетовая"})
      </button>
      {gameResult ? (
        <p className="game-result">
          Результат игры: {gameResult === "draw" ? "Ничья" : `${gameResult}`}
        </p>
      ) : (
        <p>Текущий ход: {currentTurn}</p>
      )}
      <div className="game-layout">
        <div className="player-info player-info-left">
          <h3>
            Белый игрок: {whitePlayer ? `${whitePlayer.login}` : "Waiting..."}</h3> 
          <h3>(ELO: {whitePlayer? `${whitePlayer.elo}` : " "})
          </h3>
        </div>
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
                  } ${
                    selectedSquare === `${String.fromCharCode(97 + colIndex)}${8 - rowIndex}`
                      ? "selected-cell"
                      : ""
                  }`}
                  onClick={() => handleSquareClick(rowIndex, colIndex)}
                >
                  {cell && pieceMapping[cell] ? (
                    <img src={pieceMapping[cell]} className="chess-piece" alt={cell} />
                  ) : "\u00A0"}
                </span>
              ))}
            </div>
          ))}
        </div>
        <div className="player-info player-info-right">
          <h3>
            Черный игрок: {blackPlayer ? `${blackPlayer.login}` : "Waiting..."}
          </h3> 
          <h3>
            (ELO: {blackPlayer? `${blackPlayer.elo}` : " "})
          </h3>
        </div>
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
