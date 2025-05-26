import React, { useState } from "react";

export default function BusinessIdeaGenerator() {
  const [prompt, setPrompt] = useState("");
  const [idea, setIdea] = useState("");

  const handleGenerate = () => {
    setIdea(`🚀 Business-Idee basierend auf: "${prompt}"`);
  };

  return (
    <div className="container">
      <div className="menu-icon">☰</div>
      <h1 className="title">Generate Business Idea</h1>

      <div className="input-group">
        <input
          type="text"
          placeholder="Enter a prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button onClick={handleGenerate}>Generate</button>
      </div>

      <h2 className="label">Generated Idea</h2>
      <textarea
        className="idea-box"
        readOnly
        value={idea}
        placeholder=""
      />

      <div className="tabs">
        <span className="tab active">Validierung</span>
        <span className="tab inactive">Quellen</span>
      </div>
    </div>
  );
}
