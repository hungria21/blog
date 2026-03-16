import os
import shutil
import zipfile

def zip_dir(dir_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, dir_path)
                zipf.write(abs_path, rel_path)

def build():
    theme_dir = 'opm_dark_theme'
    output_mtz = 'OnePunchMan_Dark_HyperOS.mtz'

    # 1. Zip icons
    print("Packaging icons...")
    zip_dir('icons_staging', os.path.join(theme_dir, 'icons'))

    # 2. Final MTZ
    print("Creating final .mtz package...")
    if os.path.exists(output_mtz):
        os.remove(output_mtz)

    zip_dir(theme_dir, output_mtz)

    size = os.path.getsize(output_mtz)
    print(f"Build complete: {output_mtz} ({size / 1024:.2f} KB)")

if __name__ == "__main__":
    build()
