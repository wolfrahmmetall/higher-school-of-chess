import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./AuthProvider";

const RequireAuth = ({ children }) => {
  const { token } = useAuth();
  const location = useLocation();

  if (!token) {
    // Сохраняем текущую страницу для возврата после входа
    console.log("Пользователь не авторизован. Перенаправление на /login.");
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

export default RequireAuth;
