"""
Step 1: ChatGPT用プロンプトを生成する

使い方:
  python generate_prompts.py "かわいい猫"
  python generate_prompts.py "サラリーマン" --count 16
"""

import argparse
import os
import sys
from datetime import datetime

CHATGPT_PROMPT_TEMPLATE = """\
You are a professional LINE sticker designer. Create a set of {count} LINE stickers based on the theme: "{theme}".

Follow these steps:

1. Decide on a main character or motif that fits the theme.
2. Choose an art style (kawaii, chibi, anime, cartoon, watercolor, etc.) that best suits the theme.
3. List {count} different expressions, emotions, or actions for the character (e.g., happy, sad, angry, laughing, crying, sleeping, eating, thumbs up, etc.).
4. For each expression/action, write an optimized DALL-E image generation prompt.

Rules for each DALL-E prompt:
- The character must be on a PLAIN WHITE background (important for background removal)
- Isolated single character, centered in frame
- Sticker-style illustration, no text
- Cute and expressive
- Consistent character design across all prompts
- Include the art style in every prompt

Output format (strictly follow this, output only the numbered list, no extra text):
1. "[DALL-E prompt here]"
2. "[DALL-E prompt here]"
...
{count}. "[DALL-E prompt here]"
"""

INSTRUCTIONS_TEMPLATE = """\
==================================================
 LINEスタンプ自動生成 - Step 1 完了
==================================================

テーマ: {theme}
生成枚数: {count}枚

【次の手順】

▼ Step 2: ChatGPTでDALL-Eプロンプトを生成
─────────────────────────────────────────
1. 以下のファイルを開いてください：
   {prompt_file}

2. ファイルの内容を全てコピーして ChatGPT に貼り付けます

3. ChatGPT が {count} 個の DALL-E プロンプトを番号付きリストで返します

▼ Step 3: ChatGPTのDALL-Eで画像を生成・保存
─────────────────────────────────────────
1. images/ フォルダを作成してください（まだなければ）

2. ChatGPTが出力した各プロンプトを1つずつ
   「DALL-E で画像を生成して」と ChatGPT に依頼します
   ※ ChatGPT Plus の場合、DALL-E 3 が使えます

3. 生成された画像を以下の名前で保存してください：
   images/01.png
   images/02.png
   ...
   images/{count_padded}.png

4. 全{count}枚保存したら Step 4 へ進んでください

▼ Step 4: 画像を LINE 規格に変換
─────────────────────────────────────────
以下のコマンドを実行してください：

  python process_images.py --theme "{theme}"

==================================================
"""


def main():
    parser = argparse.ArgumentParser(
        description="LINEスタンプ用のChatGPTプロンプトを生成します"
    )
    parser.add_argument("theme", help='スタンプのテーマ（例: "かわいい猫"）')
    parser.add_argument(
        "--count", type=int, default=16,
        choices=[8, 16, 24, 32, 40],
        help="スタンプ枚数（デフォルト: 16）"
    )
    args = parser.parse_args()

    theme = args.theme
    count = args.count
    count_padded = str(count).zfill(2)

    os.makedirs("prompts", exist_ok=True)

    safe_theme = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in theme)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prompt_filename = f"prompts/{safe_theme}_{timestamp}.txt"

    chatgpt_prompt = CHATGPT_PROMPT_TEMPLATE.format(
        theme=theme,
        count=count,
    )

    with open(prompt_filename, "w", encoding="utf-8") as f:
        f.write(chatgpt_prompt)

    instructions = INSTRUCTIONS_TEMPLATE.format(
        theme=theme,
        count=count,
        count_padded=count_padded,
        prompt_file=prompt_filename,
    )
    print(instructions)


if __name__ == "__main__":
    main()
