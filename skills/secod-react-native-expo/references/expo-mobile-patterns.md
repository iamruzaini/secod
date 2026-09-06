# Expo and React Native mobile patterns

## Storage and sessions

Resolve installed `expo-secure-store` API before coding. For native targets, store only small
session credentials with `SecureStore.setItemAsync`; handle reads returning no value, storage
errors, device-lock availability, logout, and account switching. Do not use AsyncStorage or
persisted Redux state for tokens. Web has no equivalent SecureStore guarantee; use secure,
HTTP-only server cookies where architecture supports them.

Never put private keys or unrestricted provider keys in `EXPO_PUBLIC_` variables. Expo replaces
those values into client bundles. Route privileged calls through backend/API routes and authorize
there.

## Links and navigation

- Prefer Expo Router HTTPS links configured as Android App Links and iOS Universal Links.
- Parse URL with a real URL parser, allowlist routes/hosts/actions, and reject bearer tokens or sensitive data in parameters.
- Protected route UI may improve navigation but does not authorize backend requests.
- OAuth public clients use provider-supported authorization code flow with PKCE and exact redirect configuration.

## Permissions and notifications

- Declare only required native permissions through supported app config or config plugins.
- Request at point of use and branch on denied/restricted states.
- Store Expo push token against authenticated user plus installation; remove/rotate it on logout, account change, and provider invalidation.
- Send minimal payloads. Fetch sensitive content after authenticated navigation and authorize every notification action on backend.

## Provider SDK boundary

Inspect provider's Expo/React Native support and installed package version. Public project IDs or
mobile configuration are not server secrets, but provider policy, App Check/attestation, API-key
restrictions, and backend authorization must constrain their use. Never substitute a server/Admin
SDK in client bundle.
