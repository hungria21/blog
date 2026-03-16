from PIL import Image, ImageDraw

def create_wallpaper(path, width=1080, height=2400):
    # Very dark background
    img = Image.new('RGB', (width, height), color='#050505')
    draw = ImageDraw.Draw(img)
    center_x, center_y = width // 2, height // 2
    fist_size = 400
    # Red Fist
    draw.ellipse([center_x - fist_size//2, center_y - fist_size//2,
                  center_x + fist_size//2, center_y + fist_size//2], fill='#D00000')
    # Yellow highlights
    draw.arc([center_x - fist_size//3, center_y - fist_size//3,
              center_x + fist_size//3, center_y + fist_size//3], start=20, end=160, fill='#FFD700', width=15)
    img.save(path, 'JPEG', quality=95)

def create_icon(path, size=192):
    img = Image.new('RGBA', (size, size), color=(10, 10, 10, 255))
    draw = ImageDraw.Draw(img)
    # Circular border (Yellow)
    draw.ellipse([10, 10, size-10, size-10], outline='#FFD700', width=8)
    # Central dot (Red)
    draw.ellipse([size//3, size//3, 2*size//3, 2*size//3], fill='#D00000')
    img.save(path, 'PNG')

if __name__ == "__main__":
    import os
    os.makedirs('opm_dark_theme/wallpaper', exist_ok=True)
    os.makedirs('opm_dark_theme/lockscreen', exist_ok=True)
    os.makedirs('icons_staging/res/drawable-xxhdpi', exist_ok=True)

    create_wallpaper('opm_dark_theme/wallpaper/default_wallpaper.jpg')
    create_wallpaper('opm_dark_theme/lockscreen/default_lock_wallpaper.jpg')

    app_icons = [
        'com.android.settings.png',
        'com.android.browser.png',
        'com.android.camera.png',
        'com.android.contacts.png',
        'com.android.mms.png',
        'com.android.gallery3d.png',
        'com.miui.gallery.png',
        'com.android.calendar.png',
        'com.android.deskclock.png',
        'com.android.calculator2.png',
        'com.android.fileexplorer.png',
        'com.android.email.png'
    ]

    for icon in app_icons:
        create_icon(f'icons_staging/res/drawable-xxhdpi/{icon}')

    print(f"Generated {len(app_icons)} icons and wallpapers.")
