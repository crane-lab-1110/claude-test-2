#!/bin/bash
# LINEスタンプ生成ツール セットアップスクリプト (Mac / Linux)
set -e

echo "===================================================="
echo " LINEスタンプ生成ツール セットアップ"
echo "===================================================="

# Python バージョン確認
PYTHON=$(command -v python3 || command -v python)
if [ -z "$PYTHON" ]; then
  echo "エラー: Python が見つかりません。Python 3.9 以上をインストールしてください。"
  exit 1
fi

VERSION=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python $VERSION を使用します"

MAJOR=$($PYTHON -c "import sys; print(sys.version_info.major)")
MINOR=$($PYTHON -c "import sys; print(sys.version_info.minor)")
if [ "$MAJOR" -lt 3 ] || { [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 9 ]; }; then
  echo "エラー: Python 3.9 以上が必要です（現在: $VERSION）"
  exit 1
fi

# 仮想環境の作成
if [ ! -d ".venv" ]; then
  echo ""
  echo "仮想環境を作成しています..."
  $PYTHON -m venv .venv
fi

# 仮想環境の有効化
source .venv/bin/activate

# 依存インストール
echo ""
echo "依存ライブラリをインストールしています..."
echo "（rembg は初回のみ モデル ~170MB をダウンロードします）"
pip install --upgrade pip -q
pip install -r requirements.txt

# 作業フォルダの作成
mkdir -p images

echo ""
echo "===================================================="
echo " セットアップ完了！"
echo "===================================================="
echo ""
echo "【使い方】"
echo ""
echo "  # 仮想環境を有効化（毎回必要）"
echo "  source .venv/bin/activate"
echo ""
echo "  # Step 1: ChatGPT用プロンプトを生成"
echo "  python generate_prompts.py \"かわいい猫\""
echo ""
echo "  # Step 4: 画像をLINE規格に変換"
echo "  python process_images.py --theme \"かわいい猫\""
echo ""
echo "詳しい手順は README.md を参照してください。"
