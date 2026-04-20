create table bot_logs (
  id uuid default gen_random_uuid() primary key,
  bot_id text,
  target_url text,
  status text,
  created_at timestamp with time zone default now()
);
