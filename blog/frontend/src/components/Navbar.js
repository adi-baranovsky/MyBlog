import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const username = localStorage.getItem('username'); // Retrieve the username

  const handleLogout = () => {
    localStorage.removeItem('token'); // Remove the token
    localStorage.removeItem('username'); // Remove the username
    window.location.href = "/login"; // Redirect to the login page
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
