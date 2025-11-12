# YouTube Video Downloader v3.0

YouTube動画をダウンロードするためのシンプルなCLIツールです。`yt-dlp` と Python を使用してMP4ファイルとしてダウンロードします。

## 特徴

- 🎥 高品質な動画ダウンロード
- 🎵 音声付き動画の自動マージ
- 📝 字幕ダウンロード（日本語・英語対応）
- 📋 利用可能なフォーマット一覧表示
- ⏬ リアルタイムプログレスバー
- 🖼️ サムネイル埋め込み
- 📊 メタデータ保持
- ⚡ 高速ダウンロード

## セットアップ

[uv](https://github.com/astral-sh/uv) を使用して依存関係をインストールしてください：

```bash
uv sync
```

## 使用方法

### 基本的なダウンロード

```bash
uv run youtube_dl_v3.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 特定のフォーマットを指定してダウンロード

```bash
uv run youtube_dl_v3.py "https://www.youtube.com/watch?v=VIDEO_ID" --format 137
```

### 利用可能なフォーマット一覧を表示

```bash
uv run youtube_dl_v3.py --list-formats "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 出力ディレクトリを指定

```bash
uv run youtube_dl_v3.py "https://www.youtube.com/watch?v=VIDEO_ID" my_videos
```

## オプション

- `--format FORMAT` - 特定のフォーマットIDを指定（例: `--format 22`）
- `--list-formats` - 利用可能なフォーマット一覧を表示

## ダウンロードされるもの

- **動画ファイル**: MP4形式（音声付きでマージ）
- **字幕ファイル**: VTT形式（日本語・英語、利用可能な場合）
- **サムネイル**: WebP形式（動画に埋め込み）
- **メタデータ**: 動画情報（タイトル、チャンネル、再生回数など）

## フォーマットについて

YouTubeの動画は様々な品質・解像度で提供されています：

- `137`: 1920x1080 (1080p) - 高品質
- `136`: 1280x720 (720p) - 中品質
- `135`: 854x480 (480p) - 低品質
- `22`: 1280x720 + 音声 - 統合フォーマット

`--list-formats` オプションで各動画の利用可能なフォーマットを確認できます。

## 注意事項

- 字幕ダウンロードはレート制限がかかる場合がありますが、動画ダウンロードは正常に行われます
- ダウンロードしたファイルは `downloads/` フォルダに保存されます
- 著作権のあるコンテンツのダウンロードは自己責任でお願いします

## 例

```bash
# 高品質動画をダウンロード
uv run youtube_dl_v3.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format 137

# フォーマット一覧を確認
uv run youtube_dl_v3.py --list-formats "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 特定のディレクトリに保存
uv run youtube_dl_v3.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" /path/to/save
```

## トラブルシューティング

- **ダウンロードが遅い場合**: ネットワーク接続を確認してください
- **フォーマットが見つからない場合**: `--list-formats` で利用可能なフォーマットを確認してください
- **字幕がダウンロードできない場合**: YouTubeの仕様変更により一時的に利用できない可能性があります

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
