import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Register from "./Register";
import Login from "./Login";
import Dashboard from "./Dashboard";
import RequireAuth from "./RequireAuth";
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
          <Route path="" element={<Navigate to="/login" />} /> {/* Редирект на /login */}
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
