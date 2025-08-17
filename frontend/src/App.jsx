import { useState, useEffect } from "react";

function App() {
  const [word, setWord] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  // Fetch suggestions as user types
  useEffect(() => {
    const fetchSuggestions = async () => {
      if (word.trim().length < 2) {
        setSuggestions([]);
        return;
      }
      try {
        const res = await fetch(
          `https://emoji-dictionary.onrender.com/search?query=${word}`
        );
        if (!res.ok) return;
        const data = await res.json();
        setSuggestions(data.results || []);
      } catch (err) {
        console.error("Suggestion error:", err);
      }
    };

    fetchSuggestions();
  }, [word]);

  const searchEmoji = async (searchWord = word) => {
    if (!searchWord.trim()) {
      setError("Please enter a word or category");
      setResults([]);
      return;
    }

    try {
      const res = await fetch(
        `https://emoji-dictionary.onrender.com/emoji?word=${searchWord}`
      );
      if (!res.ok) throw new Error("Emoji not found");
      const data = await res.json();

      if (data.results && data.results.length > 0) {
        setResults(data.results);
        setError("");
      } else {
        setResults([]);
        setError("No emojis found");
      }
    } catch (err) {
      setResults([]);
      setError(err.message);
    }
  };

  // Handle Enter key
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      searchEmoji();
    }
  };

  return (
    <div
      style={{
        textAlign: "center",
        marginTop: "50px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>Emoji Dictionary 📖</h1>

      <div style={{ position: "relative", display: "inline-block" }}>
        <input
          type="text"
          value={word}
          onChange={(e) => setWord(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a word or category (e.g. cat, place, food)"
          style={{
            padding: "10px",
            fontSize: "1rem",
            width: "250px",
            borderRadius: "8px",
            border: "1px solid #ccc",
          }}
        />
        <button
          onClick={() => searchEmoji()}
          style={{
            padding: "10px 15px",
            fontSize: "1rem",
            marginLeft: "10px",
            cursor: "pointer",
            borderRadius: "8px",
            border: "none",
            backgroundColor: "#4CAF50",
            color: "white",
          }}
        >
          Search
        </button>

        {/* Suggestions dropdown */}
        {suggestions.length > 0 && (
          <ul
            style={{
              position: "absolute",
              top: "45px",
              left: 0,
              right: 0,
              background: "white",
              border: "1px solid #ccc",
              borderRadius: "8px",
              maxHeight: "200px",
              overflowY: "auto",
              listStyle: "none",
              padding: 0,
              margin: 0,
              zIndex: 1000,
            }}
          >
            {suggestions.map((item, idx) => (
              <li
                key={idx}
                onClick={() => {
                  setWord(item.word);
                  searchEmoji(item.word);
                  setSuggestions([]);
                }}
                style={{
                  padding: "10px",
                  cursor: "pointer",
                  display: "flex",
                  justifyContent: "space-between",
                }}
                onMouseOver={(e) =>
                  (e.currentTarget.style.background = "#f0f0f0")
                }
                onMouseOut={(e) =>
                  (e.currentTarget.style.background = "white")
                }
              >
                <span>{item.word}</span>
                <span style={{ fontSize: "1.5rem" }}>{item.emoji}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}

      {/* Results */}
      {results.length > 0 && (
        <div
          style={{
            marginTop: "20px",
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: "15px",
          }}
        >
          {results.map((item, idx) => (
            <div
              key={idx}
              style={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                padding: "10px",
                minWidth: "80px",
                textAlign: "center",
                boxShadow: "2px 2px 6px rgba(0,0,0,0.1)",
              }}
            >
              <div style={{ fontSize: "2rem" }}>{item.emoji}</div>
              <div style={{ marginTop: "5px", fontSize: "0.9rem" }}>
                {item.word}
              </div>
              <div
                style={{
                  marginTop: "3px",
                  fontSize: "0.75rem",
                  color: "#555",
                }}
              >
                {item.category}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
