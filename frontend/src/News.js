import React, { useEffect, useState } from "react";
import axios from "axios";
import NewsItem from "./components/NewsItem";
import GenerateNewsletter from "./components/GenerateNewsletter";
import "./styles/News.css";

const News = () => {
  const [news, setNews] = useState([]);

  useEffect(() => {
    fetchNews();
  }, []);

  // Fetch news from Flask backend
  const fetchNews = () => {
    axios.get("https://fuzzy-guide-r4p9r44vwq54c5gxj-5000.app.github.dev/news")
      .then((response) => {
        setNews(response.data.news);
      })
      .catch((error) => {
        console.error("Error fetching news:", error);
      });
  };

  const approveNews = (id) => {
    axios.put(`https://fuzzy-guide-r4p9r44vwq54c5gxj-5000.app.github.dev/news/${id}/approve`)
      .then(() => {
        setNews((prevNews) =>
          prevNews.map((article) =>
            article.id === id ? { ...article, approved: 1 } : article
          )
        );
      })
      .catch((error) => console.error("Error approving news:", error));
  };

  // Edit news
  const editNews = (id, currentTitle, currentCategory) => {
    const newTitle = prompt("Edit title:", currentTitle);
    const newCategory = prompt("Edit category:", currentCategory);
    if (newTitle && newCategory) {
      axios.put(`https://fuzzy-guide-r4p9r44vwq54c5gxj-5000.app.github.dev/news/${id}`, {
        title: newTitle,
        category: newCategory
      })
      .then(() => fetchNews())
      .catch((error) => console.error("Error editing news:", error));
    }
  };

  // Delete news
  const deleteNews = (id) => {
    if (window.confirm("Are you sure you want to delete this news item?")) {
      axios.delete(`https://fuzzy-guide-r4p9r44vwq54c5gxj-5000.app.github.dev/news/${id}`)
        .then(() => fetchNews())
        .catch((error) => console.error("Error deleting news:", error));
    }
  };

  return (
    <div className="news-container">
      <h2>Latest News</h2>
      <ul className="news-list">
        {news.length > 0 ? (
          news.map((article) => (
            <NewsItem 
              key={article.id}
              article={article}
              approveNews={approveNews}
              editNews={editNews}
              deleteNews={deleteNews}
            />
          ))
        ) : (
          <p>No news available.</p>
        )}
      </ul>
      
      <GenerateNewsletter />
    </div>
  );
};

export default News;
