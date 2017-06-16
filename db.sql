CREATE TABLE feedback (
id integer PRIMARY KEY,
created_at text,
updated_at text,
content text NOT NULL,
status integer DEFAULT 1,
type integer NOT NULL,
total_used integer DEFAULT 0
)
