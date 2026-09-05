"""Populate provisional official-source registers without claiming content review."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
REVIEWED_DATE = "2026-09-05"
REFRESH = "2027-03-05 or documentation/service behavior change"


SOURCES: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "secod-auth0": ("Auth0", [
        ("Access token validation", "https://auth0.com/docs/secure/tokens/access-tokens/validate-access-tokens"),
        ("Refresh token rotation", "https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation"),
        ("Application settings and callback allowlists", "https://auth0.com/docs/get-started/applications/application-settings"),
    ]),
    "secod-better-auth": ("Better Auth", [
        ("Security reference", "https://better-auth.com/docs/reference/security"),
        ("Session management", "https://better-auth.com/docs/concepts/session-management"),
        ("Rate limiting", "https://better-auth.com/docs/concepts/rate-limit"),
    ]),
    "secod-clerk": ("Clerk", [
        ("Manual JWT verification", "https://clerk.com/docs/guides/sessions/manual-jwt-verification"),
        ("Session security options", "https://clerk.com/docs/guides/secure/session-options"),
        ("Account linking", "https://clerk.com/docs/guides/configure/auth-strategies/social-connections/account-linking"),
    ]),
    "secod-supabase-auth": ("Supabase", [
        ("JWT signing keys", "https://supabase.com/docs/guides/auth/signing-keys"),
        ("Auth sessions", "https://supabase.com/docs/guides/auth/sessions"),
        ("Multi-factor authentication", "https://supabase.com/docs/guides/auth/auth-mfa"),
    ]),
    "secod-workos": ("WorkOS", [
        ("AuthKit sessions", "https://workos.com/docs/authkit/sessions"),
        ("Session token JWKS", "https://workos.com/docs/reference/authkit/session-tokens/jwks"),
        ("Webhook verification", "https://workos.com/docs/webhooks"),
    ]),
    "secod-aws-web": ("Amazon Web Services", [
        ("IAM security best practices", "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html"),
        ("CloudTrail security best practices", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/best-practices-security.html"),
        ("AWS KMS best practices", "https://docs.aws.amazon.com/kms/latest/developerguide/best-practices.html"),
    ]),
    "secod-aws-cognito": ("Amazon Web Services", [
        ("Cognito user-pool security best practices", "https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html"),
        ("Cognito JWT verification", "https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html"),
    ]),
    "secod-aws-lambda-api-gateway": ("Amazon Web Services", [
        ("Lambda permissions", "https://docs.aws.amazon.com/lambda/latest/dg/lambda-permissions.html"),
        ("Lambda Function URL access control", "https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html"),
        ("API Gateway access control", "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-to-api.html"),
    ]),
    "secod-aws-s3-cloudfront": ("Amazon Web Services", [
        ("Amazon S3 security best practices", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html"),
        ("CloudFront Origin Access Control for S3", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html"),
    ]),
    "secod-aws-data-services": ("Amazon Web Services", [
        ("Amazon RDS advanced security", "https://docs.aws.amazon.com/AmazonRDS/latest/gettingstartedguide/advanced-security.html"),
        ("DynamoDB preventative security", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices-security-preventative.html"),
        ("OpenSearch Service security", "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/security.html"),
    ]),
    "secod-cloudflare": ("Cloudflare", [
        ("Cloudflare API token permissions", "https://developers.cloudflare.com/fundamentals/api/get-started/create-token/"),
        ("Cloudflare Access JWT validation", "https://developers.cloudflare.com/cloudflare-one/identity/authorization-cookie/validating-json/"),
        ("Cloudflare developer documentation index", "https://developers.cloudflare.com/llms.txt"),
    ]),
    "secod-cloudflare-workers": ("Cloudflare", [
        ("Wrangler configuration", "https://developers.cloudflare.com/workers/wrangler/configuration/"),
        ("Workers compatibility dates", "https://developers.cloudflare.com/workers/configuration/compatibility-dates/"),
        ("Workers security model", "https://developers.cloudflare.com/workers/reference/security-model/"),
    ]),
    "secod-cloudflare-pages": ("Cloudflare", [
        ("Pages preview deployments", "https://developers.cloudflare.com/pages/configuration/preview-deployments/"),
        ("Pages branch build controls", "https://developers.cloudflare.com/pages/configuration/branch-build-controls/"),
        ("Pages Functions bindings", "https://developers.cloudflare.com/pages/functions/bindings/"),
    ]),
    "secod-cloudflare-queues": ("Cloudflare", [
        ("Queues batching and retries", "https://developers.cloudflare.com/queues/configuration/batching-retries/"),
        ("Queues dead-letter queues", "https://developers.cloudflare.com/queues/configuration/dead-letter-queues/"),
    ]),
    "secod-cloudflare-workflows": ("Cloudflare", [
        ("Rules of Workflows", "https://developers.cloudflare.com/workflows/build/rules-of-workflows/"),
        ("Workflow events and parameters", "https://developers.cloudflare.com/workflows/build/events-and-parameters/"),
        ("Workflow sleeping and retrying", "https://developers.cloudflare.com/workflows/build/sleeping-and-retrying/"),
    ]),
    "secod-cloudflare-hyperdrive": ("Cloudflare", [
        ("Hyperdrive TLS and mTLS", "https://developers.cloudflare.com/hyperdrive/configuration/tls-ssl-certificates-for-hyperdrive/"),
        ("Private database connectivity", "https://developers.cloudflare.com/hyperdrive/configuration/connect-to-private-database/"),
        ("Hyperdrive connection lifecycle", "https://developers.cloudflare.com/hyperdrive/concepts/connection-lifecycle/"),
    ]),
    "secod-cloudflare-vectorize": ("Cloudflare", [
        ("Vectorize metadata filtering", "https://developers.cloudflare.com/vectorize/reference/metadata-filtering/"),
        ("Vectorize client API", "https://developers.cloudflare.com/vectorize/reference/client-api/"),
    ]),
    "secod-cloudflare-workers-ai": ("Cloudflare", [
        ("Workers AI bindings", "https://developers.cloudflare.com/workers-ai/configuration/bindings/"),
        ("Workers AI limits", "https://developers.cloudflare.com/workers-ai/platform/limits/"),
    ]),
    "secod-cloudflare-ai-gateway": ("Cloudflare", [
        ("AI Gateway authentication", "https://developers.cloudflare.com/ai-gateway/configuration/authentication/"),
        ("AI Gateway logging", "https://developers.cloudflare.com/ai-gateway/observability/logging/"),
        ("AI Gateway caching", "https://developers.cloudflare.com/ai-gateway/features/caching/"),
    ]),
    "secod-firebase": ("Google Firebase", [
        ("Firebase security checklist", "https://firebase.google.com/support/guides/security-checklist"),
        ("Firebase Security Rules", "https://firebase.google.com/docs/rules"),
        ("Firebase App Check enforcement", "https://firebase.google.com/docs/app-check/enable-enforcement"),
    ]),
    "secod-google-cloud-web": ("Google Cloud", [
        ("Using IAM securely", "https://cloud.google.com/iam/docs/using-iam-securely"),
        ("Service account best practices", "https://cloud.google.com/iam/docs/best-practices-service-accounts"),
        ("Secret Manager access control", "https://cloud.google.com/secret-manager/docs/access-control"),
    ]),
    "secod-google-cloud-storage": ("Google Cloud", [
        ("Cloud Storage access-control best practices", "https://cloud.google.com/storage/docs/access-control/best-practices-access-control"),
        ("Cloud Storage signed URLs", "https://cloud.google.com/storage/docs/access-control/signed-urls"),
        ("Public access prevention", "https://cloud.google.com/storage/docs/public-access-prevention"),
    ]),
    "secod-supabase": ("Supabase", [
        ("Secure configuration of Supabase products", "https://supabase.com/docs/guides/security/product-security"),
        ("Supabase production checklist", "https://supabase.com/docs/guides/deployment/going-into-prod"),
        ("Row Level Security", "https://supabase.com/docs/guides/database/postgres/row-level-security"),
    ]),
    "secod-neon": ("Neon", [
        ("Neon security overview", "https://neon.com/docs/security/security-overview"),
        ("Protected branches", "https://neon.com/docs/guides/protected-branches"),
        ("Data API access control", "https://neon.com/docs/data-api/access-control"),
    ]),
    "secod-convex": ("Convex", [
        ("Convex best practices", "https://docs.convex.dev/understanding/best-practices"),
        ("Function authentication", "https://docs.convex.dev/auth/functions-auth"),
        ("Internal functions", "https://docs.convex.dev/functions/internal-functions"),
    ]),
    "secod-nextjs": ("Vercel", [
        ("Next.js Data Security", "https://nextjs.org/docs/app/guides/data-security"),
        ("Next.js Server Actions", "https://nextjs.org/docs/app/guides/server-actions"),
        ("Next.js image configuration", "https://nextjs.org/docs/app/api-reference/components/image"),
    ]),
    "secod-vercel-platform": ("Vercel", [
        ("Vercel Deployment Protection", "https://vercel.com/docs/deployment-protection"),
        ("Vercel environment variables", "https://vercel.com/docs/environment-variables"),
        ("Vercel OIDC", "https://vercel.com/docs/oidc"),
    ]),
    "secod-stripe": ("Stripe", [
        ("API keys", "https://docs.stripe.com/keys"),
        ("Webhook verification and delivery", "https://docs.stripe.com/webhooks"),
        ("Idempotent API requests", "https://docs.stripe.com/api/idempotent_requests"),
    ]),
    "secod-polar": ("Polar", [
        ("API authentication", "https://polar.sh/docs/integrate/authentication"),
        ("Webhook integration", "https://polar.sh/docs/integrate/webhooks"),
    ]),
    "secod-lemonsqueezy": ("Lemon Squeezy", [
        ("API authentication", "https://docs.lemonsqueezy.com/api/getting-started/requests"),
        ("Signing webhook requests", "https://docs.lemonsqueezy.com/guides/developer-guide/webhooks"),
    ]),
    "secod-dodo-payments": ("Dodo Payments", [
        ("API authentication", "https://docs.dodopayments.com/api-reference/introduction"),
        ("Webhook security", "https://docs.dodopayments.com/developer-resources/webhooks"),
    ]),
    "secod-whop": ("Whop", [
        ("API authentication", "https://dev.whop.com/api-reference/authentication"),
        ("Webhook overview", "https://dev.whop.com/api-reference/v5/webhooks/overview"),
    ]),
    "secod-openai": ("OpenAI", [
        ("Project service-account API keys", "https://developers.openai.com/api/reference/cli/resources/admin/subresources/organization/subresources/projects/subresources/service_accounts/subresources/api_keys/methods/create"),
        ("Webhook verification", "https://platform.openai.com/docs/guides/webhooks"),
        ("Data controls", "https://platform.openai.com/docs/guides/your-data"),
    ]),
    "secod-anthropic": ("Anthropic", [
        ("API overview and versioning", "https://docs.anthropic.com/en/api/overview"),
        ("Rate limits", "https://docs.anthropic.com/en/api/rate-limits"),
        ("Data usage", "https://docs.anthropic.com/en/docs/claude-code/data-usage"),
    ]),
    "secod-google-genai": ("Google", [
        ("Gemini API key guidance", "https://ai.google.dev/gemini-api/docs/api-key"),
        ("Live API ephemeral tokens", "https://ai.google.dev/gemini-api/docs/ephemeral-tokens"),
        ("Gemini API file prompting", "https://ai.google.dev/gemini-api/docs/files"),
    ]),
    "secod-xai-grok": ("xAI", [
        ("API key and ACL management", "https://docs.x.ai/developers/management-api-guide"),
        ("Consumption and rate limits", "https://docs.x.ai/developers/rate-limits"),
        ("Data retention and privacy", "https://docs.x.ai/developers/faq/security"),
    ]),
    "secod-vercel-ai": ("Vercel", [
        ("AI Gateway authentication", "https://vercel.com/docs/ai-gateway/authentication"),
        ("AI Gateway provider options", "https://vercel.com/docs/ai-gateway/provider-options"),
        ("AI SDK telemetry", "https://ai-sdk.dev/docs/ai-sdk-core/telemetry"),
    ]),
}

ASSUMPTION_COLUMN_SKILLS = {
    "secod-core",
    "secod-crypto-data-protection",
    "secod-data-files",
    "secod-identity-access",
    "secod-inputs-apis",
    "secod-threat-model",
    "secod-web-app-security",
}


def render(slug: str, owner: str, rows: list[tuple[str, str]]) -> str:
    control = "PROVISIONAL-" + slug.removeprefix("secod-") + "-ALL"
    table_rows = []
    for index, (title, url) in enumerate(rows, 1):
        source_id = slug.removeprefix("secod-").upper().replace("-", "-") + f"-SRC-{index:02d}"
        table_rows.append(
            f"| {source_id} | {title} | {url} | {owner} | {REVIEWED_DATE} (identification only) | {REFRESH} | "
            f"Pending review | {control} | Current hosted service; exact plan, region, API/SDK version, "
            "enabled features, and deployed configuration must be verified per project. |"
        )
    return f"""# Source register: {slug}

