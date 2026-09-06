---
name: secod-aws-web
description: >-
  Route AWS coding tasks to exact service adapters and apply shared workload-identity, IAM, account, Region, secret, encryption, and environment defaults.
license: Apache-2.0
metadata:
  secod-category: "provider-family"
  secod-format: "implementation-v1"
  secod-maturity: "provisional"
---

# AWS Web implementation router

## Purpose

Identify exact provider products used by current feature, apply only shared provider defaults, and route exact SDK work to applicable feature adapters. Do not perform account-wide audit.

## When to use

Use for AWS SDKs, ARNs, IAM, STS, Lambda, API Gateway, Cognito, S3, CloudFront, RDS, DynamoDB, ElastiCache, OpenSearch, or AWS IaC. Package presence alone is possible context, not sufficient activation when current feature does not use provider.

## Context to inspect

Inspect current request, imports and SDK calls, manifest and lockfile versions, provider configuration names, IaC, runtime/deployment target, environment, trust boundaries, and tests. Never collect secret values.

## Secure defaults

- Use short-lived workload roles and federation instead of static access keys.
- Give each workload minimal identity and resource policies scoped to required account, Region, service, and resource.
- Keep secrets in trusted server/runtime paths and separate environments/accounts.
- Make public exposure and cross-account trust explicit and condition-bound.

## Implementation workflow

1. Identify exact provider products used by current feature from code and configuration evidence.
2. Classify each product as Confirmed, Possible, or Absent; route only Confirmed products.
3. Add applicable generalized skills and compute transitive dependency closure through secod-core.
4. Pass product, resolved version, environment, identity, data, boundaries, files, and assumptions to adapters.
5. Let adapters own exact SDK calls and product tests; retain shared defaults across adapters.

## Implementation recipes

- [Provider routing](references/provider-routing.md) — product signals, adapter map, exclusions, and shared context.

## Unsafe patterns to avoid

- Loading every adapter because provider package or account exists.
- Replacing feature implementation with account-wide settings inventory or findings report.
- Inventing SDK calls, product availability, plan behavior, or dashboard state.
- Treating provider authentication, edge controls, or IAM as application authorization.

## Tests to add

Test correct product activation, similar non-trigger, multiple applicable products, transitive dependencies, unused-provider exclusion, missing-version handling, secure generated boundary, and no account-audit output.

## Provider and deployment steps

- Lambda or API Gateway selects secod-aws-lambda-api-gateway.
- Cognito selects secod-aws-cognito.
- S3 or CloudFront selects secod-aws-s3-cloudfront.
- RDS, Aurora, DynamoDB, ElastiCache, or OpenSearch selects secod-aws-data-services.

If required console setting is inaccessible, provide exact official verification path without claiming it was checked.

## Official sources

Use [source register](references/sources.md). llms.txt indexes support page discovery only; direct product pages govern implementation.

## Completion handoff

State detected products, selected and excluded adapters, shared defaults applied, code/tests changed, and precise external step remaining. Never issue account-wide verdict, scanner report, certification, or whole-application security claim.
