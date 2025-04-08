import React, { useEffect, useState } from 'react';
import PostItem from './PostItem';
import "../styles/PostList.css"; 

const PostList = () => {
  const [posts, setPosts] = useState([]);
  const [page, setPage] = useState(1);
  const [nextPage, setNextPage] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      const response = await fetch(`http://127.0.0.1:8000/posts/?page=${page}`);
      const data = await response.json();
      setPosts(data.results);
      setNextPage(data.next);
    };
    fetchPosts();
  }, [page]);

  return (
    <div className="post-list-container">
      {posts.map(post => (
        <PostItem key={post.id} post={post} />
      ))}
      <div className="pagination-buttons">
        <button onClick={() => setPage(prevPage => prevPage - 1)} disabled={page <= 1}>Previous</button>
        <button onClick={() => setPage(prevPage => prevPage + 1)} disabled={!nextPage}>Next</button>
      </div>
    </div>
  );
}

export default PostList;
