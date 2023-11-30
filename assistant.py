"""
This is a script to create knowledge files for OpenAI GPT assistants.
They currently have a pretty strict file count limit, so we need to merge all files in each section into one file.
"""

import os
import shutil

DOCS_PATH = "docs"
GENERATED_PATH = "assistant"


def generate(root_path):
    os.makedirs(GENERATED_PATH, exist_ok=True)

    for root, dirs, files in os.walk(root_path):
        if root == root_path:
            # Root directory is a special case, handled below
            continue

        content_lang_map = {}

        for file in files:
            if file.endswith(".md"):
                # Determine the language variant
                parts = file.split(".")
                language = parts[-2] if len(parts) > 2 else "en"

                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()

                if language not in content_lang_map:
                    content_lang_map[language] = []
                content_lang_map[language].append(f"== {file} ==\n\n{content}")

        # Write the combined content to new files
        for language, contents in content_lang_map.items():
            combined_filename = f"{os.path.basename(root)}.{language}.md"
            with open(
                os.path.join(GENERATED_PATH, combined_filename), "w", encoding="utf-8"
            ) as f:
                f.write("\n\n".join(contents))

    # Handle files in the root directory
    for file in os.listdir(root_path):
        file_path = os.path.join(root_path, file)
        if os.path.isfile(file_path) and file.endswith(".md"):
            shutil.copy(file_path, GENERATED_PATH)


if __name__ == "__main__":
    generate(DOCS_PATH)
