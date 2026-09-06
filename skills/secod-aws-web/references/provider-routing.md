# AWS Web product routing

## Selection rule

Require current-feature evidence: import or SDK call, provider configuration/IaC, runtime binding, route, or explicit user request. Package presence alone is Possible. Route only Confirmed products.

## Adapter map

- Lambda or API Gateway selects secod-aws-lambda-api-gateway.
- Cognito selects secod-aws-cognito.
- S3 or CloudFront selects secod-aws-s3-cloudfront.
- RDS, Aurora, DynamoDB, ElastiCache, or OpenSearch selects secod-aws-data-services.

## Shared context

Pass exact product, resolved SDK/tool version, environment, resource/project/account identifiers without secrets, identity model, data classes, trust boundaries, likely files, tests, routing reason, and narrow assumptions.

## Shared defaults

- Use short-lived workload roles and federation instead of static access keys.
- Give each workload minimal identity and resource policies scoped to required account, Region, service, and resource.
- Keep secrets in trusted server/runtime paths and separate environments/accounts.
- Make public exposure and cross-account trust explicit and condition-bound.

## Exclusions

Do not select sibling adapters without product evidence. Do not inspect unrelated account settings. Do not guess plan, Region, deployment state, or APIs.
