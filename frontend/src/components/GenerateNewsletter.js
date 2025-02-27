import React, { useState } from "react";
import axios from "axios";
import "../styles/Newsletter.css";

const GenerateNewsletter = () => {
  const [newsletter, setNewsletter] = useState("");

  const generateNewsletter = () => {
    axios.get("https://fuzzy-guide-r4p9r44vwq54c5gxj-5000.app.github.dev/generate-newsletter")
      .then((response) => {
        setNewsletter(response.data.newsletter);
      })
      .catch((error) => console.error("Error generating newsletter:", error));
  };

  return (
    <div className="newsletter-container">
      <button onClick={generateNewsletter} className="generate-btn">
        📩 Generate Newsletter
      </button>

      {newsletter && (
        <div className="newsletter-preview">
          <h3>📜 Newsletter Preview</h3>
          <pre>{newsletter}</pre>
        </div>
      )}
    </div>
  );
};

export default GenerateNewsletter;
