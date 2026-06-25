#!/usr/bin/env python3
"""
YouTube動画ダウンロードスクリプト
使用方法: uv run youtube_dl_v3.py "URL"
"""

import sys
import os
from pathlib import Path
import yt_dlp
from datetime import datetime


def download_subtitles(url, output_dir, info):
    """
    字幕をダウンロードする（失敗しても続行）
    """
    video_id = info.get('id')
    title = info.get('title', 'Unknown')
    base_filename = f"{title}_{video_id}"

    subtitle_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['ja', 'en'],
        'outtmpl': f'{output_dir}/{base_filename}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,  # 動画はダウンロードしない
        'nocheckcertificate': True,
        'geo_bypass': True,

        # YouTubeの署名/nチャレンジを解くためのEJSスクリプトを取得
        'remote_components': ['ejs:github'],
    }

    try:
        print("📝 字幕ダウンロード中...")
        with yt_dlp.YoutubeDL(subtitle_opts) as ydl:
            ydl.download([url])
        print("✓ 字幕ダウンロード完了")
    except Exception as e:
        print(f"⚠️ 字幕ダウンロード失敗（ダウンロードは続行）: {e}")


def download_video(url, output_dir="downloads"):
    """
    YouTube動画をダウンロードする

    Args:
        url: YouTube動画のURL
        output_dir: ダウンロード先ディレクトリ
    """
    # ダウンロード先ディレクトリを作成
    Path(output_dir).mkdir(exist_ok=True)

    # yt-dlpの設定オプション
    ydl_opts = {
        # 出力ファイル名のテンプレート
        'outtmpl': f'{output_dir}/%(title)s_%(id)s.%(ext)s',

        # フォーマット選択（より柔軟な設定）
        # 動画+音声の組み合わせを優先し、フォールバックを追加
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/bestvideo+bestaudio/best',

        # 字幕は別途ダウンロードするため、ここでは無効
        'writesubtitles': False,
        'writeautomaticsub': False,

        # サムネイルを埋め込む
        'writethumbnail': True,
        'embedthumbnail': True,

        # メタデータを保持
        'keepvideo': True,
        'addmetadata': True,

        # プログレスフック
        'progress_hooks': [progress_hook],

        # エラー時も続行
        'ignoreerrors': False,

        # プレイリストの場合は全動画をダウンロード
        'playlistend': None,

        # ffmpegのパス（必要に応じて）
        # 'ffmpeg_location': '/usr/local/bin/ffmpeg',

        # ダウンロード後にffmpegで処理
        'postprocessors': [
            {
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            },
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            },
        ],

        # 静かなモード（False:詳細表示, True:最小限の出力）
        'quiet': False,
        'no_warnings': False,

        # その他のオプション
        'nocheckcertificate': True,
        'geo_bypass': True,

        # YouTubeの署名/nチャレンジを解くためのEJSスクリプトを取得
        # （これが無いと一部フォーマットのURLが無効になり HTTP 403 で停止する）
        'remote_components': ['ejs:github'],

        # 通信エラー/403対策のリトライ
        'retries': 10,
        'fragment_retries': 10,
        'file_access_retries': 5,

        # ブラウザのCookieを使用（必要に応じて）
        # 'cookiesfrombrowser': 'chrome',
    }

    try:
        print(f"\n📥 ダウンロード開始: {url}")
        print(f"📁 保存先: {output_dir}/")
        print("-" * 50)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 動画情報を取得
            info = ydl.extract_info(url, download=False)

            # 動画情報を表示
            if 'entries' in info:
                # プレイリストの場合
                print(f"📋 プレイリスト: {info.get('title', 'Unknown')}")
                print(f"📊 動画数: {len(info['entries'])}本")
            else:
                # 単一動画の場合
                print(f"📹 タイトル: {info.get('title', 'Unknown')}")
                print(f"👤 チャンネル: {info.get('uploader', 'Unknown')}")
                print(f"⏱️ 長さ: {format_duration(info.get('duration', 0))}")
                print(f"👁️ 再生回数: {info.get('view_count', 'Unknown'):,}")

            print("-" * 50)

            # ダウンロード実行
            ydl.download([url])

        # 字幕をダウンロード（失敗しても続行）
        download_subtitles(url, output_dir, info)

        print("\n✅ ダウンロード完了！")

    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ ダウンロードエラー: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ ダウンロードが中断されました")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        sys.exit(1)


