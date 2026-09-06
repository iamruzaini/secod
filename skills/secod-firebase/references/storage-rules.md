# Firebase Storage Rules recipe

Bind tenant and user into object path; restrict size and accepted content types:

```rules
match /tenants/{tenantId}/uploads/{userId}/{fileName} {
  allow read: if request.auth != null && request.auth.token.tenant_id == tenantId;
  allow write: if request.auth != null && request.auth.uid == userId
    && request.auth.token.tenant_id == tenantId
    && request.resource.size < 10 * 1024 * 1024
    && request.resource.contentType.matches('image/(png|jpeg)');
}
```

Treat metadata as untrusted. Validate file signatures and process uploads in bounded isolated
workers when content reaches a backend.
