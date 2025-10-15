"""CLI tool to download a YouTube video as an MP4 file using yt-dlp."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

# Force mp4 output while preferring mp4 video/audio streams when available.
DEFAULT_FORMAT = "bv*[ext=mp4]+ba[ext=m4a]/bv*+ba/b"
# Default container remux target. Allow overriding to keep high-res formats
# that cannot be muxed into MP4 (e.g. VP9 video).
DEFAULT_MERGE_OUTPUT_FORMAT = "mp4"
# Use an Android client first to dodge recent SABR streaming restrictions, then
# fall back to the standard web client if needed.
DEFAULT_PLAYER_CLIENTS = ["android", "web"]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download a YouTube video as an MP4 file using yt-dlp."
    )
    parser.add_argument("url", help="YouTube video URL to download")
    parser.add_argument(
        "-o",
        "--output",
        help=(
            "Optional output path. Provide a directory to save the file there, or a "
            "full file path (including .mp4) to control the filename."
        ),
    )
    parser.add_argument(
        "-f",
        "--format",
        default=DEFAULT_FORMAT,
        help=(
            "yt-dlp format selection string to override the default mp4-preferring "
            "format."
        ),
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable the download progress output",
    )
    parser.add_argument(
        "--player-client",
        default=",".join(DEFAULT_PLAYER_CLIENTS),
        help=(
            "Comma-separated YouTube client identifiers to try when fetching video "
            "streams (e.g. android, web, tv)."
        ),
    )
    parser.add_argument(
        "--merge-output-format",
        default=DEFAULT_MERGE_OUTPUT_FORMAT,
        metavar="FORMAT",
        help=(
            "Container format passed to yt-dlp's merge_output_format option. Use "
            "'none' to disable forcing a container so that high-resolution "
            "streams (e.g. VP9/WebM) remain available."
        ),
    )
    return parser.parse_args(argv)


def build_output_template(output: str | None) -> str:
    if not output:
        return "%(title)s.%(ext)s"

    target = Path(output).expanduser()
    if target.suffix:
        if target.suffix.lower() != ".mp4":
            target = target.with_suffix(".mp4")
        target.parent.mkdir(parents=True, exist_ok=True)
        return str(target)

    target.mkdir(parents=True, exist_ok=True)
    return str(target / "%(title)s.%(ext)s")


def parse_player_clients(raw: str | None) -> list[str]:
    if not raw:
        return []

    return [item for item in (part.strip() for part in raw.split(",")) if item]


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    player_clients = parse_player_clients(args.player_client)
    merge_output_format = (
        None
        if args.merge_output_format is None
        else args.merge_output_format.strip() or None
    )
    if merge_output_format and merge_output_format.lower() == "none":
        merge_output_format = None

    ydl_opts = {
        "format": args.format,
        "noplaylist": True,
        "outtmpl": build_output_template(args.output),
        "noprogress": args.no_progress,
    }

    if merge_output_format is not None:
        ydl_opts["merge_output_format"] = merge_output_format

    if player_clients:
        ydl_opts["extractor_args"] = {
            "youtube": {"player_client": player_clients}
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([args.url])
    except DownloadError as exc:
        sys.stderr.write(f"Download failed: {exc}\n")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
