# Trigger case: secod-google-cloud-web

## Should trigger

```text
Add private Cloud Storage uploads to a Google Cloud application.
```

Expected: Select Google Cloud Storage with shared project/IAM defaults; select Firebase only when Firebase products are used.

## Should not trigger

```text
Add Firebase Auth only; no general Google Cloud service adapter is required beyond Firebase routing.
```

Expected: family router excluded unless stated provider-family routing is required.
