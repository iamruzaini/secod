# Official source register

| Source ID | Title | Source type | Direct official URL | Owner | Reviewed date | Refresh trigger | Status | Recipes or decisions supported | Assumptions/notes |
|---|---|---|---|---|---|---|---|---|---|
| SUPABASE-SRC-001 | Row Level Security | Direct implementation guide | https://supabase.com/docs/guides/database/postgres/row-level-security | Supabase | 2026-09-06 | RLS guide or platform change | Reviewed | rls-key-boundaries.md: grants, policies, views, and testing | Validate claim design per project. |
| SUPABASE-SRC-002 | API keys | Direct security guide | https://supabase.com/docs/guides/api/api-keys | Supabase | 2026-09-06 | Key model change | Reviewed | rls-key-boundaries.md: publishable versus secret/service-role boundary | Legacy keys may require migration. |
| SUPABASE-SRC-003 | Storage access control | Direct implementation guide | https://supabase.com/docs/guides/storage/security/access-control | Supabase | 2026-09-06 | Storage policy change | Reviewed | rls-key-boundaries.md: storage.objects policy design | Operation-specific grants differ. |
| SUPABASE-SRC-004 | Supabase documentation index | Official llms.txt | https://supabase.com/llms.txt | Supabase | 2026-09-06 | Index change | Reviewed | rls-key-boundaries.md: current direct-page discovery | Index is not sole support for code. |
