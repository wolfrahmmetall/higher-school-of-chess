import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthProvider';

const LoginForm = () => {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login: authenticate } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    console.log("Попытка входа с данными:");
    console.log("Логин:", login);
    console.log("Пароль:", password);

    try {
      const response = await fetch('http://5.35.5.18/api/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login, password }),
      });

      console.log("Ответ сервера:", response);
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Ошибка авторизации:", errorData);
        setError(errorData.detail || 'Invalid login or password');
        return;
      }

      const data = await response.json();
      console.log("Успешный ответ от сервера:", data);
      
      authenticate(data.token); // Сохраняем токен
      console.log("Токен сохранён, переход на /dashboard");
      navigate('/dashboard');  // Переход на защищённую страницу
    } catch (error) {
      console.error("Ошибка при выполнении запроса на логин:", error);
      setError('Something went wrong. Please try again.');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label>Login:</label>
          <input
            type="text"
            value={login}
            onChange={(e) => setLogin(e.target.value)}
            style={{ width: '100%', padding: '8px', margin: '5px 0' }}
            required
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', padding: '8px', margin: '5px 0' }}
            required
          />
        </div>
        {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}
        <button type="submit" style={{ padding: '10px 20px', background: '#007bff', color: '#fff', border: 'none', borderRadius: '4px' }}>
          Login
        </button>
      </form>
    </div>
  );
};

export default LoginForm;
