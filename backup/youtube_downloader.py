import os
import sys
import json
import yt_dlp

def get_video_info(url):
    """YouTubeの動画情報を取得する"""
    try:
        # yt-dlpのオプション設定
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,  # 情報取得のみで、ダウンロードはしない
            'format': 'best',
        }
        
        # yt-dlpで動画情報を取得
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # 動画情報を返す
            return {
                'title': info.get('title', 'Unknown Title'),
                'duration': info.get('duration', 0),
                'view_count': info.get('view_count', 0),
                'uploader': info.get('uploader', 'Unknown Uploader'),
                'upload_date': info.get('upload_date', ''),
                'formats': info.get('formats', []),
                'thumbnail': info.get('thumbnail', ''),
                'description': info.get('description', ''),
                'id': info.get('id', ''),
            }
    except Exception as e:
        print(f"動画情報の取得中にエラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def format_upload_date(date_str):
    """YYYYMMDDの形式の日付文字列をYYYY-MM-DDに変換する"""
    if len(date_str) == 8:
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    return date_str

def download_youtube_video(url, output_path=None):
    """YouTubeの動画をMP4形式でダウンロードする"""
    # 動画情報を取得
    video_info = get_video_info(url)
    if not video_info:
        return None
    
    try:
        # 動画情報を表示
        print(f"タイトル: {video_info['title']}")
        print(f"長さ: {video_info['duration']}秒")
        print(f"評価数: {video_info['view_count']}回視聴")
        print(f"投稿者: {video_info['uploader']}")
        if video_info['upload_date']:
            print(f"公開日: {format_upload_date(video_info['upload_date'])}")
        
        # 出力パスが指定されていない場合はカレントディレクトリを使用
        if output_path is None:
            output_path = os.getcwd()
        
        # 出力ディレクトリが存在しない場合は作成
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # ファイル名を作成（タイトルから無効な文字を削除）
        import re
        filename = re.sub(r'[\\/*?:"<>|]', "", video_info['title'])
        output_template = os.path.join(output_path, f"{filename}.%(ext)s")
        
        # ダウンロードオプションを設定
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # 最高品質のMP4を優先
            'outtmpl': output_template,
            'progress_hooks': [lambda d: print_progress(d)],
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': True,
        }
        
        print("ダウンロード中...")
        # yt-dlpで動画をダウンロード
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # ダウンロードされたファイルのパスを取得
        expected_file = os.path.join(output_path, f"{filename}.mp4")
        if os.path.exists(expected_file):
            print(f"\nダウンロード完了: {expected_file}")
            return expected_file
        else:
            # mp4以外の形式でダウンロードされた可能性がある
            files = [f for f in os.listdir(output_path) if f.startswith(filename) and os.path.isfile(os.path.join(output_path, f))]
            if files:
                downloaded_file = os.path.join(output_path, files[0])
                print(f"\nダウンロード完了: {downloaded_file}")
                return downloaded_file
            else:
                print("ダウンロードされたファイルが見つかりません")
                return None
            
    except Exception as e:
        print(f"ダウンロード中にエラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def print_progress(d):
    """ダウンロード進捗を表示するコールバック関数"""
    if d['status'] == 'downloading':
        percentage = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"\r{percentage} 速度: {speed} 残り時間: {eta}", end='')
    elif d['status'] == 'finished':
        print("\nダウンロード完了、変換処理中...")

def main():
    # コマンドライン引数からURLと出力パスを取得
    if len(sys.argv) < 2:
        print("使用方法: python youtube_downloader.py [YouTube URL] [出力パス(省略可)]")
        return
    
    url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    download_youtube_video(url, output_path)

if __name__ == "__main__":
    main()
