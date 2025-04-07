import React from 'react';

const PostItem = ({ post }) => {
  return (
    <div>
      <h2>{post.title}</h2>
      <h3>{post.author}</h3>
      {post.pic_url && (
        <img src={post.pic_url} alt="Post" style={{ width: "150px", height: "150px", borderRadius: "10px" }} />
      )}
      <p>{post.content}</p>
    </div>
  );
}


export default PostItem;
