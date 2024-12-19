import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./AuthProvider";

const RequireAuth = ({ children }) => {
  const { token } = useAuth();
  const location = useLocation();

  console.log("Текущий токен:", token);

  if (!token) {
    console.log("Пользователь не авторизован. Перенаправление на /login.");
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

export default RequireAuth;
