import os
from PIL import Image

def create_thumbnails():
    # Define paths relative to where the script runs
    source_dir = os.path.join(".", "full")
    target_dir = os.path.join(".", "thumbs")
    
    # Target maximum dimensions for gallery layout thumbnails (4:3 bounding box)
    TARGET_SIZE = (400, 300)
    
    # Create thumbs directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created directory: {target_dir}")

    # Check if full/ directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Could not find '{source_dir}' folder. Make sure to run this script inside your images/gallery/ directory!")
        return

    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    processed_count = 0

    print("Starting batch thumbnail generation...")
    
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(valid_extensions):
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, filename)
            
            try:
                with Image.open(source_path) as img:
                    # Convert to RGB if image is in a profile like RGBA (prevents JPEG errors)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    # .thumbnail() scales down modifying the image in-place while preserving exact aspect ratio
                    img.thumbnail(TARGET_SIZE, Image.Resampling.LANCZOS)
                    
                    # Save with tight web compression optimization (80 quality is indistinguishable at thumbnail scale)
                    img.save(target_path, "JPEG", quality=80, optimize=True)
                    processed_count += 1
                    print(f"✓ Generated thumbnail for: {filename}")
            except Exception as e:
                print(f"✗ Failed to process {filename}: {e}")

    print(f"\n✨ Done! Successfully processed {processed_count} thumbnails into '{target_dir}'.")

if __name__ == "__main__":
    create_thumbnails()