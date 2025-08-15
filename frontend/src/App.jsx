import { useState } from "react";

function App() {
  const [word, setWord] = useState("");
  const [emoji, setEmoji] = useState("");

  const searchEmoji = async () => {
    const res = await fetch(`https://emoji-backend.onrender.com/emoji?word=${word}`);
    const data = await res.json();
    setEmoji(data.emoji || "❓");
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Emoji Dictionary 📖</h1>
      <input
        type="text"
        value={word}
        onChange={(e) => setWord(e.target.value)}
        placeholder="Enter a word"
      />
      <button onClick={searchEmoji}>Search</button>
      <h2 style={{ fontSize: "4rem" }}>{emoji}</h2>
    </div>
  );
}

export default App;

