import React, { createContext, useState, useContext, useEffect } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("authToken"));

  useEffect(() => {
    console.log("Текущее значение токена при загрузке:", token); // Лог начального состояния токена
  }, []);

  const login = (newToken) => {
    console.log("Функция login вызвана. Новый токен:", newToken); // Лог нового токена
    setToken(newToken);
    localStorage.setItem("authToken", newToken);
    console.log("Токен сохранён в localStorage."); // Подтверждение сохранения
  };

  const logout = () => {
    console.log("Функция logout вызвана. Текущий токен:", token); // Лог перед логаутом
    setToken(null);
    localStorage.removeItem("authToken");
    console.log("Токен удалён из localStorage."); // Подтверждение удаления
  };

  useEffect(() => {
    console.log("Токен изменён. Текущее значение:", token); // Лог при каждом изменении токена
  }, [token]);

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
