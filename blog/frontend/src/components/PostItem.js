import React, { useEffect, useState } from "react";
import "../styles/PostList.css";

const PostItem = ({ post }) => {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [user, setUser] = useState(null); // Assuming you have a way to check logged-in user

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem("token"); // Retrieve the token from localStorage

      if (!token) {
        console.error("No token found!");
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:8000/api/auth/user/", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`, // Use Bearer + token format
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch user: ${response.statusText}`);
        }

        const userData = await response.json();
        setUser(userData);
        console.log("User data:", userData);
      } catch (error) {
        console.error("Failed to fetch user:", error);
      }
    };

    fetchUser();
  }, []); // Empty array to fetch on mount

  const handleCommentSubmit = async (e) => {
    e.preventDefault();

    if (!newComment.trim()) return;

    const token = localStorage.getItem("token"); // Retrieve token from localStorage

    if (!token) {
      console.error("No token found for commenting!");
      return;
    }

    const response = await fetch(`http://127.0.0.1:8000/comments/create/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`, // Use Bearer + token format for comment submission
      },
      body: JSON.stringify({ content: newComment, post: post.id }),
    });

    if (response.ok) {
      const data = await response.json();
      setComments([...comments, data]);
      setNewComment("");
    } else {
      console.error("Failed to post comment");
    }
  };

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
          comments.map((comment) => (
            <div key={comment.id} className="comment">
              <p>
                <strong>{comment.author}</strong>: {comment.content}
              </p>
              <p>Likes: {comment.likes_count}</p>
            </div>
          ))
        ) : (
          <p>No comments yet</p>
        )}
      </div>

      {user ? (
        <form onSubmit={handleCommentSubmit} className="comment-form">
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Write a comment..."
          />
          <button type="submit">Post Comment</button>
        </form>
      ) : (
        <p>
          <i>Login to add a comment</i>
        </p>
      )}
    </div>
  );
};

export default PostItem;
