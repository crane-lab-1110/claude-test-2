@echo off
REM LINEスタンプ生成ツール セットアップスクリプト (Windows)
echo ====================================================
echo  LINEスタンプ生成ツール セットアップ
echo ====================================================

REM Python 確認
python --version >nul 2>&1
if errorlevel 1 (
    echo エラー: Python が見つかりません。
    echo https://www.python.org/ から Python 3.9 以上をインストールしてください。
    pause
    exit /b 1
)

REM 仮想環境の作成
if not exist ".venv" (
    echo.
    echo 仮想環境を作成しています...
    python -m venv .venv
)

REM 仮想環境の有効化
call .venv\Scripts\activate.bat

REM 依存インストール
echo.
echo 依存ライブラリをインストールしています...
echo （rembg は初回のみ モデル ^~170MB をダウンロードします）
pip install --upgrade pip -q
pip install -r requirements.txt

REM 作業フォルダの作成
if not exist "images" mkdir images

echo.
echo ====================================================
echo  セットアップ完了！
echo ====================================================
echo.
echo 【使い方】
echo.
echo   # 仮想環境を有効化（毎回必要）
echo   .venv\Scripts\activate
echo.
echo   # Step 1: ChatGPT用プロンプトを生成
echo   python generate_prompts.py "かわいい猫"
echo.
echo   # Step 4: 画像をLINE規格に変換
echo   python process_images.py --theme "かわいい猫"
echo.
echo 詳しい手順は README.md を参照してください。
pause
