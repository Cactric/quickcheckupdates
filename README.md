# Quick check updates
Quickly check for Arch Linux updates (with some caveats)

## Caveats compared to `checkupdates`:
* The feed only contains a few entries (50 for the main one), so some updates may not show up
* Your mirror may not have synced yet for recent updates - this tool will display them anyway

## Benefits:
* Much less data gets downloaded - for me the feed is around 21 KB, versus around 7 MB

## Dependencies:
You need (Arch packages):
* `python`
* `python-feedparser`
* `pyalpm`
