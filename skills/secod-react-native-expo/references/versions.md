# Version boundary

1. Resolve `expo`, `react-native`, Expo Router, and relevant `expo-*` package versions from lockfile.
2. Read the matching Expo SDK reference, not an unqualified latest snippet.
3. Check config-plugin and native target requirements before editing app config or generated projects.
4. Prefer CNG/config plugins when project uses them; preserve directly maintained native projects when repository does.
5. If installed API differs materially and version cannot be resolved, ask one narrow version/workflow question.

As reviewed on 2026-09-06, Expo documentation exposes a current `llms.txt` index and versioned SDK
references. React Native documentation also exposes `llms.txt`. Neither index alone proves an API is
available in installed version.
