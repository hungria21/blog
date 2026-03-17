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
    src_dir = 'db_theme_src'
    build_dir = 'db_theme_build'
    output_mtz = 'DragonBall_LiquidGlass_v1.2.mtz'

    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)

    # 1. Package icons
    print("Packaging icons module...")
    zip_dir(os.path.join(src_dir, 'icons_res'), os.path.join(build_dir, 'icons'))

    # 2. Package framework-res
    print("Packaging framework-res module...")
    zip_dir(os.path.join(src_dir, 'framework-res'), os.path.join(build_dir, 'framework-res'))

    # 3. Package com.android.systemui
    print("Packaging com.android.systemui module...")
    zip_dir(os.path.join(src_dir, 'com.android.systemui'), os.path.join(build_dir, 'com.android.systemui'))

    # 4. Copy wallpapers and description
    shutil.copytree(os.path.join(src_dir, 'wallpaper'), os.path.join(build_dir, 'wallpaper'))
    shutil.copytree(os.path.join(src_dir, 'lockscreen'), os.path.join(build_dir, 'lockscreen'))
    shutil.copy(os.path.join(src_dir, 'description.xml'), os.path.join(build_dir, 'description.xml'))

    # 5. Final MTZ
    print("Creating final .mtz package...")
    zip_dir(build_dir, output_mtz)

    size = os.path.getsize(output_mtz)
    print(f"Build complete: {output_mtz} ({size / 1024:.2f} KB)")

if __name__ == "__main__":
    build()
