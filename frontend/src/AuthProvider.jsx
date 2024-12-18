import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('authToken') || null);
  const navigate = useNavigate();

  // Проверяем наличие токена при запуске
  useEffect(() => {
    if (token) {
      localStorage.setItem('authToken', token);
    } else {
      localStorage.removeItem('authToken');
    }
  }, [token]);

  const login = (newToken) => {
    setToken(newToken);
    localStorage.setItem('authToken', newToken);
    navigate('/dashboard'); // Перенаправляем на дашборд после логина
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem('authToken');
    navigate('/login'); // Возвращаем на страницу логина
  };

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);