def progress_hook(d):
    """
    ダウンロード進行状況を表示するフック関数
    """
    if d['status'] == 'downloading':
        # ダウンロード中の進行状況を表示
        total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        downloaded = d.get('downloaded_bytes', 0)
        
        if total > 0:
            percentage = (downloaded / total) * 100
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)
            
            # 速度をMB/s単位で表示
            speed_mb = speed / 1024 / 1024 if speed else 0
            
            # プログレスバーを作成
            bar_length = 30
            filled_length = int(bar_length * downloaded // total)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            
            # 進行状況を表示
            print(f"\r⏬ [{bar}] {percentage:.1f}% | {speed_mb:.2f} MB/s | ETA: {format_time(eta)}", end='', flush=True)
    
    elif d['status'] == 'finished':
        # ダウンロード完了
        filename = d.get('filename', 'unknown')
        print(f"\n✓ ダウンロード完了: {os.path.basename(filename)}")


def format_duration(seconds):
    """秒数を時:分:秒形式に変換"""
    if not seconds:
        return "Unknown"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def format_time(seconds):
    """秒数を読みやすい形式に変換"""
    if not seconds:
        return "Unknown"
    if seconds < 60:
        return f"{seconds}秒"
    elif seconds < 3600:
        return f"{seconds // 60}分{seconds % 60}秒"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}時間{minutes}分"


