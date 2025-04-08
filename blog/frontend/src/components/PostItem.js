import React, { useEffect, useState } from 'react';
import "../styles/PostList.css";

const PostItem = ({ post }) => {
  const [comments, setComments] = useState([]);
  
  useEffect(() => {
    const fetchComments = async () => {
      const response = await fetch(`http://127.0.0.1:8000/comments/?post=${post.id}`);
      const data = await response.json();
      setComments(data);
    };

    fetchComments();
  }, [post.id]);

  return (
    <div className="post-card">
      <h2 className="post-title">{post.title}</h2>
      <h3 className="post-author">By: {post.author}</h3>
      {post.pic && <img src={post.pic} alt="Post" className="post-image" />}
      <p className="post-content">{post.content}</p>
      <div className="post-likes-count">Likes: {post.likes_count}</div>
      <div className="comments-section">
        <h4>Comments:</h4>
        {comments.length > 0 ? (
          comments.map(comment => (
            <div key={comment.id} className="comment">
              <p><strong>{comment.author}</strong>: {comment.content}</p>
              <p>Likes: {comment.likes_count}</p>
            </div>
          ))
        ) : (
          <p>No comments yet</p>
        )}
      </div>
    </div>
  );
};

export default PostItem;