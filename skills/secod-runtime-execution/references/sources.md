# Source register: secod-runtime-execution

Official documentation indexes are used for discovery only. Security-critical conclusions are
verified against the direct primary sources below. Refresh each entry before its review-expiry
date; mark `Stale`, `Changed`, or `Unavailable` when verification fails.

| ID | Title | Direct URL | Owner | Reviewed | Expiry / refresh trigger | Status | Controls | Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | OWASP OS Command Injection Defense Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html | OWASP Foundation | 2026-08-24 | Expires 2027-02-24 or on content change | Reviewed | -1, -2, -3, -4, -5 | Language-agnostic guidance; no plan/region dependency |
| S2 | OWASP Command Injection (attack description) | https://owasp.org/www-community/attacks/Command_Injection | OWASP Foundation | 2026-08-24 | Expires 2027-02-24 or on content change | Reviewed | -1, -2 | Threat-model context only |
| S3 | OWASP WSTG: Testing for Server-side Template Injection (v4.7.18 / latest) | https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server-side_Template_Injection | OWASP Foundation | 2026-08-24 | Expires 2027-02-24 or on content change | Reviewed | -7 | Testing methodology; engine versions vary |
| S4 | PortSwigger Web Security Academy: OS command injection prevention | https://portswigger.net/web-security/os-command-injection | PortSwigger Ltd | 2026-08-24 | Expires 2027-02-24 or on content change | Reviewed | -1, -2, -3, -4 | Educational reference; no plan/region dependency |
| S5 | Python `subprocess` module documentation (incl. Security Considerations) | https://docs.python.org/3/library/subprocess.html | Python Software Foundation | 2026-08-25 | Expires 2027-02-25 or on CPython doc change | Reviewed | -2, -5 | Python 3.x line; sequence args preferred; `shell=True` responsibility documented |
| S6 | Node.js `child_process` API documentation | https://nodejs.org/api/child_process.html | OpenJS Foundation | 2026-08-25 | Expires 2027-02-25 or on Node doc change | Reviewed | -2 | Active LTS/current docs; unsanitized-input warning verified verbatim |
| S7 | Jinja2 Sandboxed Environment documentation | https://jinja.palletsprojects.com/en/stable/sandbox/ | Pallets Projects | 2026-08-25 | Expires 2027-02-25 or on Jinja doc change | Reviewed | -7 | Jinja 3.x stable docs |
| S8 | Twig `sandbox` tag documentation | https://twig.symfony.com/doc/3.x/tags/sandbox.html | Symfony SAS | 2026-08-25 | Expires 2027-02-25 or on Twig doc change | Reviewed | -7 | Twig 3.x docs; explicit tags/filters/functions allowlists |
| S9 | FreeMarker `TemplateClassResolver` Javadoc (SAFER_RESOLVER) | https://freemarker.apache.org/docs/api/freemarker/core/TemplateClassResolver.html | Apache Software Foundation | 2026-08-25 | Expires 2027-02-25 or on FreeMarker doc change | Reviewed | -7 | FreeMarker 2.3.x Javadoc; SAFER_RESOLVER verified present |
| S10 | POSIX Vol. 1 Ch. 12 — Utility Argument Syntax (Guideline 10, end-of-options `--`) | https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html | The Open Group | 2026-08-25 | Expires 2027-02-25 or on new POSIX edition | Reviewed | -4 | Issue 8 base definitions; tool must document `--` support |

For every retained source also record version/SDK version, content hash or ETag where
obtainable, owner, plan/tier, region, and feature maturity when those dimensions apply.
Mark a control **Not verified** whenever its supporting evidence is missing, stale,
contradictory, inaccessible, snapshot-only, unsupported, or from failed tests.
