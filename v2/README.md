# youtube-dl-v2

Simple CLI to download a YouTube video as an MP4 file using `yt-dlp` and Python.

## Setup

Use [uv](https://github.com/astral-sh/uv) to install dependencies:

```bash
uv sync
```

## Usage

```bash
uv run youtube_dl_v2.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Optional arguments:

- `-o/--output` – directory or full file path for the downloaded video.
- `-f/--format` – override the default yt-dlp format string.
- `--no-progress` – hide the progress bar output.
- `--player-client` – comma-separated YouTube client identifiers to try (defaults to
  `android,web`).
- `--merge-output-format` – container passed to yt-dlp when merging audio/video
  (defaults to `mp4`, use `none` to keep yt-dlp's automatic choice for higher
  resolutions like VP9/WebM).

The downloader prefers MP4-ready streams and merges to MP4 when needed.
