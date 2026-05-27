import colorsys

def hex_to_signed_int(hex_str):
    if hex_str.startswith('#'):
        hex_str = hex_str[1:]
    if len(hex_str) == 6:
        hex_str = 'FF' + hex_str
    val = int(hex_str, 16)
    if val > 0x7FFFFFFF:
        val -= 0x100000000
    return val

def apply_alpha(hex_str, alpha_hex):
    if hex_str.startswith('#'):
        hex_str = hex_str[1:]
    if len(hex_str) == 8:
        hex_str = hex_str[2:]
    return alpha_hex + hex_str

# Material 3 Dark Palette (Blue/Violet based)
M3_DARK_SURFACE = "111318"
M3_DARK_ON_SURFACE = "E2E2E6"
M3_DARK_PRIMARY = "D0BCFF"
M3_DARK_ON_PRIMARY = "381E72"
M3_DARK_PRIMARY_CONTAINER = "4F378B"
M3_DARK_ON_PRIMARY_CONTAINER = "EADDFF"
M3_DARK_SECONDARY = "CCC2DC"
M3_DARK_SECONDARY_CONTAINER = "4A4458"
M3_DARK_SURFACE_VARIANT = "44474E"
M3_DARK_ON_SURFACE_VARIANT = "C4C7D0"
M3_DARK_OUTLINE = "938F99"

LIQUID_ALPHA = "B3" # ~70%

def get_m3_color(key):
    key_lower = key.lower()

    # Special alpha keys
    if "bluralpha" in key_lower:
        return hex_to_signed_int("B2000000")

    # Liquid Glass for Bubbles and panels
    if any(x in key_lower for x in ["bubble", "replypanel", "toppanel"]):
        if "out" in key_lower:
            return hex_to_signed_int(apply_alpha(M3_DARK_PRIMARY_CONTAINER, LIQUID_ALPHA))
        else:
            return hex_to_signed_int(apply_alpha(M3_DARK_SURFACE_VARIANT, LIQUID_ALPHA))

    # Green redirect
    if "green" in key_lower:
        if "text" in key_lower:
            return hex_to_signed_int(M3_DARK_PRIMARY)
        return hex_to_signed_int(M3_DARK_SECONDARY)

    # Backgrounds and containers
    if any(x in key_lower for x in ["background", "window", "wallpaper", "graysection", "divider"]):
        if any(x in key_lower for x in ["text", "icon", "title", "name", "button"]):
             # Fall through to text/icon handling
             pass
        else:
            if "selected" in key_lower or "pressed" in key_lower:
                return hex_to_signed_int(M3_DARK_SECONDARY_CONTAINER)
            return hex_to_signed_int(M3_DARK_SURFACE)

    # Action Bar
    if "actionbar" in key_lower:
        if any(x in key_lower for x in ["title", "item", "icon", "text", "subtitle", "selector"]):
            if "selector" in key_lower:
                return hex_to_signed_int(M3_DARK_SECONDARY_CONTAINER)
            return hex_to_signed_int(M3_DARK_ON_SURFACE)
        return hex_to_signed_int(M3_DARK_SURFACE)

    # Text and Messages
    if any(x in key_lower for x in ["text", "title", "name", "message", "status", "date", "time"]):
        if any(x in key_lower for x in ["blue", "primary", "link", "active", "online"]):
            return hex_to_signed_int(M3_DARK_PRIMARY)
        if any(x in key_lower for x in ["gray", "hint", "subtitle", "secondary", "unactive", "disabled"]):
            return hex_to_signed_int(M3_DARK_ON_SURFACE_VARIANT)
        return hex_to_signed_int(M3_DARK_ON_SURFACE)

    # Checkbox, Radio, Switch, Progress
    if any(x in key_lower for x in ["checkbox", "radio", "switch", "progress", "seekbar"]):
        if any(x in key_lower for x in ["check", "thumb", "inner", "fill", "active"]):
            return hex_to_signed_int(M3_DARK_PRIMARY)
        return hex_to_signed_int(M3_DARK_OUTLINE)

    # Icons and Buttons
    if any(x in key_lower for x in ["icon", "button", "avatar", "selector"]):
        if "pressed" in key_lower or "selected" in key_lower:
            return hex_to_signed_int(M3_DARK_SECONDARY_CONTAINER)
        if "text" in key_lower:
            return hex_to_signed_int(M3_DARK_ON_SURFACE)
        return hex_to_signed_int(M3_DARK_ON_SURFACE_VARIANT)

    # Fallback - distinguish between likely background and likely foreground
    # If it ends in Background, Shadow, or is a known container-like key
    if any(x in key_lower for x in ["shadow", "overlay", "header"]):
        return hex_to_signed_int(M3_DARK_SURFACE)

    return hex_to_signed_int(M3_DARK_ON_SURFACE)

keys_to_process = []
with open('iwDarkRiff_ModoEscuro.attheme', 'r') as f:
    for line in f:
        if '=' in line:
            keys_to_process.append(line.split('=')[0])

with open('Material3_LiquidGlass_Dark.attheme', 'w') as f:
    for key in keys_to_process:
        color = get_m3_color(key)
        f.write(f"{key}={color}\n")

print(f"Generated theme with {len(keys_to_process)} keys.")
