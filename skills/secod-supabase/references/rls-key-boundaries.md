# Supabase RLS and key-boundary recipe

Keep grants and policies in migration. Example tenant-owned table:

```sql
alter table public.projects enable row level security;
revoke all on public.projects from anon;
grant select, insert, update on public.projects to authenticated;

create policy "tenant members read projects"
on public.projects for select to authenticated
using (tenant_id = (auth.jwt() ->> 'tenant_id')::uuid);

create policy "tenant members create projects"
on public.projects for insert to authenticated
with check (
  tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
  and owner_id = auth.uid()
);
```

Validate claim design for project before using it; stale mutable authorization data may require a
membership-table policy instead. Browser/mobile uses publishable key. Secret or `service_role` key
bypasses RLS and belongs only in trusted backend after application authorization. Apply equivalent
RLS to `storage.objects`, constraining bucket, path, owner, operation, and listing behavior.

Tests: anonymous denial, member success, cross-tenant denial, forged body tenant, forbidden update,
view/function bypass, Storage list/read/write/delete. Use Supabase local/database test tooling supported
by project version.
