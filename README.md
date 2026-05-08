# LINE スタンプ自動生成ツール

テーマを入力するだけで、LINEクリエイターズマーケットで販売できるスタンプセットを生成するツールです。
**APIキー不要** — ChatGPT（手動）+ ローカル画像処理で動作します。

---

## 仕組み

```
[あなた] テーマを入力
    ↓
[このツール] ChatGPT用プロンプトを生成
    ↓
[ChatGPT] 16個のDALL-Eプロンプトを出力
    ↓
[ChatGPT DALL-E] 画像を生成（手動）
    ↓
[このツール] 背景除去 + LINE規格にリサイズ → 完成
```

---

## インストール

Python 3.10 以上が必要です。

```bash
pip install -r requirements.txt
```

> **注意:** `rembg` は初回実行時に背景除去モデル（約170MB）を自動ダウンロードします。

---

## 使い方

### Step 1: ChatGPT用プロンプトを生成

```bash
python generate_prompts.py "かわいい猫"
```

`prompts/` フォルダにプロンプトファイルが生成されます。

オプション:
```bash
python generate_prompts.py "サラリーマン" --count 8   # 8枚セット
python generate_prompts.py "ゆるい犬" --count 24      # 24枚セット
```

---

### Step 2: ChatGPTでDALL-Eプロンプトを生成

1. `prompts/` 内に生成されたファイルを開く
2. 内容を全てコピーして **ChatGPT** に貼り付ける
3. ChatGPTが16個のDALL-Eプロンプトを番号付きリストで返す

---

### Step 3: ChatGPTのDALL-Eで画像を生成・保存

1. `images/` フォルダを作成する

```bash
mkdir images
```

2. ChatGPTが出力した各プロンプトを1つずつ ChatGPT に貼り付け、DALL-E で画像を生成する
   - ChatGPT Plus では DALL-E 3 が使用可能
3. 生成された画像を `images/` に保存する（ファイル名は自由、処理順は名前順）

```
images/
├── 01.png
├── 02.png
...
└── 16.png
```

---

### Step 4: LINE規格に変換

```bash
python process_images.py --theme "かわいい猫"
```

`output/かわいい猫_YYYYMMDD_HHMMSS/` に以下が生成されます:

```
output/かわいい猫_20240508_123456/
├── stickers/
│   ├── 01.png   ← 370×320px 透過PNG
│   ├── 02.png
│   ...
│   └── 16.png
└── tab_icon.png ← 96×74px 透過PNG
```

---

## LINE Creator Market へのアップロード

1. [creator.line.me](https://creator.line.me) にアクセスしてログイン
2. 「スタンプ」→「新規登録」
3. `stickers/` 内の画像を1枚ずつアップロード
4. `tab_icon.png` をタブ画像としてアップロード
5. **「AIを使用した」チェックボックスにチェックを入れる**（必須）
6. タイトル・説明文を入力して審査に提出
7. 審査通過後（数時間〜2日）、LINEストアで販売開始

---

## スタンプ技術仕様

| 種別 | サイズ | 形式 |
|------|--------|------|
| スタンプ本体 | 370 × 320 px（最大） | PNG（透過背景） |
| タブアイコン | 96 × 74 px | PNG |
| ファイルサイズ | 1 MB 以下/枚 | - |
| セット枚数 | 8 / 16 / 24 / 32 / 40 枚 | - |

---

## よくある質問

**Q: 背景除去の精度が低い場合は？**
白背景で生成した画像であれば rembg の精度が向上します。DALL-E プロンプトに `plain white background` が含まれていることを確認してください。

**Q: ファイルサイズが 1MB を超えてしまった場合は？**
処理時に警告が表示されます。Pillow で追加圧縮するか、画像サイズを小さくしてください。

**Q: アニメーションスタンプは作れますか？**
現在のツールは静止画スタンプのみ対応しています。
