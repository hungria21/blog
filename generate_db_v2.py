from PIL import Image, ImageDraw

def create_db_wallpaper(path, width=1080, height=2400):
    # Dark orange gradient simulation
    img = Image.new('RGB', (width, height), color='#0A0500')
    draw = ImageDraw.Draw(img)
    center_x, center_y = width // 2, height // 2

    # Large Dragon Ball glow
    for s in range(600, 400, -10):
        alpha = int((600-s)/200 * 255)
        draw.ellipse([center_x - s//2, center_y - s//2, center_x + s//2, center_y + s//2], fill='#FF4500')

    # Dragon Ball
    draw.ellipse([center_x - 200, center_y - 200, center_x + 200, center_y + 200], fill='#FF8C00', outline='#E67E22', width=8)

    # 4 Stars
    star_size = 35
    stars = [(0, -80), (0, 80), (-80, 0), (80, 0)]
    for sx, sy in stars:
        px, py = center_x + sx, center_y + sy
        draw.polygon([(px, py-star_size), (px+star_size*0.4, py-star_size*0.4), (px+star_size, py),
                      (px+star_size*0.4, py+star_size*0.4), (px, py+star_size), (px-star_size*0.4, py+star_size*0.4),
                      (px-star_size, py), (px-star_size*0.4, py-star_size*0.4)], fill='#D00000')

    img.save(path, 'JPEG', quality=95)

def draw_icon_shape(draw, shape, size):
    mid = size // 2
    pad = size // 4
    if shape == 'gear': # Settings
        draw.ellipse([pad, pad, size-pad, size-pad], outline='#FFD700', width=10)
        for i in range(8):
            import math
            angle = i * (math.pi/4)
            x = mid + (mid-pad+10) * math.cos(angle)
            y = mid + (mid-pad+10) * math.sin(angle)
            draw.rectangle([x-10, y-10, x+10, y+10], fill='#FFD700')
    elif shape == 'globe': # Browser
        draw.ellipse([pad, pad, size-pad, size-pad], outline='#FFD700', width=8)
        draw.line([mid, pad, mid, size-pad], fill='#FFD700', width=4)
        draw.line([pad, mid, size-pad, mid], fill='#FFD700', width=4)
    elif shape == 'camera':
        draw.rectangle([pad, pad+20, size-pad, size-pad], outline='#FFD700', width=8)
        draw.ellipse([mid-30, mid-10, mid+30, mid+50], outline='#FFD700', width=6)
    else: # Default Star
        draw.polygon([(mid, pad), (mid+20, mid-20), (size-pad, mid), (mid+20, mid+20), (mid, size-pad), (mid-20, mid+20), (pad, mid), (mid-20, mid-20)], fill='#FFD700')

def create_themed_icon(path, shape, size=192):
    img = Image.new('RGBA', (size, size), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    # Glassy background
    draw.ellipse([5, 5, size-5, size-5], fill=(255, 255, 255, 30), outline=(255, 255, 255, 80), width=4)
    draw_icon_shape(draw, shape, size)
    img.save(path, 'PNG')

if __name__ == "__main__":
    create_db_wallpaper('db_theme_src/wallpaper/default_wallpaper.jpg')
    create_db_wallpaper('db_theme_src/lockscreen/default_lock_wallpaper.jpg')

    apps = {
        'com.android.settings': 'gear',
        'com.android.browser': 'globe',
        'com.android.camera': 'camera',
        'com.android.contacts': 'star',
        'com.android.mms': 'star',
        'com.miui.gallery': 'star',
        'com.android.calendar': 'star',
        'com.android.deskclock': 'star',
        'com.android.calculator2': 'star',
        'com.android.fileexplorer': 'star',
        'com.android.email': 'star'
    }

    for pkg, shape in apps.items():
        create_themed_icon(f'db_theme_src/icons_res/res/drawable-xxhdpi/{pkg}.png', shape)

    print("Icons and Wallpapers generated with vector-like shapes.")
