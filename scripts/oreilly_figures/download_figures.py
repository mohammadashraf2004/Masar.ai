"""Download the figures of one O'Reilly book into a local staging folder.

Runs on your machine with your own O'Reilly login (a browser window opens; sign in
there, then press ENTER in the terminal). Nothing is written into backend/courses:
review the staging folder, then copy the figures you want into a course folder and
add them to that course's assets_manifest.json (see docs/lesson-figures.md).

Setup (once):
    pip install playwright
    playwright install chromium

Usage:
    python scripts/oreilly_figures/download_figures.py \
        --book-base https://learning.oreilly.com/library/view/hands-on-large-language/9781098150952/ \
        --chapters 12

Output (gitignored): scripts/oreilly_figures/_staging/<book-id>/chapter_NN/
    figure_NN_<caption>.<ext>, a .txt per figure, figures.json; plus all_figures.json
The browser profile (your session cookies) is kept in scripts/oreilly_figures/_profile
and is gitignored. Never commit it.
"""

import argparse
import asyncio
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
PROFILE_DIR = HERE / "_profile"
STAGING_DIR = HERE / "_staging"

# Pause between requests so the run stays gentle on the site.
DOWNLOAD_DELAY_MS = 1500
CHAPTER_DELAY_MS = 3000

EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "image/svg+xml": ".svg",
    "image/avif": ".avif",
}
REJECT_WORDS = (
    "logo", "favicon", "avatar", "profile", "icon", "spinner", "loading",
    "badge", "button", "social", "facebook", "twitter", "linkedin", "instagram",
)


def clean_filename(text: str, max_length: int = 120) -> str:
    """'Figure 3-2. The Transformer Architecture' -> 'The_Transformer_Architecture'."""
    if not text:
        return "image"
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^figure\s+\d+(?:[-.]\d+)*[.:]?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r'[<>:"/\\|?*]', "", text)
    text = re.sub(r"[^\w\-]+", "_", text, flags=re.UNICODE)
    text = re.sub(r"_+", "_", text).strip("_")
    return (text or "image")[:max_length]


