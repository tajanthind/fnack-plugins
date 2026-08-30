# Official fnack Plugins Repository

This repository hosts official first-party plugins for [fnack](https://github.com/tajanthind/fnack).

## Available Official Plugins

| Plugin ID | Name | Type | Description |
|-----------|------|------|-------------|
| `fnack.spotiflac` | SpotiFLAC | `downloader` | Lossless audio via SpotiFLAC (Tidal/Qobuz/Deezer/SoundCloud, zero-auth). Priority 10. |
| `fnack.ytdlp` | yt-dlp | `downloader` | YouTube / YouTube Music fallback downloader. Priority 50. |
| `fnack.deezer-batch` | Deezer (batch enrichment) | `metadata_provider` | Fast discography & album metadata lookup for queue/import pipeline. Priority 10. |
| `fnack.musicbrainz` | MusicBrainz | `metadata_provider` | Catalogue enrichment with 1 req/s rate-limiting. Priority 20. |
| `fnack.spotify` | Spotify (URL resolution) | `metadata_provider` | Zero-auth Spotify track URL resolution (ISRC-first). Priority 30. |
| `fnack.itunes` | iTunes Search API | `metadata_provider` | Fallback metadata provider. Priority 40. |
| `fnack.acoustid` | AcoustID Fingerprinting | `fingerprint` | Audio fingerprint identification and mismatch verification via chromaprint fpcalc. |
| `fnack.navidrome` | Navidrome Integration | `scan_trigger` | Triggers Navidrome media server scans and split-album repair. |
| `fnack.vpn` | VPN (WireGuard / OpenVPN) | `vpn` | Split-mode WireGuard/OpenVPN tunnel for download & metadata traffic. |
| `fnack.clean-navidrome-artists` | Clean Navidrome Artists | `library_task` | Cleanup phantom artists and empty artist rows in Navidrome. |
| `fnack.normalize-album-tags` | Normalize Album Tags | `library_task` | Aligns library tags with fnack database and merges split albums. |
| `fnack.fix-navidrome-splits` | Fix Navidrome Splits | `library_task` | Directly merges split album rows inside Navidrome's SQLite database. |
| `fnack.reverify-library` | Reverify Library | `library_task` | Re-verifies downloaded files against official metadata durations. |
| `fnack.subsonic` | Subsonic API | `server_extension` | Exposes fnack library as a Subsonic server for Symfonium, DSub, and Sublime Music. |
| `fnack.discord-webhook` | Discord Webhook | `event_hook` | Real-time Discord notifications for download completions, failures, and AcoustID flags. |
| `fnack.ntfy-webhook` | ntfy Webhook | `event_hook` | Push notifications via ntfy.sh or self-hosted ntfy instance. |
| `fnack.reverse-proxy-auth` | Reverse-Proxy Auth | `auth_provider` | Optional reverse-proxy header authentication (Authelia, Authentik). |

## Using in fnack

This repository index is pre-configured by default in fnack:
`https://raw.githubusercontent.com/tajanthind/fnack-plugins/main/index.json`

## Packaging Plugins

To package all plugins in `plugins/` into distribution archives in `dist/` and regenerate `index.json`:

```bash
python3 package_plugins.py
```
