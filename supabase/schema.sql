-- Run this in Supabase SQL Editor (Dashboard -> SQL -> New query)

-- Profile row per authenticated user (auth.users managed by Supabase Auth)
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

-- Optional: auto-create profile on signup (advanced — can add later)
-- For now the app upserts profile after sign-up/sign-in.
