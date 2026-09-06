# Trigger case: secod-aws-web

## Should trigger

```text
Add an AWS Lambda API backed by DynamoDB.
```

Expected: Select Lambda/API Gateway and data-services adapters, apply short-lived identity and scoped IAM defaults, then implement tests.

## Should not trigger

```text
Add a Google Cloud Run service with no AWS signals.
```

Expected: family router excluded unless stated provider-family routing is required.
