import re

COLORS = {
    'emerald green': '#50C878', 'forest green': '#228B22', 'mint green': '#98FF98', 'sage green': '#9DC183', 'olive green': '#808000', 'green': '#008000',
    'royal blue': '#4169E1', 'navy blue': '#000080', 'sky blue': '#87CEEB', 'baby blue': '#89CFF0', 'indigo': '#4B0082', 'cobalt': '#0047AB', 'blue': '#0000FF',
    'crimson red': '#DC143C', 'ruby red': '#E0115F', 'burgundy': '#800020', 'maroon': '#800000', 'wine red': '#722F37', 'scarlet': '#FF2400', 'red': '#FF0000',
    'pastel pink': '#FFD1DC', 'rose pink': '#FF66CC', 'baby pink': '#F4C2C2', 'blush pink': '#DE5D83', 'fuchsia': '#FF00FF', 'magenta': '#FF0090', 'pink': '#FFC0CB',
    'lavender': '#E6E6FA', 'lilac': '#C8A2C8', 'purple': '#800080', 'violet': '#8F00FF', 'plum': '#8E4585',
    'mustard yellow': '#FFDB58', 'canary yellow': '#FFEF00', 'gold': '#D4AF37', 'metallic gold': '#D4AF37', 'yellow': '#FFFF00',
    'metallic silver': '#C0C0C0', 'silver': '#C0C0C0', 'grey': '#808080', 'charcoal': '#36454F', 'black': '#111111',
    'ivory': '#FFFFF0', 'cream': '#FFFDD0', 'beige': '#F5F5DC', 'white': '#FFFFFF',
    'peach': '#FFE5B4', 'coral': '#FF7F50', 'orange': '#FFA500', 'rust': '#B7410E', 'terracotta': '#E2725B',
    'turquoise': '#40E0D0', 'teal': '#008080', 'cyan': '#00FFFF'
}

test_inputs = [
    'emerald green and gold banarasi saree with peacocks',
    'pastel pink floral dress material with silver embroidery',
    'navy blue and white houndstooth blazer fabric',
    'black and red tartan plaid shirt',
    'yellow polka dots on white summer frock',
    'royal blue velvet sherwani with silver zari',
    'kerala kasavu'
]

for inp in test_inputs:
    low = inp.lower()
    found_colors = []
    for c in sorted(COLORS.keys(), key=lambda x: -len(x)):
        pattern = r'\b' + re.escape(c) + r'\b'
        if re.search(pattern, low):
            found_colors.append(c)
            low = re.sub(pattern, '', low)
    print(f"Input: '{inp}' -> Colors: {found_colors}")