Use official documentation indexes for discovery only. These direct official sources were
identified on {REVIEWED_DATE}, but their control mapping still requires substantive review.
Until that review is complete, affected provider requirements remain **Not verified**.

| Source ID | Title | Direct official URL | Owner | Reviewed date | Refresh trigger | Status | Control IDs | Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
{"\n".join(table_rows)}

Status meanings: `Reviewed` means content was read and mapped to controls; `Pending review` means
the official URL is identified but mapping is incomplete; `Not verified` means evidence is
inaccessible, stale, or insufficient. URL reachability alone never establishes `Reviewed`.
"""


def add_assumption_column(content: str) -> str:
    lines = content.splitlines()
    in_source_table = False
    changed = False
    for index, line in enumerate(lines):
        if line.startswith("| Source ID |") and "Assumptions" not in line:
            lines[index] = line.rstrip().rstrip("|").rstrip() + " | Assumptions |"
            in_source_table = True
            changed = True
            continue
        if in_source_table and line.startswith("|"):
            value = "---" if re.fullmatch(r"\|[\s|:-]+\|", line) else "See register assumptions below."
            lines[index] = line.rstrip().rstrip("|").rstrip() + f" | {value} |"
            continue
        if in_source_table:
            break
    return "\n".join(lines) + ("\n" if content.endswith("\n") else "") if changed else content


def main() -> None:
    changed = 0
    for slug, (owner, rows) in SOURCES.items():
        target = ROOT / "skills" / slug / "references" / "sources.md"
        current = target.read_text(encoding="utf-8")
        if "Add the control-specific primary sources" in current:
            target.write_text(render(slug, owner, rows), encoding="utf-8")
            changed += 1
        elif f"| {REVIEWED_DATE} | {REFRESH} | Pending review |" in current:
            updated = current.replace(
                f"| {REVIEWED_DATE} | {REFRESH} | Pending review |",
                f"| {REVIEWED_DATE} (identification only) | {REFRESH} | Pending review |",
            )
            target.write_text(updated, encoding="utf-8")
            changed += 1
    for slug in ASSUMPTION_COLUMN_SKILLS:
        target = ROOT / "skills" / slug / "references" / "sources.md"
        current = target.read_text(encoding="utf-8")
        normalized = add_assumption_column(current)
        if normalized != current:
            target.write_text(normalized, encoding="utf-8")
            changed += 1
    print(f"Populated {changed} provisional source registers.")


if __name__ == "__main__":
    main()
