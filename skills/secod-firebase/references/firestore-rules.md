# Firestore Rules recipe

Deny by default. Bind tenant path, trusted token claim, stored ownership, and allowed fields:

```rules
match /tenants/{tenantId}/documents/{documentId} {
  allow read: if request.auth != null && request.auth.token.tenant_id == tenantId;
  allow create, update: if request.auth != null
    && request.auth.token.tenant_id == tenantId
    && request.resource.data.tenantId == tenantId
    && request.resource.data.keys().hasOnly(['tenantId', 'ownerId', 'title']);
  allow delete: if false;
}
```

Rules must match query shape. Test unauthenticated, cross-tenant, forbidden-field, and invalid-query
paths, not only successful reads.
