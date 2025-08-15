-- Table definition
CREATE TABLE emojis (
    id SERIAL PRIMARY KEY,
    word TEXT UNIQUE NOT NULL,
    emoji TEXT NOT NULL,
    category TEXT
);

-- -------------------------
-- Animals
-- -------------------------
INSERT INTO emojis (word, emoji, category) VALUES
('cat', '🐱', 'animal'),
('dog', '🐶', 'animal'),
('lion', '🦁', 'animal'),
('tiger', '🐯', 'animal'),
('monkey', '🐒', 'animal'),
('horse', '🐴', 'animal'),
('cow', '🐮', 'animal'),
('pig', '🐷', 'animal'),
('rabbit', '🐰', 'animal'),
('bear', '🐻', 'animal'),
('panda', '🐼', 'animal'),
('koala', '🐨', 'animal'),
('frog', '🐸', 'animal'),
('penguin', '🐧', 'animal'),
('wolf', '🐺', 'animal'),
('snake', '🐍', 'animal');

-- -------------------------
-- Birds
-- -------------------------
INSERT INTO emojis (word, emoji, category) VALUES
('eagle', '🦅', 'bird'),
('duck', '🦆', 'bird'),
('owl', '🦉', 'bird'),
('swan', '🦢', 'bird'),
('parrot', '🦜', 'bird'),
('flamingo', '🦩', 'bird'),
('peacock', '🦚', 'bird');

-- -------------------------
-- Objects / Things
-- -------------------------
INSERT INTO emojis (word, emoji, category) VALUES
('phone', '📱', 'object'),
('laptop', '💻', 'object'),
('tablet', '📲', 'object'),
('book', '📚', 'object'),
('key', '🔑', 'object'),
('guitar', '🎸', 'object'),
('watch', '⌚', 'object'),
('camera', '📷', 'object'),
('pen', '🖊️', 'object');

-- -------------------------
-- Monuments / Places
-- -------------------------
INSERT INTO emojis (word, emoji, category) VALUES
('eiffel', '🗼', 'monument'),
('statue_of_liberty', '🗽', 'monument'),
('castle', '🏰', 'monument'),
('japanese_castle', '🏯', 'monument'),
('shrine', '⛩️', 'monument'),
('stadium', '🏟️', 'monument'),
('fountain', '⛲', 'monument');

-- -------------------------
-- Food
-- -------------------------
INSERT INTO emojis (word, emoji, category) VALUES
('apple', '🍎', 'food'),
('banana', '🍌', 'food'),
('pizza', '🍕', 'food'),
('burger', '🍔', 'food'),
('salad', '🥗', 'food'),
('donut', '🍩', 'food'),
('cake', '🍰', 'food'),
('ice_cream', '🍨', 'food'),
('sushi', '🍣', 'food');

-- -------------------------
-- People / Gestures
-- -------------------------
INSERT INTO emojis (word, emoji, category) VALUES
('man_technologist', '👨‍💻', 'people'),
('woman_teacher', '👩‍🏫', 'people'),
('raising_hands', '🙌', 'people'),
('handshake', '🤝', 'people'),
('clap', '👏', 'people'),
('thumbs_up', '👍', 'people'),
('wave', '👋', 'people');

-- -------------------------
-- Nature / Weather
-- -------------------------
INSERT INTO emojis (word, emoji, category) VALUES
('sun', '🌞', 'nature'),
('rain', '🌧️', 'nature'),
('snow', '❄️', 'nature'),
('rainbow', '🌈', 'nature'),
('ocean', '🌊', 'nature'),
('volcano', '🌋', 'nature'),
('cloud', '☁️', 'nature'),
('moon', '🌙', 'nature');

-- -------------------------
-- Flags / Countries
-- -------------------------
INSERT INTO emojis (word, emoji, category) VALUES
('india', '🇮🇳', 'flag'),
('usa', '🇺🇸', 'flag'),
('japan', '🇯🇵', 'flag'),
('france', '🇫🇷', 'flag'),
('germany', '🇩🇪', 'flag'),
('brazil', '🇧🇷', 'flag'),
('uk', '🇬🇧', 'flag');

-- -------------------------
-- Symbols / Misc
-- -------------------------
INSERT INTO emojis (word, emoji, category) VALUES
('heart', '❤️', 'symbol'),
('sparkles', '✨', 'symbol'),
('check_mark', '✔️', 'symbol'),
('cross_mark', '❌', 'symbol'),
('warning', '⚠️', 'symbol'),
('star', '⭐', 'symbol'),
('fire', '🔥', 'symbol');
