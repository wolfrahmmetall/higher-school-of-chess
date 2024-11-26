import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Register from "./Register";
import Login from "./Login";
import Dashboard from "./Dashboard";
import RequireAuth from "./RequireAuth";
import Game from "./Game";
import GameSetup from "./GameSetup"; // Импорт нового компонента
import { AuthProvider } from "./AuthProvider";

import './index.css';
import './App.css'; 

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route 
            path="/dashboard" 
            element={
              <RequireAuth>
                <Dashboard />
              </RequireAuth>
            } 
          />
          <Route 
          path="/game/setup" 
          element={
          <RequireAuth>
            <GameSetup />
          </RequireAuth>
          } /> {/* Новый маршрут */}
          <Route 
            path="/game" 
            element={
              <RequireAuth>
                <Game />
              </RequireAuth>
            } 
          />
          <Route path="" element={<Navigate to="/login" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
