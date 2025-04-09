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
    const username = localStorage.getItem('username'); // Retrieve the username
    if (token && username) {
      setUser({ username }); // Set the user state with the username
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setUser(null); // Reset user state
  };

  return (
    <Router>
      <Navbar user={user} onLogout={handleLogout} />
      <Routes>
        <Route path="/login" element={<LoginPage setUser={setUser} />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/posts" element={<PostList />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/" element={<h1>{user ? `Welcome, ${user.username}` : 'Welcome, Guest'}</h1>} />
      </Routes>
    </Router>
  );
};

export default App;
