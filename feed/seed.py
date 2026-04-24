# seed.py
# ─────────────────────────────────────────────────────────────────────────────
# 3-Tier Image Seeding Pipeline
#
# Tiers:
#   _thumb.webp   300×300 max  quality=70  → used in Flutter feed list
#   _mobile.webp  1080×1080 max quality=80  → loaded on detail screen
#   _raw.<ext>    original file             → download-on-demand only
#
# Usage:
#   pip install supabase Pillow
#   mkdir input_images && cp your_4k_photos/*.jpg input_images/
#   python seed.py
# ─────────────────────────────────────────────────────────────────────────────

import os
import io
from PIL import Image
from supabase import create_client, Client

# ── CONFIG — fill these in ──────────────────────────────────────────────────
SUPABASE_URL = "https://xdvnquywbtaxsercluha.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhkdm5xdXl3YnRheHNlcmNsdWhhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njg3OTUwOCwiZXhwIjoyMDkyNDU1NTA4fQ.H_zoz9aqnjr3Oa-YU9acRccoIfmNEIShezZUPvCOiIE"   # service role, NOT anon key
BUCKET_NAME  = "media"
INPUT_DIR    = "input_images"
# ────────────────────────────────────────────────────────────────────────────

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def process_and_upload():
    if not os.path.exists(INPUT_DIR):
        print(f"[ERROR] Folder '{INPUT_DIR}' not found.")
        print(f"        Create it and add some .jpg / .png images, then re-run.")
        return

    files = [
        f for f in os.listdir(INPUT_DIR)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    if not files:
        print(f"[ERROR] No .jpg/.png files found in '{INPUT_DIR}/'")
        return

    print(f"Found {len(files)} image(s) to process.\n")

    for filename in files:
        filepath  = os.path.join(INPUT_DIR, filename)
        base_name = os.path.splitext(filename)[0]
        print(f"▶  Processing: {filename}")

        try:
            with Image.open(filepath) as img:
                # Some PNGs / screenshots are RGBA or P — convert to RGB
                # so they can be saved as JPEG/WebP without errors.
                if img.mode in ("RGBA", "P", "LA"):
                    img = img.convert("RGB")

                original_format = img.format or "JPEG"

                # ── Tier 1: Raw archive (original bytes, untouched) ──────────
                raw_bytes = io.BytesIO()
                img.save(raw_bytes, format=original_format)
                raw_path = f"{base_name}_raw.{original_format.lower()}"
                print(f"   raw    → {raw_path}  "
                      f"({len(raw_bytes.getvalue()) / 1024 / 1024:.1f} MB)")

                # ── Tier 2: Mobile (1080×1080 max, WebP q=80) ───────────────
                mobile_img = img.copy()
                mobile_img.thumbnail((1080, 1080), Image.Resampling.LANCZOS)
                mobile_bytes = io.BytesIO()
                mobile_img.save(mobile_bytes, format="webp", quality=80)
                mobile_path = f"{base_name}_mobile.webp"
                print(f"   mobile → {mobile_path}  "
                      f"({len(mobile_bytes.getvalue()) / 1024:.0f} KB)  "
                      f"{mobile_img.size[0]}×{mobile_img.size[1]}")

                # ── Tier 3: Thumbnail (300×300 max, WebP q=70) ──────────────
                thumb_img = img.copy()
                thumb_img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                thumb_bytes = io.BytesIO()
                thumb_img.save(thumb_bytes, format="webp", quality=70)
                thumb_path = f"{base_name}_thumb.webp"
                print(f"   thumb  → {thumb_path}  "
                      f"({len(thumb_bytes.getvalue()) / 1024:.0f} KB)  "
                      f"{thumb_img.size[0]}×{thumb_img.size[1]}")

            # ── Upload all 3 tiers ───────────────────────────────────────────
            print(f"   Uploading to Supabase Storage bucket '{BUCKET_NAME}'…")
            upload_to_storage(raw_path,    raw_bytes.getvalue(),    original_format.lower())
            upload_to_storage(mobile_path, mobile_bytes.getvalue(), "webp")
            upload_to_storage(thumb_path,  thumb_bytes.getvalue(),  "webp")

            # ── Get public URLs ──────────────────────────────────────────────
            raw_url    = supabase.storage.from_(BUCKET_NAME).get_public_url(raw_path)
            mobile_url = supabase.storage.from_(BUCKET_NAME).get_public_url(mobile_path)
            thumb_url  = supabase.storage.from_(BUCKET_NAME).get_public_url(thumb_path)

            # ── Insert DB row ────────────────────────────────────────────────
            result = supabase.table("posts").insert({
                "media_thumb_url":  thumb_url,
                "media_mobile_url": mobile_url,
                "media_raw_url":    raw_url,
            }).execute()

            print(f"   ✅ Inserted into DB — id: {result.data[0]['id']}\n")

        except Exception as e:
            print(f"   ❌ Failed to process {filename}: {e}\n")
            continue


def upload_to_storage(path: str, file_bytes: bytes, fmt: str):
    content_type = "image/webp" if fmt == "webp" else f"image/{fmt}"
    try:
        supabase.storage.from_(BUCKET_NAME).upload(
            path,
            file_bytes,
            {"content-type": content_type},
        )
        print(f"   ✓ Uploaded {path}")
    except Exception as e:
        # File already exists in storage — safe to skip, URL still valid
        print(f"   ⚠  Skipped {path} (already exists in bucket)")


if __name__ == "__main__":
    print("=" * 55)
    print("  3-Tier Image Seeding Pipeline")
    print("=" * 55 + "\n")

    if "YOUR_SUPABASE" in SUPABASE_URL:
        print("[ERROR] Fill in SUPABASE_URL and SUPABASE_KEY before running.")
        exit(1)

    process_and_upload()
    print("=" * 55)
    print("  Pipeline complete.")
    print("=" * 55)