# Expected result: secod-web-app-security

Use safe rendering, server authorization, appropriate CSRF protection, narrow origins, and browser-boundary tests.

Missing context: Rendering context or cookie/origin model is unclear; inspect framework and deployment before choosing controls.

Rejected behavior: Never trust CORS, hidden UI, or browser headers as authorization.
