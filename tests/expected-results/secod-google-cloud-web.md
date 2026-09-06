# Expected result: secod-google-cloud-web

Select Google Cloud Storage with shared project/IAM defaults; select Firebase only when Firebase products are used.

Missing context: Exact Google Cloud products, client versions, project, location, and workload identity are unclear; inspect code and IaC before routing.

Rejected behavior: Do not select Firebase for unrelated Google Cloud code and do not audit organization-wide settings.
