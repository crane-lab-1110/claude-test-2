"""
Step 4: 画像を LINE スタンプ規格に変換する

使い方:
  python process_images.py --theme "かわいい猫"
  python process_images.py --theme "サラリーマン" --images ./my_images
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("エラー: Pillow がインストールされていません。\n  pip install -r requirements.txt を実行してください。")

try:
    from rembg import remove
except ImportError:
    sys.exit("エラー: rembg がインストールされていません。\n  pip install -r requirements.txt を実行してください。")

# LINE スタンプ規格
STICKER_SIZE = (370, 320)
TAB_ICON_SIZE = (96, 74)
MAX_FILE_BYTES = 1 * 1024 * 1024  # 1 MB


def remove_background(img: Image.Image) -> Image.Image:
    """rembg で背景を除去して RGBA 画像を返す。"""
    import io
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    result_bytes = remove(buf.getvalue())
    return Image.open(io.BytesIO(result_bytes)).convert("RGBA")


def fit_on_canvas(img: Image.Image, canvas_size: tuple[int, int]) -> Image.Image:
    """アスペクト比を保ちながら canvas_size に収め、中央に配置する。"""
    canvas_w, canvas_h = canvas_size
    img.thumbnail((canvas_w, canvas_h), Image.LANCZOS)
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    offset_x = (canvas_w - img.width) // 2
    offset_y = (canvas_h - img.height) // 2
    canvas.paste(img, (offset_x, offset_y), img)
    return canvas


def save_png(img: Image.Image, path: str) -> int:
    """PNG として保存し、ファイルサイズ（バイト）を返す。"""
    img.save(path, format="PNG", optimize=True)
    return os.path.getsize(path)


def process_image(src_path: str, sticker_out: str, is_first: bool, tab_icon_out: str | None) -> bool:
    """
    1枚の画像を処理してLINE規格のスタンプとして保存する。
    is_first=True のとき tab_icon も生成する。
    成功すれば True を返す。
    """
    try:
        img = Image.open(src_path).convert("RGBA")
    except Exception as e:
        print(f"  ✗ 読み込み失敗: {e}")
        return False

    print("    背景除去中...", end=" ", flush=True)
    img_nobg = remove_background(img)
    print("完了")

    print("    リサイズ中...", end=" ", flush=True)
    sticker = fit_on_canvas(img_nobg, STICKER_SIZE)
    print("完了")

    size_bytes = save_png(sticker, sticker_out)
    size_kb = size_bytes / 1024
    if size_bytes > MAX_FILE_BYTES:
        print(f"  ⚠ ファイルサイズ超過: {size_kb:.0f} KB（上限 1024 KB）")
    else:
        print(f"  ✓ 保存完了: {sticker_out} ({size_kb:.0f} KB)")

    if is_first and tab_icon_out:
        tab = fit_on_canvas(img_nobg, TAB_ICON_SIZE)
        save_png(tab, tab_icon_out)
        print(f"  ✓ タブアイコン: {tab_icon_out}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="画像を LINE スタンプ規格（370x320 透過PNG）に変換します"
    )
    parser.add_argument("--theme", required=True, help='スタンプのテーマ名（出力フォルダ名に使用）')
    parser.add_argument(
        "--images", default="./images",
        help="入力画像フォルダ（デフォルト: ./images）"
    )
    parser.add_argument(
        "--output", default="./output",
        help="出力先フォルダ（デフォルト: ./output）"
    )
    args = parser.parse_args()

    images_dir = Path(args.images)
    if not images_dir.exists():
        sys.exit(f"エラー: 入力フォルダが見つかりません: {images_dir}\n"
                 f"  images/ フォルダを作成して画像を配置してください。")

    png_files = sorted(images_dir.glob("*.png")) + sorted(images_dir.glob("*.PNG"))
    jpg_files = sorted(images_dir.glob("*.jpg")) + sorted(images_dir.glob("*.jpeg"))
    all_files = sorted(set(png_files + jpg_files), key=lambda p: p.name)

    if not all_files:
        sys.exit(f"エラー: {images_dir} に画像ファイルが見つかりません。\n"
                 f"  PNG または JPG ファイルを配置してください。")

    safe_theme = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in args.theme)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.output) / f"{safe_theme}_{timestamp}"
    stickers_dir = out_dir / "stickers"
    stickers_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n==================================================")
    print(f" LINEスタンプ変換処理")
    print(f"==================================================")
    print(f"テーマ  : {args.theme}")
    print(f"入力    : {images_dir} ({len(all_files)} 枚)")
    print(f"出力    : {out_dir}")
    print(f"==================================================\n")

    tab_icon_path = str(out_dir / "tab_icon.png")
    success_count = 0

    for i, src in enumerate(all_files, start=1):
        print(f"[{i}/{len(all_files)}] {src.name}")
        out_name = f"{i:02d}.png"
        sticker_out = str(stickers_dir / out_name)
        ok = process_image(
            str(src),
            sticker_out,
            is_first=(i == 1),
            tab_icon_out=tab_icon_path if i == 1 else None,
        )
        if ok:
            success_count += 1
        print()

    print(f"==================================================")
    print(f" 完了: {success_count}/{len(all_files)} 枚変換成功")
    print(f" 出力フォルダ: {out_dir.resolve()}")
    print(f"==================================================")
    print()
    print("【LINE Creator Market へのアップロード手順】")
    print("  1. https://creator.line.me にアクセス")
    print("  2. 「スタンプ」→「新規登録」を選択")
    print(f"  3. stickers/ フォルダの画像を1枚ずつアップロード")
    print(f"  4. tab_icon.png をタブ画像としてアップロード")
    print("  5. AI ツール使用の申告にチェックを入れる（必須）")
    print("  6. 審査に提出")
    print()


if __name__ == "__main__":
    main()
