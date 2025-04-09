export const getPosts = async (page) => {
    const response = await fetch(`/api/posts/?page=${page}`);
    const data = await response.json();
    return data.results;
  };
  
  export const getProfile = async () => {
    const response = await fetch('/api/profile', { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } });
    const data = await response.json();
    return data;
  };
  
  export const updateProfile = async (profileData) => {
    const response = await fetch('/api/profile', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(profileData)
    });
    return response.json();
  };
  
  export const login = async (username, password) => {
    const response = await fetch('http://127.0.0.1:8000/api/token/', { // Ensure this URL is correct
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    
    if (!response.ok) {
      throw new Error('Invalid credentials');
    }
    
    return await response.json();
  };
  
  
  
  
  export const register = async (email, password) => {
    const response = await fetch('/api/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await response.json();
    return data;
  };
