import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div>
      <h1>Welcome to the Blog!</h1>
      <nav>
        <ul>
          <li><Link to="/posts">View Posts</Link></li>
          <li><Link to="/profile">Your Profile</Link></li>
          <li><Link to="/login">Login</Link></li>
          <li><Link to="/register">Register</Link></li>
        </ul>
      </nav>
    </div>
  );
}

export default HomePage;
