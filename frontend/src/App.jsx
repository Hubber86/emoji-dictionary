import { useState } from "react";

function App() {
  const [word, setWord] = useState("");
  const [emoji, setEmoji] = useState("");
  const [error, setError] = useState("");

  const searchEmoji = async () => {
    if (!word.trim()) {
      setError("Please enter a word");
      setEmoji("");
      return;
    }

    try {
      // const res = await fetch(`https://emoji-backend.onrender.com/emoji?word=${word}`);
      const res = await fetch(`https://emoji-dictionary.onrender.com/emoji?word=${word}`);
      if (!res.ok) throw new Error("Emoji not found");
      const data = await res.json();
      setEmoji(data.emoji || "❓");
      setError("");
    } catch (err) {
      setEmoji("❓");
      setError(err.message);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px", fontFamily: "sans-serif" }}>
      <h1>Emoji Dictionary 📖</h1>

      <input
        type="text"
        value={word}
        onChange={(e) => setWord(e.target.value)}
        placeholder="Enter a word"
        style={{ padding: "10px", fontSize: "1rem", marginRight: "10px" }}
      />
      <button
        onClick={searchEmoji}
        style={{ padding: "10px 15px", fontSize: "1rem", cursor: "pointer" }}
      >
        Search
      </button>

      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}

      {emoji && (
        <h2 style={{ fontSize: "4rem", marginTop: "20px" }}>
          {emoji}
        </h2>
      )}
    </div>
  );
}

export default App;
