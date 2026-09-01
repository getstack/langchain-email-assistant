-- Run this in Supabase SQL Editor (Dashboard -> SQL -> New query)

-- Profiles (one row per authenticated user)
create table if not exists public.profiles (
    id uuid primary key references auth.users (id) on delete cascade,
    display_name text not null,
    default_tone text not null default 'Professional',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

create policy "Users can read own profile"
    on public.profiles for select
    using (auth.uid() = id);

create policy "Users can insert own profile"
    on public.profiles for insert
    with check (auth.uid() = id);

create policy "Users can update own profile"
    on public.profiles for update
    using (auth.uid() = id);

-- Generation history
create table if not exists public.history (
    id bigint primary key generated always as identity,
    user_id uuid not null references auth.users (id) on delete cascade,
    feature text not null,
    title text not null,
    input_text text,
    output_text text,
    tone text,
    length text,
    created_at timestamptz not null default now()
);

alter table public.history enable row level security;

create policy "Users can read own history"
    on public.history for select
    using (auth.uid() = user_id);

create policy "Users can insert own history"
    on public.history for insert
    with check (auth.uid() = user_id);

-- Usage / token tracking
create table if not exists public.usage_events (
    id bigint primary key generated always as identity,
    user_id uuid references auth.users (id) on delete cascade,
    feature text not null,
    model text,
    input_tokens integer not null default 0,
    output_tokens integer not null default 0,
    total_tokens integer not null default 0,
    latency_ms integer not null default 0,
    status text not null,
    created_at timestamptz not null default now()
);

alter table public.usage_events enable row level security;

create policy "Users can read own usage"
    on public.usage_events for select
    using (auth.uid() = user_id);

create policy "Users can insert own usage"
    on public.usage_events for insert
    with check (auth.uid() = user_id);
