# Scholar Statistics

The homepage displays all-time citations, h-index, and i10-index from the public
Google Scholar profile configured for Yifei. It is a daily snapshot, not a live
Google Scholar API or a measure of research quality.

## Update flow

- GitHub Actions runs daily at 10:23 UTC, and can be run manually. Scheduled runs
  can be delayed by GitHub; inactive public repositories may have schedules disabled.
- `scripts/update_scholar.py` checks robots.txt and reads only the public profile's
  summary table. No pagination, proxy, CAPTCHA bypass, paid service, or API key.
- Only validated metrics are written to `scholar.json` on `google-scholar-stats`.
  No automatic commits go to `main`; the homepage still deploys from `main`.
- The page loads the latest JSON from that branch, with a seven-second timeout.
  Failed requests leave the most recent valid browser cache or built-in snapshot
  visible. The last successful fetch date is shown, not the page access date.
- If Google blocks a runner or changes its HTML, the action fails without changing
  the previous data. Check the action log; do not bypass Google's access controls.

## Local checks

```sh
python3 -m unittest discover -s tests -p 'test_update_scholar.py'
node tests/test_scholar_stats.js
```

To refresh the built-in no-JavaScript / network-failure snapshot intentionally:

```sh
python3 scripts/update_scholar.py --author-id y5FkC7cAAAAJ --output _data/scholar.json
```

Commit that snapshot only as part of an intentional homepage update. The initial
snapshot is not automatically rewritten in `main`. Keep the profile ID, include's
data URL, and workflow aligned if the profile or repository changes.
