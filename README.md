# Official fnack Plugins Repository

This repository hosts official first-party plugins for [fnack](https://github.com/tajanthind/fnack).

## Available Official Plugins

| Plugin ID | Name | Type | Description |
|-----------|------|------|-------------|
| `fnack.spotiflac` | SpotiFLAC | `downloader` | Lossless audio via SpotiFLAC (Tidal/Qobuz/Deezer/SoundCloud, zero-auth). Priority 10. |
| `fnack.ytdlp` | yt-dlp | `downloader` | YouTube / YouTube Music fallback downloader. Priority 50. |
| `fnack.deezer-batch` | Deezer (batch enrichment) | `metadata_provider` | Authoritative Deezer metadata (artist search/info, discography, track/album, album/track search) via artist.search / artist.discography / artist.info / track.metadata / album.metadata / album.search / track.search / album.tracks. Implementation lives in this plugin. Priority 10. |
| `fnack.musicbrainz` | MusicBrainz | `metadata_provider` | Authoritative catalogue enrichment (artist.search + enrich) with 1 req/s rate-limiting and plugin-owned cache. Implementation lives in this plugin. Priority 20. |
| `fnack.spotify` | Spotify (URL resolution) | `metadata_provider` | Authoritative zero-auth Spotify track URL resolution (ISRC-first) via the `track.resolve` capability. Implementation lives in this plugin. Priority 30. |
| `fnack.itunes` | iTunes Search API | `metadata_provider` | Authoritative iTunes fallback (artist.search / artist.discography / album.tracks). Implementation lives in this plugin. Priority 40. |
| `fnack.acoustid` | AcoustID Fingerprinting | `fingerprint` | Authoritative fingerprinting (fingerprint.identify): verification, unknown/regional identification, mismatch flags. API key plugin-owned. Implementation lives in this plugin. |
| `fnack.navidrome` | Navidrome Integration | `scan_trigger` | Authoritative Navidrome integration (media.scan / media.health / media.connection_test): ping test, debounced scan, split-album repair. Config plugin-owned. Implementation lives in this plugin. |
| `fnack.vpn` | VPN (WireGuard / OpenVPN) | `vpn` | Split-mode WireGuard/OpenVPN tunnel for download & metadata traffic. |
| `fnack.clean-navidrome-artists` | Clean Navidrome Artists | `library_task` | Cleanup phantom artists and empty artist rows in Navidrome. |
| `fnack.normalize-album-tags` | Normalize Album Tags | `library_task` | Aligns library tags with fnack database and merges split albums. |
| `fnack.fix-navidrome-splits` | Fix Navidrome Splits | `library_task` | Directly merges split album rows inside Navidrome's SQLite database. |
| `fnack.reverify-library` | Reverify Library | `library_task` | Re-verifies downloaded files against official metadata durations. |
| `fnack.subsonic` | Subsonic API | `server_extension` | Exposes fnack library as a Subsonic server for Symfonium, DSub, and Sublime Music. |
| `fnack.lidarr` | Lidarr Integration | `library_source`, `server_extension` | Lets Lidarr use fnack as its indexer + download client (Newznab/Torznab + SABnzbd emulation); grabs expand into fnack's library and download like any other track. |
| `fnack.discord-webhook` | Discord Webhook | `event_hook` | Real-time Discord notifications for download completions, failures, and AcoustID flags. |
| `fnack.ntfy-webhook` | ntfy Webhook | `event_hook` | Push notifications via ntfy.sh or self-hosted ntfy instance. |
| `fnack.reverse-proxy-auth` | Reverse-Proxy Auth | `auth_provider` | Optional reverse-proxy header authentication (Authelia, Authentik). |

## Using in fnack

This repository index is pre-configured by default in fnack:
`https://raw.githubusercontent.com/tajanthind/fnack-plugins/main/index.json`

All plugins above are **official** and installable from fnack's
**Settings → Plugins → Marketplace**. The fnack Docker image ships only the
**essential** subset (downloaders + discography sync); the authoritative
essential list lives in fnack's `plugins/essential.py` (`ESSENTIAL_PLUGINS`)
— every other official plugin here stays one click away in the Marketplace.

## Packaging Plugins

To package all plugins in `plugins/` into distribution archives in `dist/` and regenerate `index.json`:

```bash
python3 package_plugins.py
```

Manifest/index consistency is guarded by a deterministic parity test (plain
python, no pytest, no network):

```bash
python3 tests/test_manifest_index_parity.py
```
