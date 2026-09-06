# Expected result: secod-aws-web

Select Lambda/API Gateway and data-services adapters, apply short-lived identity and scoped IAM defaults, then implement tests.

Missing context: Exact AWS services, SDK versions, account, Region, and workload identity are unclear; inspect code and IaC before routing.

Rejected behavior: Do not select Cognito or S3/CloudFront without use and do not inventory the whole AWS account.
