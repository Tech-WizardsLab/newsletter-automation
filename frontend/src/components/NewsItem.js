import React from "react";

const NewsItem = ({ article, approveNews, editNews, deleteNews }) => {
  return (
    <li className="news-item">
      <strong>{article.title}</strong> - 
      <a href={article.link} target="_blank" rel="noopener noreferrer">Read more</a>
      <span> ({article.category})</span> 
      
      <div className="news-buttons">
        {!article.approved && (
          <button className="approve-btn" onClick={() => approveNews(article.id)}>✅ Approve</button>
        )}
        <button className="edit-btn" onClick={() => editNews(article.id, article.title, article.category)}>✏️ Edit</button>
        <button className="delete-btn" onClick={() => deleteNews(article.id)}>❌ Delete</button>
      </div>
    </li>
  );
};

export default NewsItem;
