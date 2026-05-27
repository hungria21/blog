import colorsys

def int_to_argb(val):
    if val < 0:
        val += 0x100000000
    return (val >> 24) & 0xFF, (val >> 16) & 0xFF, (val >> 8) & 0xFF, val & 0xFF

def is_green(r, g, b):
    # Convert to HSV to check hue
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    hue_degrees = h * 360.0
    # Green is typically between 80 and 160 degrees
    # Low saturation/value might be neutral, but we want to be strict if hue is in green range
    if 80 <= hue_degrees <= 160 and s > 0.1 and v > 0.1:
        return True
    return False

def verify():
    original_keys = []
    with open('iwDarkRiff_ModoEscuro.attheme', 'r') as f:
        for line in f:
            if '=' in line:
                original_keys.append(line.split('=')[0])

    new_keys = {}
    with open('Material3_LiquidGlass_Dark.attheme', 'r') as f:
        for line in f:
            if '=' in line:
                k, v = line.strip().split('=')
                new_keys[k] = int(v)

    # Check key count
    if len(original_keys) != len(new_keys):
        print(f"Error: Key count mismatch. Expected {len(original_keys)}, got {len(new_keys)}")
        return False

    # Check for green colors and signed 32-bit range
    for k, v in new_keys.items():
        if not (-2147483648 <= v <= 2147483647):
            print(f"Error: {k} has value {v} outside signed 32-bit range")
            return False

        a, r, g, b = int_to_argb(v)
        if is_green(r, g, b):
            print(f"Error: {k} has green color (A={a}, R={r}, G={g}, B={b})")
            return False

    print("Verification successful: 646 keys, no green colors, all valid signed 32-bit integers.")
    return True

if __name__ == "__main__":
    import sys
    if not verify():
        sys.exit(1)