def main():
    """メイン関数"""
    # コマンドライン引数をチェック
    if len(sys.argv) < 2:
        print("❌ エラー: URLを指定してください")
        print(f"使用方法: {sys.argv[0]} <YouTube URL> [出力ディレクトリ]")
        print(f"例: {sys.argv[0]} \"https://www.youtube.com/watch?v=xxxxx\"")
        print(f"例: {sys.argv[0]} \"https://www.youtube.com/watch?v=xxxxx\" my_videos")
        print(f"\n📋 オプション:")
        print(f"  --list-formats <URL>   利用可能なフォーマット一覧を表示")
        print(f"  --format FORMAT       特定のフォーマットを指定（例: --format 22）")
        sys.exit(1)
    
    # 最初の引数をチェック
    first_arg = sys.argv[1]
    
    # --list-formatsが最初の引数の場合
    if first_arg == "--list-formats":
        if len(sys.argv) < 3:
            print("❌ エラー: --list-formats の後にURLを指定してください")
            print(f"例: {sys.argv[0]} --list-formats \"https://www.youtube.com/watch?v=xxxxx\"")
            sys.exit(1)
        url = sys.argv[2]
        list_formats(url)
        sys.exit(0)
    
    # 通常のURL処理
    url = first_arg
    output_dir = "downloads"
    format_code = None
    
    # 残りのオプション引数の処理
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == "--format" and i + 1 < len(sys.argv):
            format_code = sys.argv[i + 1]
            i += 2
        elif arg == "--list-formats":
            # URLの後に--list-formatsが来た場合
            list_formats(url)
            sys.exit(0)
        elif not arg.startswith("--"):
            # オプションでない場合は出力ディレクトリとして扱う
            output_dir = arg
            i += 1
        else:
            print(f"⚠️ 不明なオプション: {arg}")
            i += 1
    
    # ヘッダー表示
    print("\n" + "=" * 50)
    print("🎥 YouTube Video Downloader v3.0")
    print("=" * 50)
    print(f"📅 実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # フォーマット指定がある場合は渡す
    if format_code:
        download_video_with_format(url, output_dir, format_code)
    else:
        download_video(url, output_dir)
    
    print(f"\n📂 ファイルは '{output_dir}/' フォルダに保存されました")
    print("=" * 50 + "\n")


def list_formats(url):
    """利用可能なフォーマット一覧を表示"""
    print("\n📋 利用可能なフォーマット一覧を取得中...")

    # より詳細なオプションでフォーマット情報を取得
    ydl_opts = {
        'quiet': False,  # 詳細情報を表示
        'no_warnings': False,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'extract_flat': False,  # 完全な情報を取得

        # YouTubeの署名/nチャレンジを解くためのEJSスクリプトを取得
        'remote_components': ['ejs:github'],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            print(f"\n📹 タイトル: {info.get('title', 'Unknown')}")
            print("-" * 60)

            formats = info.get('formats', [])

            if not formats:
                print("⚠️ 利用可能なフォーマットが見つかりませんでした")
                print("💡 ヒント: YouTubeの仕様変更により、一時的に利用できない可能性があります")
                print("   しばらく時間をおいて再度お試しください")
                return

            # フォーマットをカテゴリ別に整理
            video_formats = []
            audio_formats = []

            for f in formats:
                format_id = f.get('format_id', 'N/A')
                ext = f.get('ext', 'N/A')
                resolution = f.get('resolution', 'N/A')
                fps = f.get('fps', 'N/A')
                vcodec = f.get('vcodec', 'N/A')
                acodec = f.get('acodec', 'N/A')
                filesize = f.get('filesize', 0)
                url_available = f.get('url', None) is not None

                # ファイルサイズをMBで表示
                size_mb = filesize / 1024 / 1024 if filesize else 0
                size_str = f"{size_mb:.1f}MB" if size_mb > 0 else "N/A"

                # URLが利用可能かチェック
                status = "✓" if url_available else "✗"

                if vcodec != 'none':
                    video_formats.append({
                        'id': format_id,
                        'ext': ext,
                        'resolution': resolution,
                        'fps': fps,
                        'size': size_str,
                        'vcodec': vcodec,
                        'acodec': acodec,
                        'available': url_available,
                        'status': status,
                    })
                elif acodec != 'none':
                    audio_formats.append({
                        'id': format_id,
                        'ext': ext,
                        'acodec': acodec,
                        'size': size_str,
                        'available': url_available,
                        'status': status,
                    })

            # 動画フォーマットを表示
            if video_formats:
                print("\n🎥 動画フォーマット:")
                print(f"{'ID':<6} {'解像度':<10} {'FPS':<5} {'形式':<5} {'サイズ':<10} {'ステータス':<8} {'コーデック'}")
                print("-" * 70)
                for f in sorted(video_formats, key=lambda x: (x['available'], x['resolution']), reverse=True):
                    print(f"{f['id']:<6} {f['resolution']:<10} {f['fps']:<5} {f['ext']:<5} {f['size']:<10} {f['status']:<8} {f['vcodec']}")

            # 音声フォーマットを表示
            if audio_formats:
                print("\n🎵 音声フォーマット:")
                print(f"{'ID':<6} {'形式':<5} {'サイズ':<10} {'ステータス':<8} {'コーデック'}")
                print("-" * 50)
                for f in audio_formats:
                    print(f"{f['id']:<6} {f['ext']:<5} {f['size']:<10} {f['status']:<8} {f['acodec']}")

            # 利用可能なフォーマットがあるかチェック
            available_video = [f for f in video_formats if f['available']]
            available_audio = [f for f in audio_formats if f['available']]

            if available_video or available_audio:
                print("\n💡 ヒント: 特定のフォーマットをダウンロードするには:")
                print(f"   uv run youtube_dl_v3.py \"{url}\" --format <ID>")
                print(f"   例: uv run youtube_dl_v3.py \"{url}\" --format 22")
                if available_video:
                    best_video = max(available_video, key=lambda x: x['resolution'])
                    print(f"   おすすめ: --format {best_video['id']} (最高品質の動画)")
            else:
                print("\n⚠️ 利用可能なフォーマットがありません")
                print("💡 ヒント: YouTubeの仕様変更により、一時的に利用できない可能性があります")
                print("   しばらく時間をおいて再度お試しください")

    except yt_dlp.utils.DownloadError as e:
        print(f"❌ ダウンロードエラー: {e}")
        print("💡 ヒント: 動画が削除されたか、非公開になっている可能性があります")
    except yt_dlp.utils.ExtractorError as e:
        print(f"❌ 抽出エラー: {e}")
        print("💡 ヒント: YouTubeの仕様変更により、情報取得に失敗しました")
        print("   yt-dlpを最新版にアップデートしてください: uv lock --upgrade")
    except Exception as e:
        print(f"❌ エラー: {e}")
        print("💡 ヒント: 予期しないエラーが発生しました")
        print("   詳細: https://github.com/yt-dlp/yt-dlp/issues")


def download_video_with_format(url, output_dir, format_code):
    """指定されたフォーマットで動画をダウンロード"""
    Path(output_dir).mkdir(exist_ok=True)

    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s_%(id)s.%(ext)s',
        'format': f'{format_code}+bestaudio/best',  # 指定されたフォーマットに音声を追加
        'writesubtitles': False,  # 字幕は別途ダウンロード
        'writeautomaticsub': False,
        'writethumbnail': True,
        'embedthumbnail': True,
        'keepvideo': True,
        'addmetadata': True,
        'progress_hooks': [progress_hook],
        'ignoreerrors': False,
        'quiet': False,
        'no_warnings': False,
        'nocheckcertificate': True,
        'geo_bypass': True,

        # YouTubeの署名/nチャレンジを解くためのEJSスクリプトを取得
        'remote_components': ['ejs:github'],

        # 通信エラー/403対策のリトライ
        'retries': 10,
        'fragment_retries': 10,
        'file_access_retries': 5,
    }

    try:
        print(f"\n📥 ダウンロード開始: {url}")
        print(f"📁 保存先: {output_dir}/")
        print(f"🎯 指定フォーマット: {format_code}")
        print("-" * 50)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 動画情報を取得
            info = ydl.extract_info(url, download=False)

            # 動画情報を表示
            print(f"📹 タイトル: {info.get('title', 'Unknown')}")
            print(f"👤 チャンネル: {info.get('uploader', 'Unknown')}")
            print(f"⏱️ 長さ: {format_duration(info.get('duration', 0))}")
            print(f"👁️ 再生回数: {info.get('view_count', 'Unknown'):,}")
            print("-" * 50)

            # ダウンロード実行
            ydl.download([url])

        # 字幕をダウンロード（失敗しても続行）
        download_subtitles(url, output_dir, info)

        print("\n✅ ダウンロード完了！")

    except Exception as e:
        print(f"\n❌ エラー: {e}")
        print("💡 ヒント: --list-formats オプションで利用可能なフォーマットを確認してください")
        sys.exit(1)


if __name__ == "__main__":
    main()
