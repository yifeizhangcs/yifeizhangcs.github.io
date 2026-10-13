# Scholar Statistics

The homepage embeds three hosted Google Scholar badges: all-time citations,
h-index, and i10-index. No local task, crawler, API key, or automatic Git commit
is needed. Every badge links to the public Scholar profile.

- Provider: https://github.com/dexhunter/google-scholar-badge
- Rendering: https://shields.io/badges/endpoint-badge
- The provider's source defaults to a seven-day Redis cache when Redis is enabled.
  Shields also caches images; this is automatic cached data, not guaranteed live data.
- The provider depends on its SerpApi quota and uptime. The homepage labels the
  figures as cached, does not invent a refresh timestamp, and keeps a direct link
  to Scholar for checking the authoritative current values.
- The initial GitHub-hosted crawler returned HTTP 403 and was removed rather than
  installing local background jobs or bypassing Google's access controls.

Display markup lives in `_includes/scholar-stats.html`; the small stylesheet is
`assets/css/scholar-stats.css`. If the Scholar profile changes, update the three
encoded `user` parameters and `_config.yml`'s `google_scholar` link together.
