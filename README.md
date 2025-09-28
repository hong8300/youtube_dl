# YouTube ダウンローダー

> [!WARNING]
> **⚠️ この README の内容は古いバージョン（v1）のものです**
>
> 最新版のソースコードとドキュメントはすべて **`/v2`** ディレクトリに移行しました。
>
> ### 📁 **[最新版はこちら → v2 ディレクトリ](./v2/README.md)**
>
> 以下の内容は旧バージョンの参考情報として残しています。

---

## 旧バージョン（v1）について

このプログラムは、YouTubeの動画を簡単にダウンロードするためのコマンドラインツールです。最高品質のMP4形式で動画をダウンロードし、進捗状況をリアルタイムで表示します。

## 機能

- ダウンロード進捗のリアルタイム表示（パーセンテージ、速度、残り時間）
- 動画の詳細情報（タイトル、長さ、視聴回数、投稿者、公開日）の表示
- エラー処理の強化

## 必要条件

- Python 3.6以上
- yt-dlp ライブラリ

## インストール方法

1. Condaの環境をアクティブにします（必要に応じて）：

```bash
conda activate work
```

2. 必要なライブラリをインストールします：

```bash
pip install yt-dlp
```

## 使用方法

基本的な使い方：

```bash
python youtube_downloader.py [YouTube URL]
```

出力先を指定する場合：

```bash
python youtube_downloader.py [YouTube URL] [出力パス]
```

### 例

```bash
# 基本的な使用方法（カレントディレクトリにダウンロード）
python youtube_downloader.py https://www.youtube.com/watch?v=_yZTsJdy0Tc

# 出力先を指定してダウンロード
python youtube_downloader.py https://www.youtube.com/watch?v=_yZTsJdy0Tc /path/to/download/folder
```

## 出力例

```
タイトル: 【鹿島アントラーズ×浦和レッズ｜ハイライト】2025明治安田J1リーグ第6節｜2025シーズン｜Jリーグ
長さ: 434秒
評価数: 107666回視聴
投稿者: DAZN Japan
公開日: 2025-03-16
ダウンロード中...
[youtube] Extracting URL: https://www.youtube.com/watch?v=_yZTsJdy0Tc
[youtube] _yZTsJdy0Tc: Downloading webpage
...
100.0% 速度: 36.56MiB/s 残り時間: 00:00
ダウンロード完了: /path/to/download/folder/【鹿島アントラーズ×浦和レッズ｜ハイライト】2025明治安田J1リーグ第6節｜2025シーズン｜Jリーグ.mp4
```

## MP4 to MOV
```
# そのまま
ffmpeg -i input.mp4 -c:v copy -c:a copy output.mov

# 再エンコード
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mov

# ハードウェアエンコード(mac)
ffmpeg -i input.mp4 -c:v h264_videotoolbox -c:a copy output.mov

```

## 注意事項

- このツールはローカル的な使用目的でのみ使用してください。
