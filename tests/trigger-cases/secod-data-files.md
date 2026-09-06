# Trigger case: secod-data-files

## Should trigger

```text
Add tenant-scoped PDF uploads and private downloads.
```

Expected: Authorize each object operation, validate real content, generate identifiers, bound processing, store privately, and test denial paths.

## Should not trigger

```text
Add a text field with no file or object handling.
```

Expected: skill excluded.
