import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/api';
import "../styles/LoginPage.css";

const LoginPage = ({ setUser }) => { // Get setUser as a prop from App.js
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
  
    try {
      const data = await login(username, password);

      if (data.access) {
        localStorage.setItem('token', data.access);
        localStorage.setItem('username', username);

        // Immediately update the user state in App.js
        setUser({ username });

        setSuccess("Login Successful!");

        setTimeout(() => navigate("/posts"), 500);
      } else {
        throw new Error("No access token received.");
      }
    } catch (err) {
      console.error("Login failed:", err);
      setError("Invalid credentials, please try again.");
    }
  };

  return (
    <div className="form-container">
      <h1>Login</h1>
      {error && <p className="error">{error}</p>}
      {success && <p className="success">{success}</p>}
      <form onSubmit={handleLogin}>
        <input 
          type="text" 
          value={username} 
          onChange={(e) => { setUsername(e.target.value); setError(''); }}  
          placeholder="Username" 
        />
        <input 
          type="password" 
          value={password} 
          onChange={(e) => { setPassword(e.target.value); setError(''); }} 
          placeholder="Password" 
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;
