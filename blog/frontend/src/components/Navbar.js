import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const [username, setUsername] = useState(localStorage.getItem('username') || '');

  useEffect(() => {
    const handleStorageChange = () => {
      setUsername(localStorage.getItem('username') || '');
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  useEffect(() => {
    setUsername(localStorage.getItem('username') || '');
  }, [localStorage.getItem('username')]); // 🔥 This will trigger a re-render

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setUsername(''); // Update state
    window.location.href = "/login";
  };

  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        {username ? (
          <>
            <li><Link to="/posts">Posts</Link></li>
            <li><Link to={`/profile/?user=${username}`}>Profile</Link></li>
            <li><Link to="#" className="logout" onClick={handleLogout}>Logout</Link></li>
          </>
        ) : (
          <>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Register</Link></li>
          </>
        )}
      </ul>
      <div className="welcome">
        {username ? `Welcome, ${username}` : 'Welcome, Guest'}
      </div>
    </nav>
  );
};

export default Navbar;
