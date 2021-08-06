CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  message TEXT NOT NULL
);

INSERT INTO comments (message) VALUES ('first blood!', 'hello', 'whut');
