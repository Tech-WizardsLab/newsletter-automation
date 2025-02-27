import React, { useState, useEffect } from "react";
import axios from "axios";

const GenerateNewsletter = ({ triggerUpdate }) => {
  const [newsletter, setNewsletter] = useState("");

  const fetchNewsletter = () => {
    axios.get("https://fuzzy-guide-r4p9r44vwq54c5gxj-5000.app.github.dev/generate-newsletter")
      .then((response) => {
        setNewsletter(response.data.newsletter);
      })
      .catch((error) => console.error("Error generating newsletter:", error));
  };

  useEffect(() => {
    fetchNewsletter();
  }, [triggerUpdate]); // Re-fetch newsletter when triggerUpdate changes

  return (
    <div className="newsletter-container">
      <h3>📜 Newsletter Preview</h3>
      <pre>{newsletter}</pre>
    </div>
  );
};

export default GenerateNewsletter;
