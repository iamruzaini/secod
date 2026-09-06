# Implementation fixture plan: secod-react-native-expo

Given Expo code with a private key in `EXPO_PUBLIC_`, token persistence in AsyncStorage, unvalidated
Router link parameters, broad permissions, and sensitive notification data, move privileged work to
backend, use version-supported SecureStore/native linking APIs, minimize permissions/payloads, and
test development plus production builds. Documentation fixture; no scan executed.
