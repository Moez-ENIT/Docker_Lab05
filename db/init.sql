CREATE TABLE IF NOT EXISTS visits (
  id serial primary key,
  ts timestamptz default now()
);