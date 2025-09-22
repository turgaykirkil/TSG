from __future__ import annotations

import argparse
import sys
from pathlib import Path

from utils.scrape_helpers import solve_captcha_image


def main() -> int:
    parser = argparse.ArgumentParser(description="Try solving a CAPTCHA image via Tesseract (fallback: Ollama if available)")
    parser.add_argument("--image", required=True, help="Path to CAPTCHA image (png/jpg)")
    args = parser.parse_args()

    img_path = Path(args.image)
    if not img_path.exists():
        print(f"Image not found: {img_path}", file=sys.stderr)
        return 2

    code = solve_captcha_image(str(img_path))
    if code:
        print(code)
        return 0
    print("<unresolved>")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