def get_extension(url: str, content_type: str | None = None) -> str:
    if content_type:
        for mime, extension in EXTENSIONS.items():
            if mime in content_type.lower():
                return extension
    path = urlparse(url).path.lower()
    for extension in (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"):
        if path.endswith(extension):
            return ".jpg" if extension == ".jpeg" else extension
    return ".jpg"


async def wait_for_login(page, book_base: str, timeout_s: int = 600):
    """No terminal to press ENTER in: continue once the chapter text is on screen."""
    print("\nSign in to O'Reilly in the browser window; continuing automatically once the chapter loads...")
    for _ in range(timeout_s // 2):
        on_book = page.url.startswith(book_base)
        has_text = await page.evaluate("document.querySelectorAll('article p, main p, #sbo-rt-content p').length")
        if on_book and has_text > 5:
            print("Chapter text detected, starting.")
            return
        await page.wait_for_timeout(2000)
        if not on_book and "login" not in page.url and "sign" not in page.url:
            await page.goto(f"{book_base}", wait_until="domcontentloaded", timeout=60_000)
    raise SystemExit("Timed out waiting for sign-in.")


async def scroll_page(page):
    """Scroll through the chapter so lazy-loaded images load."""
    print("  Scrolling page to load lazy images...")
    previous_height = 0
    for _ in range(40):
        current_height = await page.evaluate("document.body.scrollHeight")
        if current_height == previous_height:
            break
        previous_height = current_height
        await page.evaluate(
            """
            async () => {
                for (let y = 0; y < document.body.scrollHeight; y += 800) {
                    window.scrollTo(0, y);
                    await new Promise(resolve => setTimeout(resolve, 120));
                }
            }
            """
        )
        await page.wait_for_timeout(800)
    await page.evaluate("window.scrollTo(0, 0)")
    await page.wait_for_timeout(500)


async def extract_figures(page):
    """Image URL, figcaption, alt text and size for every candidate image."""
    return await page.evaluate(
        """
        () => {
            const results = [];
            const seen = new Set();
            for (const selector of ["figure img", "article img", "main img"]) {
                for (const img of document.querySelectorAll(selector)) {
                    const src = img.currentSrc || img.src ||
                        img.getAttribute("data-src") ||
                        img.getAttribute("data-original") ||
                        img.getAttribute("data-lazy-src");
                    if (!src || seen.has(src)) continue;
                    seen.add(src);

                    const alt = img.getAttribute("alt") || "";
                    const figure = img.closest("figure");
                    let caption = "";
                    if (figure) {
                        const figcaption = figure.querySelector("figcaption");
                        caption = (figcaption ? figcaption.innerText : figure.innerText).trim();
                    }
                    if (!caption && alt) caption = alt.trim();

                    results.push({
                        src, caption, alt,
                        width: img.naturalWidth || img.width || 0,
                        height: img.naturalHeight || img.height || 0,
                    });
                }
            }
            return results;
        }
        """
    )


def useful_image(image: dict) -> bool:
    """Reject site UI images (logos, icons, tiny sprites)."""
    combined = " ".join(
        image.get(k, "").lower() for k in ("src", "alt", "caption")
    )
    if any(word in combined for word in REJECT_WORDS):
        return False
    width, height = image.get("width", 0), image.get("height", 0)
    return not (width and height and width < 150 and height < 100)


async def download_image(context, image_url: str):
    """Fetch through the logged-in browser context (reuses your session)."""
    try:
        response = await context.request.get(image_url, timeout=30_000)
        if not response.ok:
            print(f"      HTTP {response.status}: {image_url}")
            return None, None
        return await response.body(), response.headers.get("content-type", "")
    except Exception as exc:
        print(f"      Download failed: {exc}")
        return None, None


async def process_chapter(context, page, book_base: str, out_dir: Path, chapter_number: int):
    chapter_url = f"{book_base}ch{chapter_number:02d}.html"
    print(f"\n{'=' * 80}\nCHAPTER {chapter_number:02d}\n{chapter_url}\n{'=' * 80}")
    try:
        await page.goto(chapter_url, wait_until="domcontentloaded", timeout=60_000)
    except Exception as exc:
        print(f"Could not open chapter: {exc}")
        return

    await page.wait_for_timeout(CHAPTER_DELAY_MS)
    print(f"  Page title: {await page.title()}")
    await scroll_page(page)

    found = await extract_figures(page)
    images = [image for image in found if useful_image(image)]
    print(f"  Images found: {len(found)}, potential book figures: {len(images)}")

    folder = out_dir / f"chapter_{chapter_number:02d}"
    folder.mkdir(parents=True, exist_ok=True)

    manifest = []
    downloaded_urls = set()
    figure_number = 1

    for image in images:
        image_url = urljoin(page.url, image["src"])
        if image_url in downloaded_urls:
            continue
        downloaded_urls.add(image_url)

        caption = (image.get("caption") or image.get("alt") or "").strip()
        if not caption:
            caption = f"Figure {figure_number}"

        print(f"\n  Figure {figure_number:02d}\n    Description: {caption[:150]}\n    URL: {image_url}")

        content, content_type = await download_image(context, image_url)
        if content is None:
            continue

        extension = get_extension(image_url, content_type)
        base_filename = f"figure_{figure_number:02d}_{clean_filename(caption)}"
        image_filename = base_filename + extension
        image_path = folder / image_filename
        duplicate_index = 2
        while image_path.exists():
            image_filename = f"{base_filename}_{duplicate_index}{extension}"
            image_path = folder / image_filename
            duplicate_index += 1
        image_path.write_bytes(content)

        description_filename = image_path.stem + ".txt"
        (folder / description_filename).write_text(
            f"Chapter: {chapter_number}\n\nFigure: {figure_number}\n\n"
            f"Description:\n{caption}\n\nImage source:\n{image_url}\n\n"
            f"Chapter source:\n{page.url}\n",
            encoding="utf-8",
        )

        manifest.append(
            {
                "chapter": chapter_number,
                "figure": figure_number,
                "image_file": image_filename,
                "description_file": description_filename,
                "caption": caption,
                "alt": image.get("alt", ""),
                "source_url": image_url,
                "chapter_url": page.url,
                "width": image.get("width", 0),
                "height": image.get("height", 0),
                "content_type": content_type,
            }
        )
        print(f"    Saved image: {image_filename}")
        figure_number += 1
        await page.wait_for_timeout(DOWNLOAD_DELAY_MS)

    manifest_path = folder / "figures.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Finished chapter {chapter_number}: {len(manifest)} figures. Manifest: {manifest_path}")


def create_global_manifest(out_dir: Path, chapters: range):
    all_figures = []
    for chapter_number in chapters:
        manifest_path = out_dir / f"chapter_{chapter_number:02d}" / "figures.json"
        if not manifest_path.exists():
            continue
        try:
            all_figures.extend(json.loads(manifest_path.read_text(encoding="utf-8")))
        except Exception as exc:
            print(f"Could not read {manifest_path}: {exc}")
    target = out_dir / "all_figures.json"
    target.write_text(json.dumps(all_figures, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nGlobal manifest: {target}\nTotal downloaded figures: {len(all_figures)}")


async def main(book_base: str, chapters: range, wait_for_enter: bool = False):
    book_id = book_base.rstrip("/").rsplit("/", 1)[-1]
    out_dir = STAGING_DIR / book_id
    out_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=False,
            viewport={"width": 1440, "height": 1000},
        )
        page = context.pages[0] if context.pages else await context.new_page()

        print(f"\n{'=' * 80}\nO'Reilly figure downloader\n{book_base}\n{'=' * 80}")
        await page.goto(f"{book_base}ch{chapters.start:02d}.html", wait_until="domcontentloaded", timeout=60_000)
        await page.wait_for_timeout(2000)
        if wait_for_enter:
            input(
                "\nIf O'Reilly asks you to sign in, do it in the browser window.\n"
                "Make sure the chapter text is visible, then press ENTER here..."
            )
        else:
            await wait_for_login(page, book_base)

        for chapter_number in chapters:
            try:
                await process_chapter(context, page, book_base, out_dir, chapter_number)
            except Exception as exc:
                print(f"\nERROR processing chapter {chapter_number}: {exc}")

        await context.close()

    create_global_manifest(out_dir, chapters)
    print(f"\nDONE. Files are in: {out_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--book-base", required=True, help="Book URL ending in the ISBN and a slash")
    parser.add_argument("--chapters", type=int, required=True, help="Number of chapters (ch01..chNN)")
    parser.add_argument("--start", type=int, default=1, help="First chapter to fetch (default 1)")
    parser.add_argument(
        "--wait-for-enter", action="store_true",
        help="After signing in, press ENTER to start (default: start automatically once the chapter text is detected)",
    )
    args = parser.parse_args()
    base = args.book_base if args.book_base.endswith("/") else args.book_base + "/"
    asyncio.run(main(base, range(args.start, args.chapters + 1), args.wait_for_enter))
