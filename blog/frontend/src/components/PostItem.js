import React, { useEffect, useState } from "react";
import "../styles/PostList.css";

const PostItem = ({ post }) => {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");

  // Just grab the token once from localStorage
  const token = localStorage.getItem("token");

  useEffect(() => {
    const fetchUserAndComments = async () => {
      try {
        if (token) {
          const userResponse = await fetch("http://127.0.0.1:8000/api/auth/user/", {
            method: "GET",
            headers: {
              "Authorization": `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          });

          if (userResponse.ok) {
            const userData = await userResponse.json();
            setUser(userData);
          }
        }

        const commentsResponse = await fetch(`http://127.0.0.1:8000/api/comments/?post=${post.id}`, {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (commentsResponse.ok) {
          const commentsData = await commentsResponse.json();
          setComments(commentsData);
        } else {
          const errText = await commentsResponse.text();
          console.error("Failed to fetch comments:", errText);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchUserAndComments();
  }, [post.id, token]);

  const handleCommentSubmit = async (e) => {
    e.preventDefault();

    if (!newComment.trim()) {
      console.error("Comment content cannot be empty.");
      return;
    }

    const commentData = {
      content: newComment,
      post: post.id,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/api/comments/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(commentData),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Failed to post comment.");
      }

      console.log("Comment posted successfully:", data);
      setNewComment("");

      // Refresh comments after posting
      setComments((prev) => [...prev, data]);
    } catch (error) {
      console.error("Error posting comment:", error);
    }
  };

  return (
    <div className="post-card">
      <h2 className="post-title">{post.title}</h2>
      <h3 className="post-author">By: {post.author}</h3>
      {post.pic && <img src={post.pic} alt="Post" className="post-image" />}
      <p className="post-content">{post.content}</p>
      <div className="post-likes-count">{comments.length}💬  {post.likes_count}❤  </div>
      <div className="comments-section">
        {comments.length > 0 ? (
          comments.map((comment) => (
            <div key={comment.id} className="comment">
              <p>
              <strong>{comment.author_username}</strong>: {comment.content}
              </p>
            </div>
          ))
        ) : (
          <p>No comments yet</p>
        )}
      </div>

      {user ? (
        <form onSubmit={handleCommentSubmit} className="comment-form">
        <div className="comment-input-wrapper">
          
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Write a comment..."
          />
          <button type="submit" className="submit-btn">➤</button>
        </div>
      </form>
      
      ) : (
        <p>
          <i>Login to add a comment</i>
        </p>
      )}

      {error && <p>{error}</p>}
    </div>
  );
};

export default PostItem;

