import { useState } from "react";

function App() {
  const [word, setWord] = useState("");
  const [emoji, setEmoji] = useState("");
  const [error, setError] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [highlightIndex, setHighlightIndex] = useState(-1);

  // Fetch suggestions dynamically
  useEffect(() => {
    if (word.trim().length === 0) {
      setSuggestions([]);
      return;
    }

    const fetchSuggestions = async () => {
      try {
        const res = await fetch(
          `https://emoji-dictionary.onrender.com/search?query=${word}`
        );
        const data = await res.json();
        setSuggestions(data.results || []);
      } catch {
        setSuggestions([]);
      }
    };

    fetchSuggestions();
  }, [word]);
  
  const searchEmoji = async (searchWord = word) => {
    if (!searchWord.trim()) {
      setError("Please enter a word");
      setEmoji("");
      return;
    }

    try {
      // const res = await fetch(`https://emoji-backend.onrender.com/emoji?word=${word}`);      
      const res = await fetch(
        `https://emoji-dictionary.onrender.com/emoji?word=${searchWord}`
      );
      if (!res.ok) throw new Error("Emoji not found");
      const data = await res.json();
      setEmoji(data.emoji || "❓");
      setError("");
      setSuggestions([]);
    } catch (err) {
      setEmoji("❓");
      setError(err.message);
    }
  };

  // Handle keyboard navigation
  const handleKeyDown = (e) => {
    if (e.key === "ArrowDown") {
      setHighlightIndex((prev) => (prev + 1) % suggestions.length);
    } else if (e.key === "ArrowUp") {
      setHighlightIndex((prev) =>
        prev <= 0 ? suggestions.length - 1 : prev - 1
      );
    } else if (e.key === "Enter") {
      if (highlightIndex >= 0 && suggestions[highlightIndex]) {
        const selected = suggestions[highlightIndex];
        setWord(selected.word);
        searchEmoji(selected.word);
      } else {
        searchEmoji();
      }
    }
  };
  
  return (
    <div
      style={{
        textAlign: "center",
        marginTop: "50px",
        fontFamily: "sans-serif",
      }}
    >
      <h1>Emoji Dictionary 📖</h1>

      <input
        type="text"
        value={word}
        onChange={(e) => setWord(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Enter a word"
        style={{ padding: "10px", fontSize: "1rem", marginRight: "10px" }}
      />
      <button
        onClick={() => searchEmoji()}
        style={{ padding: "10px 15px", fontSize: "1rem", cursor: "pointer" }}
      >
        Search
      </button>

      {/* Suggestions Dropdown */}
      {suggestions.length > 0 && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))",
            gap: "10px",
            marginTop: "20px",
            maxWidth: "600px",
            marginLeft: "auto",
            marginRight: "auto",
          }}
        >
          {suggestions.map((s, idx) => (
            <div
              key={idx}
              onClick={() => {
                setWord(s.word);
                searchEmoji(s.word);
              }}
              style={{
                border:
                  idx === highlightIndex ? "2px solid blue" : "1px solid #ddd",
                borderRadius: "8px",
                padding: "10px",
                cursor: "pointer",
                background: idx === highlightIndex ? "#f0f8ff" : "white",
              }}
            >
              <span style={{ fontSize: "2rem" }}>{s.emoji}</span>
              <p style={{ margin: "5px 0 0", fontSize: "0.9rem" }}>{s.word}</p>
              {s.category && (
                <p style={{ margin: 0, fontSize: "0.75rem", color: "gray" }}>
                  {s.category}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}

      {emoji && (
        <h2 style={{ fontSize: "4rem", marginTop: "20px" }}>{emoji}</h2>
      )}
    </div>
  );
}

export default App;
