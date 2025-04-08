import React, { useEffect, useState } from 'react';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; 
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import PostList from './components/PostList';
import ProfilePage from './components/ProfilePage';
import './styles/App.css';

const App = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      fetch('/api/profile', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(response => response.json())
        .then(data => setUser(data))
        .catch(error => console.error('Error fetching user:', error));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <Router>
      <Navbar user={user} onLogout={handleLogout} />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/posts" element={<PostList />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/" element={<h1>{user ? `Welcome, ${user.username}` : 'Welcome, Guest'}</h1>} />
      </Routes>
    </Router>
  );
};

export default App;
