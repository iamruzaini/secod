# Implementation fixture plan: secod-aws-lambda-api-gateway

Start from an intentionally unsafe AWS Lambda and API Gateway boundary. Replace client-trusted authority and unbounded provider calls with version-matched secure implementation from references/runtime-deployment.md.

Test success, unauthorized/cross-tenant access, malformed input, replay/retry where applicable, provider failure, and secret redaction. This plan is not a scanner execution.
