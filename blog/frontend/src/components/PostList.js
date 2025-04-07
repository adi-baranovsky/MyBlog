import React, { useEffect, useState } from 'react';
import { getPosts } from '../services/api';
import PostItem from './PostItem';

const PostList = () => {
  const [posts, setPosts] = useState([]);
  const [page, setPage] = useState(1);
  const [nextPage, setNextPage] = useState(null); // הוספנו את nextPage

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/posts/?page=${page}`);
        const data = await response.json();
        console.log("Data:", data);
        setPosts(data.results);
        setNextPage(data.next); // עדכון אם יש עמודים נוספים
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    };
    
    fetchPosts();
  }, [page]);

  return (
    <div>
      <h1>Posts</h1>
      {posts.map(post => (
        <PostItem key={post.id} post={post} />
      ))}
      <button onClick={() => setPage(prevPage => prevPage - 1)} disabled={page <= 1}>Previous</button>
      <button 
        onClick={() => setPage(prevPage => prevPage + 1)} 
        disabled={!nextPage}>Next</button>
    </div>
  );
}

export default PostList;
