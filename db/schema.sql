 CREATE TABLE emojis (
    id SERIAL PRIMARY KEY,
    word TEXT UNIQUE NOT NULL,
    emoji TEXT NOT NULL,
    category TEXT
);

INSERT INTO emojis (word, emoji, category) VALUES
('cat', '🐱', 'animal'),
('dog', '🐶', 'animal'),
('book', '📚', 'object'),
('india', '🇮🇳', 'flag'),
('sun', '☀️', 'nature');

