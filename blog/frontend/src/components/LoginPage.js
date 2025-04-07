import React, { useState } from 'react';
import { login } from '../services/api';

const LoginPage = () => {
  const [username, setUsername] = useState('');  // הוסף את המשתנה הזה
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await login(username, password);  // השתמש ב-username במקום ב-email
      if (data.token) {
        window.location.href = "/posts"; 
      }
    } catch (err) {
      setError("Invalid credentials, please try again.");
    }
  }

  return (
    <div>
      <h1>Login</h1>
      {error && <p>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)}  // עדכון המשתנה username
          placeholder="Username" 
        />
        <input 
          type="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          placeholder="Password" 
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginPage;
