import React from "react";
import { useAuth } from "./AuthProvider";
import { useNavigate } from "react-router-dom";
import PlayerRating from "./components/PlayerRating";
import GameList from "./components/GameList";
import './App.css';

const Dashboard = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };
  const handleNewGame = () => {
    navigate("/game/setup");
  };

  return (
    <div className="container">
      <h2>Добро пожаловать в Дашборд</h2>
      <button onClick={handleLogout}>Logout</button>
      <div className="dashboard-container">
        <div className="component-container">
          <button onClick={handleNewGame}>Создать новую игру</button>
        </div>
      </div>

      <div className="dashboard-container">
        <div className="component-container">
          <PlayerRating />
        </div>
        
        <div className="component-container">
          <GameList />
        </div>
      </div>
    </div>
  );
};


export default Dashboard;
