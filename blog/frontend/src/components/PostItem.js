import React, { useEffect, useState } from "react";
import "../styles/PostList.css";
import { FaHeart } from "react-icons/fa";

const PostItem = ({ post }) => {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");
  const [liked, setLiked] = useState(false);

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

  useEffect(() => {
    const checkLiked = async () => {
      if (!user) return;
  
      const response = await fetch(`http://127.0.0.1:8000/api/likes/check_liked/?object_id=${post.id}&content_type=7`, {
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });
  
      if (response.ok) {
        const data = await response.json();
        setLiked(data.liked); // Set the initial liked state
      }
    };
  
    checkLiked();
  }, [user, post.id, token]);  // Ensure it runs when the user or post changes
  

  const toggleLike = async () => {
    if (!user) return;
  
    const contentTypeId = 7; // Post content type ID
    const likeData = {
      object_id: post.id,
      content_type: contentTypeId,
    };
  
    try {
      const response = await fetch("http://127.0.0.1:8000/api/likes/", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(likeData),
      });
  
      if (response.ok) {
        if (liked) {
          // Unliked
          post.likes_count = Math.max(0, post.likes_count - 1);
          setLiked(false);
        } else {
          // Liked
          post.likes_count += 1;
          setLiked(true);
        }
      } else {
        const errorText = await response.text();
        console.error("Like toggle failed:", errorText);
      }
    } catch (error) {
      console.error("Error toggling like:", error);
    }
  };
  
  
  

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

      setNewComment("");
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

      <div className="post-likes-count">
      <button className="comment-btn">💬 {comments.length}</button>

        <button onClick={toggleLike} className="like-btn">
        <FaHeart className={`heart-icon ${liked ? "liked" : ""}`} />

          <span style={{ marginLeft: "4px" }}>{post.likes_count}</span>
        </button>
      </div>

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
