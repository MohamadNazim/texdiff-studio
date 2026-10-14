import re
import random
import difflib
import chromadb
from sentence_transformers import SentenceTransformer

# ==============================================================================
# 1. COMPREHENSIVE FASHION COLOR TAXONOMY (70+ Exact Colors & Hex Codes)
# ==============================================================================
FASHION_COLORS = {
    # Jewel & Forest Greens
    "emerald green": "#50C878", "forest green": "#228B22", "mint green": "#98FF98",
    "sage green": "#9DC183", "olive green": "#808000", "bottle green": "#006A4E",
    "jade green": "#00A86B", "lime green": "#32CD32", "green": "#008000", "olive": "#808000",
    "mint": "#98FF98", "sage": "#9DC183",

    # Royal, Sapphire & Navy Blues
    "royal blue": "#4169E1", "navy blue": "#000080", "sky blue": "#87CEEB",
    "baby blue": "#89CFF0", "peacock blue": "#005F73", "midnight blue": "#191970",
    "cobalt blue": "#0047AB", "indigo": "#4B0082", "cobalt": "#0047AB",
    "turquoise": "#40E0D0", "teal": "#008080", "cyan": "#00FFFF", "blue": "#0000FF",
    "navy": "#000080",

    # Crimson, Scarlet, Wine & Ruby Reds
    "crimson red": "#DC143C", "ruby red": "#E0115F", "wine red": "#722F37",
    "scarlet red": "#FF2400", "burgundy": "#800020", "maroon": "#800000",
    "crimson": "#DC143C", "ruby": "#E0115F", "scarlet": "#FF2400", "red": "#FF0000",
    "rust": "#B7410E", "terracotta": "#E2725B",

    # Pinks, Corals & Purples
    "pastel pink": "#FFD1DC", "rose pink": "#FF66CC", "baby pink": "#F4C2C2",
    "blush pink": "#DE5D83", "hot pink": "#FF69B4", "magenta": "#FF0090",
    "fuchsia": "#FF00FF", "pink": "#FFC0CB", "rose": "#FF007F",
    "coral": "#FF7F50", "peach": "#FFE5B4",
    "lavender": "#E6E6FA", "lilac": "#C8A2C8", "plum": "#8E4585",
    "violet": "#8F00FF", "purple": "#800080",

    # Metallics, Golds & Yellows
    "metallic gold": "#D4AF37", "rose gold": "#B76E79", "champagne gold": "#F7E7CE",
    "gold": "#D4AF37", "mustard yellow": "#FFDB58", "canary yellow": "#FFEF00",
    "lemon yellow": "#FFF44F", "ochre": "#CC7722", "amber": "#FFBF00",
    "mustard": "#FFDB58", "yellow": "#FFFF00", "orange": "#FFA500",

    # Monochromes & Neutrals
    "metallic silver": "#C0C0C0", "silver": "#C0C0C0",
    "jet black": "#0A0A0A", "charcoal grey": "#36454F", "black": "#111111",
    "charcoal": "#36454F", "grey": "#808080", "gray": "#808080",
    "ivory white": "#FFFFF0", "kora cream": "#FFFDD0", "cream": "#FFFDD0",
    "ivory": "#FFFFF0", "beige": "#F5F5DC", "white": "#FFFFFF",
    "bronze": "#CD7F32", "copper": "#B87333", "tan": "#D2B48C", "brown": "#964B00"
}

# ==============================================================================
# 2. FASHION ATTIRE & GARMENT TAXONOMY
# ==============================================================================
ATTIRE_TYPES = {
    # Indian / South Asian Traditional
    "saree": "royal silk saree with ornamental border",
    "sari": "royal silk saree with ornamental border",
    "lehenga": "flared royal bridal lehenga",
    "dupatta": "sheer embellished dupatta veil",
    "kurta": "bespoke tailored kurta ensemble",
    "kurti": "chic tailored kurti tunic",
    "sherwani": "regal brocade ceremonial sherwani",
    "nehru jacket": "structured tailored Nehru jacket",
    "anarkali": "regal floor-length flared anarkali",
    "mundu": "traditional kasavu handloom mundu drape",
    "dhoti": "traditional handloom dhoti",
    "salwar": "traditional embroidered salwar suit",

    # Western Haute Couture & Tailored Wear
    "evening gown": "haute couture red-carpet evening gown",
    "ballgown": "regal dramatic ballgown",
    "cocktail dress": "sophisticated cocktail dress",
    "dress": "bespoke designer fashion dress",
    "frock": "chic flared summer frock",
    "blazer": "bespoke tailored luxury blazer",
    "suit": "impeccably tailored luxury suit",
    "tuxedo": "black-tie ceremonial tuxedo",
    "jacket": "structured designer jacket",
    "coat": "luxurious outerwear coat",
    "skirt": "flowing designer flared skirt",
    "blouse": "embroidered couture blouse",
    "shirt": "crisp tailored button-down shirt",
    "trousers": "bespoke tailored trousers",
    "pants": "tailored high-fashion pants",

    # Global Traditional & Resort
    "kimono": "traditional Japanese silk kimono",
    "yukata": "crisp Japanese summer yukata",
    "kaftan": "luxurious flowing silk kaftan",
    "tunic": "effortless chic relaxed tunic",
    "scarf": "luxurious silk twill fashion scarf",
    "shawl": "fine woven ceremonial heirloom shawl"
}

# ==============================================================================
# 3. TEXTILE DESIGN PATTERNS & MOTIFS
# ==============================================================================
DESIGN_PATTERNS = {
    # Florals & Botanicals
    "floral": "lush blossoming botanical flowers and delicate vine stems",
    "botanical": "intricate naturalist botanical leaves, flora, and stems",
    "lotus": "sacred blooming lotus rosettes and lily buds",
    "rose": "romantic full-bloom English roses and thorny vine foliage",
    "jasmine": "delicate star-shaped jasmine blossoms and leafy sprigs",
    "cherry blossom": "floating sakura cherry blossom petals and branches",
    "peony": "grand imperial blooming peony blossoms",
    "sunflower": "radiant blooming sunflower heads",
    "chinar": "iconic serrated Kashmiri Chinar leaf foliage",
    "tree of life": "intricate flowering Tree of Life botanical meanders",

    # Geometrics & Checks
    "houndstooth": "sharp two-tone broken geometric houndstooth twill checks",
    "polka dots": "balanced rhythmic circular polka dot motifs",
    "dots": "delicate micro-dot pinhead dots",
    "stripes": "crisp clean parallel linear orthogonal stripes",
    "striped": "bold contrasting rhythmic parallel stripes",
    "pinstripe": "refined executive ultra-fine pinstripes",
    "checks": "orthogonal grid matrix windowpane checks",
    "checkered": "crisp orthogonal alternating checkerboard squares",
    "plaid": "rich multi-color crossed orthogonal twill plaid",
    "tartan": "authentic Scottish Highland sett twill tartan banding",
    "chevron": "dynamic 45-degree zig-zag chevron herringbone weave",
    "herringbone": "subtle broken twill V-shaped herringbone weave",
    "geometric": "crisp interlocking mathematical geometric polygon shapes",
    "diamonds": "stepped diamond lozenge tessellations",

    # Historic & Luxury Archetypes
    "paisley": "ornate curving teardrop Boteh paisley motifs with fine flourishes",
    "damask": "luxurious tonal reversible jacquard damask acanthus foliage",
    "brocade": "raised metallic zari threadwork embossed brocade",
    "jacquard": "richly textured supplementary weft jacquard weave",
    "medallion": "staggered ornamental circular filigree medallions",
    "arabesque": "flowing interlaced curvilinear Islamic arabesque foliage",
    "ikat": "distinctive feathered tie-dye blurred-edge ikat bands",
    "bandhani": "delicate resist-dyed diamond-grouped micro-ringlet dots",
    "batik": "hand-drawn wax-resist canting crackle batik veining",
    "tie-dye": "vibrant radial spiral bleed tie-dye gradients",
    "abstract": "modernist expressive fluid abstract shapes",
    "art deco": "opulent 1920s geometric fans, sunbursts, and brass arches",
    "baroque": "dramatic gilded acanthus scrollwork and palmette leaves",
    "vintage": "nostalgic heirloom antique filigree engraving",
    "animal print": "bold naturalistic animal spot texture",
    "leopard": "stylized naturalistic leopard rosette spots",
    "zebra": "flowing organic wavy monochrome zebra stripes"
}

# Specific Motifs
SPECIFIC_MOTIFS = {
    "peacock": "majestic Mayil peacocks with fan-tail plumes and crowned heads",
    "swan": "graceful Annapakshi sacred swans with curving necks",
    "elephant": "royal ceremonial caparisoned elephants (Hathi)",
    "parrot": "vibrant jewel-eyed parrots (Popat) perched on flowering branches",
    "dragon": "imperial coiled serpentine Asian dragons with auspicious clouds",
    "butterfly": "ethereal fluttering butterflies with filigree wing patterns",
    "fish": "sacred Matsya fish twin motifs swimming through water ripples",
    "stars": "brilliant 8-point geometric star rosettes",
    "waves": "cresting rhythmic Seigaiha ocean arch waves"
}

# ==============================================================================
# 4. ENCYCLOPEDIC CULTURAL REGIONS (Invoked ONLY when culturally requested)
# ==============================================================================
CULTURAL_REGIONS = {
    "kerala": {
        "style": "Kerala Royal Kasavu & Karalkada",
        "origin": "Kerala, India",
        "technique": "sacred temple kasavu gold zari borders, delicate Mayil peacock and Kara temple spire motifs",
        "fabric": "pristine unbleached kora cream cotton with brilliant pure metallic gold kasavu thread",
        "default_palette": ["#FFFDF0", "#D4AF37", "#AA7A1E", "#332211"],
        "triggers": ["kerala", "kasavu", "karalkada", "mundu", "onam"]
    },
    "tamil nadu": {
        "style": "Kanchipuram Zari Brocade",
        "origin": "Tamil Nadu, India",
        "technique": "Mayil peacock medallions, Annapakshi sacred swans, Thazhampoo temple spires, Rudraksha and mango paisley butas",
        "fabric": "heavyweight Mulberry silk with lustrous twisted 3-ply gold zari brocade",
        "default_palette": ["#800020", "#D4AF37", "#1B4D3E", "#4A0E17"],
        "triggers": ["tamil nadu", "tamil", "kanchipuram", "kanchi", "madurai", "sungudi", "chettinad", "kandangi"]
    },
    "uttar pradesh": {
        "style": "Royal Banarasi Katan Silk Brocade",
        "origin": "Varanasi / Banaras, Uttar Pradesh",
        "technique": "intricate gold and silver zari floral jaal, Shikargah hunting motifs, Kalga paisley medallions, Bel foliage vines",
        "fabric": "pure hand-spun Katan silk with rich brocade meenakari detailing",
        "default_palette": ["#800020", "#D4AF37", "#9E1B32", "#E5C07B"],
        "triggers": ["banaras", "banarasi", "varanasi", "uttar pradesh", "chikankari", "lucknow", "katan silk"]
    },
    "kashmir": {
        "style": "Kashmir Royal Jamawar & Kani Weave",
        "origin": "Kashmir, India",
        "technique": "ornate Boteh paisley ambi motifs, dense swirling Chinar leaf foliage, intricate Kani shawl needlework arabesques",
        "fabric": "luxurious fine woven Pashmina wool with vibrant jewel-tone floral threadwork",
        "default_palette": ["#0F2042", "#C84B31", "#E4A951", "#2D4263"],
        "triggers": ["kashmir", "kashmiri", "jamawar", "kani", "pashmina", "sozni", "tilla"]
    },
    "odisha": {
        "style": "Odisha Sambalpuri Bandha Ikat",
        "origin": "Odisha, India",
        "technique": "traditional Shankha conch shell, sacred lotus, Chakra wheel motifs, Bomkai temple spire borders",
        "fabric": "handwoven tie-dye resist silk with feathered micro-warp threads",
        "default_palette": ["#9A1F26", "#D9822B", "#1C1C1C", "#F4EBD9"],
        "triggers": ["odisha", "orissa", "sambalpuri", "bomkai", "pasapalli", "bandha"]
    },
    "west bengal": {
        "style": "Bengal Baluchari & Jamdani Silk",
        "origin": "West Bengal, India",
        "technique": "intricate royal court procession scenes, stylized floral kalka butidar sprigs, geometric Jamdani muslin weave",
        "fabric": "sheer fine muslin and rich Murshidabad silk with supplementary weft patterning",
        "default_palette": ["#7B1113", "#C59B27", "#1E3F20", "#FBF5E8"],
        "triggers": ["bengal", "west bengal", "baluchari", "jamdani", "kantha", "dhakai"]
    },
    "gujarat": {
        "style": "Gujarat Patan Patola & Bandhani",
        "origin": "Gujarat, India",
        "technique": "Patan Patola double ikat geometric elephants (Hathi), parrots (Popat), 8-point stars, Bandhani resist micro-dots",
        "fabric": "pure mulberry silk with double-resist tie-dye and vibrant natural dyes",
        "default_palette": ["#A81C24", "#FFC300", "#1E1E1E", "#FFFFFF"],
        "triggers": ["gujarat", "gujarati", "patola", "patan", "bandhani", "ajrakh", "kutch", "ashavali"]
    },
    "rajasthan": {
        "style": "Jaipur Sanganeri & Leheriya Block Print",
        "origin": "Rajasthan, India",
        "technique": "delicate floral butis, poppy and iris flowers with curving stems, Leheriya diagonal ripple waves",
        "fabric": "crisp white sheer mulmul cotton with natural herbal dyes",
        "default_palette": ["#E8D8C8", "#B83B5E", "#50675B", "#F08A5D"],
        "triggers": ["rajasthan", "rajasthani", "jaipur", "sanganeri", "bagru", "leheriya", "dabu", "jodhpur"]
    },
    "punjab": {
        "style": "Punjab Royal Phulkari & Bagh",
        "origin": "Punjab, India",
        "technique": "vibrant geometric silk floss embroidery, interlocking diamond Bagh flower gardens, triangular Chevron sunbursts",
        "fabric": "coarse hand-spun khaddar cotton base with heavy sheen pat silk floss stitchwork",
        "default_palette": ["#E63946", "#F4A261", "#E76F51", "#2A9D8F"],
        "triggers": ["punjab", "punjabi", "phulkari", "bagh", "amritsar"]
    },
    "andhra pradesh": {
        "style": "Andhra Srikalahasti Kalamkari",
        "origin": "Andhra Pradesh, India",
        "technique": "sacred blooming lotus flowers, tree of life, flowing botanical vines jaal, peacocks, fine black bamboo pen outlines",
        "fabric": "unbleached ecru linen dyed with natural madder root, indigo, and myrobalan",
        "default_palette": ["#8C2D19", "#1A2B4C", "#C8963E", "#EFE8DA"],
        "triggers": ["andhra", "andhra pradesh", "kalamkari", "srikalahasti", "machilipatnam"]
    },
    "japan": {
        "style": "Japanese Kyoto Yuzen & Seigaiha",
        "origin": "Kyoto, Japan",
        "technique": "flowing Seigaiha ocean crest waves, delicate floating Sakura cherry blossoms, Asanoha geometric hemp leaf",
        "fabric": "pure crepe silk (Chirimen) with fine gold-leaf paste (Kindei) and indigo dye",
        "default_palette": ["#1B3B6F", "#FAD2E1", "#D4AF37", "#111625"],
        "triggers": ["japan", "japanese", "yuzen", "seigaiha", "sakura", "shibori", "kyoto", "tokyo", "ukiyo-e"]
    },
    "indonesia": {
        "style": "Indonesian Javanese Royal Batik",
        "origin": "Java, Indonesia",
        "technique": "Batik Parang diagonal dagger blades, Kawung four-petal circular geometry, Mega Mendung billowing cloud formations",
        "fabric": "fine cambric cotton with natural beeswax resist dye and soga brown tree-bark dyes",
        "default_palette": ["#4A2E18", "#C8963E", "#1B2A4A", "#F4EBD9"],
        "triggers": ["indonesia", "indonesian", "batik", "parang", "kawung", "java", "javanese", "bali"]
    },
    "morocco": {
        "style": "Moroccan Zellige & Fez Mosaic",
        "origin": "Marrakech / Fez, Morocco",
        "technique": "complex 16-point interlocking star geometric tessellations, Moorish arabesque archways, Berber tribal diamond talismans",
        "fabric": "glazed ceramic tile symmetry and woven flat-weave kilim wool textures",
        "default_palette": ["#0F4C81", "#E07A5F", "#2A9D8F", "#F4F1DE"],
        "triggers": ["morocco", "moroccan", "zellige", "marrakech", "fez", "moorish"]
    },
    "scotland": {
        "style": "Scottish Highland Tartan Sett",
        "origin": "Highlands, Scotland",
        "technique": "authentic Highland clan sett orthogonal intersecting color bands, 2/2 twill diagonal ribbing",
        "fabric": "pure worsted sheep wool with saturated yarn-dyed orthogonal symmetry",
        "default_palette": ["#00246B", "#0B6623", "#C00000", "#FFD700"],
        "triggers": ["scotland", "scottish", "tartan", "plaid", "highland", "kilt"]
    },
    "france": {
        "style": "French Lyon Toile de Jouy & Silk",
        "origin": "Versailles / Lyon, France",
        "technique": "fine monochromatic pastoral toile engravings, romantic Rococo floral garlands, ribbon bow swags",
        "fabric": "crisp unbleached percale cotton and lustrous Lyon lampas silk brocade",
        "default_palette": ["#1A2A6C", "#F4F1DE", "#B21F1F", "#FDBB2D"],
        "triggers": ["france", "french", "toile", "toile de jouy", "lyon", "rococo", "versailles"]
    },
    "italy": {
        "style": "Venetian Baroque Silk Damask",
        "origin": "Venice, Italy",
        "technique": "sculptural acanthus leaf volutes, scalloped artichoke medallions, imperial palmettes",
        "fabric": "heavyweight silk velvet and gold lurex figured brocade jacquard",
        "default_palette": ["#4A0E17", "#D4AF37", "#1E2A38", "#E6DFD5"],
        "triggers": ["italy", "italian", "venetian", "venice", "damask", "baroque", "florence"]
    },
    "mexico": {
        "style": "Mexican Otomi Tenango Embroidery",
        "origin": "Hidalgo / Oaxaca, Mexico",
        "technique": "vibrant hand-embroidered silhouette animals, stylized roosters, deer, peacocks, native wildflowers",
        "fabric": "natural rustic manta cotton with dense satin-stitch multi-color threads",
        "default_palette": ["#FF0055", "#00CCFF", "#FFCC00", "#00FF66"],
        "triggers": ["mexico", "mexican", "otomi", "tenango", "talavera", "oaxaca"]
    },
    "west africa": {
        "style": "West African Royal Kente Strip Weave",
        "origin": "Ghana / West Africa",
        "technique": "sacred geometric chevron lozenge strips, zigzag warp stripes, symbolic royal checkerboards",
        "fabric": "heavy interlocked rayon-silk strip-woven narrow bands",
        "default_palette": ["#FFD700", "#008000", "#FF0000", "#000080"],
        "triggers": ["africa", "african", "kente", "ghana", "ankara", "adinkra"]
    }
}

# ==============================================================================
# 5. COMPOSITIONAL LAYOUT VARIATIONS (Guarantees Infinite Diversity)
# ==============================================================================
COMPOSITION_LAYOUTS = [
    "allover jaal continuous trailing floral lattice vine repeat",
    "staggered half-drop medallion roundel repeat",
    "dynamic diagonal 45-degree chevron grid layout",
    "spaced butidar floating sprig spot motif repeat",
    "serpentine S-curve undulating vine meander",
    "interlocking geometric matrix tile repeat",
    "stepped drop-repeat featuring rhythmic alternating motif clusters"
]


class FashionPromptParser:
    """
    Intelligent NLP Parser that extracts:
    - User's exact requested colors (multi-word and single-word)
    - User's exact requested attire/garment context
    - User's exact requested pattern styles and motifs
    - Explicit cultural heritage (if directly requested by user)
    """
    @staticmethod
    def parse(user_input: str) -> dict:
        raw = user_input.strip()
        low = f" {raw.lower()} "

        # 1. Extract Colors (Multi-word matches prioritized)
        found_colors = []
        found_hexes = []
        # Sort colors by length descending so "emerald green" matches before "green"
        for color_name in sorted(FASHION_COLORS.keys(), key=lambda x: -len(x)):
            pattern = r"(?<!\w)" + re.escape(color_name) + r"(?!\w)"
            if re.search(pattern, low):
                found_colors.append(color_name)
                found_hexes.append(FASHION_COLORS[color_name])
                low = re.sub(pattern, " ", low)

        # 2. Extract Attire Types
        found_attire = []
        attire_description = ""
        for attire_kw, desc in sorted(ATTIRE_TYPES.items(), key=lambda x: -len(x[0])):
            pattern = r"(?<!\w)" + re.escape(attire_kw) + r"(?!\w)"
            if re.search(pattern, low):
                found_attire.append(attire_kw)
                if not attire_description:
                    attire_description = desc
                low = re.sub(pattern, " ", low)

        # 3. Extract Design Patterns & Motifs
        found_styles = []
        style_descriptions = []
        for style_kw, desc in sorted(DESIGN_PATTERNS.items(), key=lambda x: -len(x[0])):
            pattern = r"(?<!\w)" + re.escape(style_kw) + r"(?!\w)"
            if re.search(pattern, low):
                found_styles.append(style_kw)
                style_descriptions.append(desc)
                low = re.sub(pattern, " ", low)

        # 4. Extract Specific Motifs (Peacock, Swan, Lotus, etc.)
        found_motifs = []
        motif_descriptions = []
        for motif_kw, desc in sorted(SPECIFIC_MOTIFS.items(), key=lambda x: -len(x[0])):
            pattern = r"(?<!\w)" + re.escape(motif_kw) + r"(?!\w)"
            if re.search(pattern, low):
                found_motifs.append(motif_kw)
                motif_descriptions.append(desc)
                low = re.sub(pattern, " ", low)

        # 5. Extract Cultural Heritage (ONLY when explicit triggers are present)
        matched_region = None
        for reg_id, data in CULTURAL_REGIONS.items():
            for trig in data["triggers"]:
                pattern = r"(?<!\w)" + re.escape(trig) + r"(?!\w)"
                if re.search(pattern, f" {raw.lower()} "):
                    matched_region = data
                    break
            if matched_region:
                break

        # Remaining residual keywords
        cleaned_residuals = re.sub(r"[^a-zA-Z0-9\s]", " ", low).split()
        stop_words = {
            "a", "an", "the", "in", "on", "of", "with", "and", "or", "for", "to",
            "pattern", "fabric", "textile", "print", "swatch", "tile", "seamless",
            "repeat", "surface", "design", "style", "texture", "make", "create",
            "draw", "generate", "render", "give", "me", "show", "material", "cloth"
        }
        residual_tokens = [w for w in cleaned_residuals if w not in stop_words and len(w) > 2]

        return {
            "raw_input": raw,
            "colors": found_colors,
            "hexes": found_hexes,
            "attire": found_attire,
            "attire_desc": attire_description,
            "styles": found_styles,
            "style_descs": style_descriptions,
            "motifs": found_motifs,
            "motif_descs": motif_descriptions,
            "cultural_region": matched_region,
            "residuals": residual_tokens
        }


class TextileMotifStore:
    """
    Universal Textile CAD Knowledge & Prompt Engineering Engine.
    Strictly prioritizes the user's requested colors, style, attire, and motifs,
    while guaranteeing pristine 2D orthogonal CAD repeat tiles with zero human figures or cloth folds.
    """
    def __init__(self, collection_name: str = "textile_motifs_v6"):
        self.client = chromadb.Client()
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self._seed_database()

    def _seed_database(self):
        if self.collection.count() >= len(CULTURAL_REGIONS):
            return
        ids, docs, metas = [], [], []
        for reg_id, data in CULTURAL_REGIONS.items():
            doc_text = f"{reg_id} {data['style']} {data['origin']} {data['technique']} {data['fabric']} {' '.join(data['triggers'])}"
            ids.append(f"reg_{reg_id}")
            docs.append(doc_text)
            metas.append({
                "region_id": reg_id,
                "style": data["style"],
                "origin": data["origin"],
                "technique": data["technique"],
                "fabric": data["fabric"],
                "palette": ", ".join(data["default_palette"])
            })
        embeddings = self.encoder.encode(docs).tolist()
        self.collection.add(ids=ids, documents=docs, metadatas=metas, embeddings=embeddings)

    def auto_expand_prompt(self, user_query: str, variation_index: int = None) -> dict:
        """
        Synthesizes a production CAD prompt where:
        1. User's exact colors, styles, attire, and motifs are placed in TOKENS 1-20 (maximum CLIP attention).
        2. Cultural weaving techniques are seamlessly incorporated if requested.
        3. Strict negative prompt eliminates all humans, garments, 3D folds, and wrinkles.
        4. Dynamic layout variation produces infinite unique generations for repeated inputs.
        """
        raw_query = user_query.strip() if user_query else "Royal Brocade"
        parsed = FashionPromptParser.parse(raw_query)

        # Select dynamic compositional layout
        if variation_index is not None:
            layout = COMPOSITION_LAYOUTS[variation_index % len(COMPOSITION_LAYOUTS)]
        else:
            layout = random.choice(COMPOSITION_LAYOUTS)

        # Strict Anti-Defect Negative Prompt
        strict_negative = (
            "human, person, woman, man, face, body, limbs, realistic model, photo of dress, "
            "3D perspective, folded fabric, wrinkles, cloth folds, ripples, crease, shadows, "
            "mannequin, garment mockup, depth of field, blurry edges, distorted lines, low quality"
        )

        # -------------------------------------------------------------
        # STEP 1: CONSTRUCT USER COLOR SPECIFICATION
        # -------------------------------------------------------------
        if parsed["colors"]:
            if len(parsed["colors"]) == 1:
                color_phrase = f"{parsed['colors'][0]}"
            elif len(parsed["colors"]) == 2:
                color_phrase = f"{parsed['colors'][0]} and {parsed['colors'][1]}"
            else:
                color_phrase = f"{', '.join(parsed['colors'][:-1])} and {parsed['colors'][-1]}"
            palette_hexes = parsed["hexes"]
            # Pad palette with neutral or accent if under 4 swatches
            while len(palette_hexes) < 4:
                palette_hexes.append("#D4AF37" if "#D4AF37" not in palette_hexes else "#111111")
        else:
            # If no colors specified by user, check cultural region or default
            if parsed["cultural_region"]:
                palette_hexes = parsed["cultural_region"]["default_palette"]
                color_phrase = ""
            else:
                color_phrase = "luxurious rich palette"
                palette_hexes = ["#D4AF37", "#800020", "#1B4D3E", "#0A192F"]

        # -------------------------------------------------------------
        # STEP 2: CONSTRUCT CORE DESIGN & MOTIF SPECIFICATION
        # -------------------------------------------------------------
        core_elements = []
        if color_phrase:
            core_elements.append(color_phrase)

        # Add explicit motifs (peacock, swan, lotus, etc.)
        if parsed["motif_descs"]:
            core_elements.append(parsed["motif_descs"][0])
        elif parsed["motifs"]:
            core_elements.append(f"{' and '.join(parsed['motifs'])} motifs")

        # Add design pattern/style (floral, houndstooth, polka dots, damask, etc.)
        if parsed["style_descs"]:
            core_elements.append(parsed["style_descs"][0])
        elif parsed["styles"]:
            core_elements.append(f"{' and '.join(parsed['styles'])} pattern")

        # If user didn't mention specific styles or motifs, use residual words or default
        if not parsed["motifs"] and not parsed["styles"]:
            if parsed["residuals"]:
                core_elements.append(f"{' '.join(parsed['residuals'])} pattern")
            elif not parsed["cultural_region"]:
                core_elements.append("intricate damask filigree pattern")

        core_subject = ", ".join(core_elements)

        # -------------------------------------------------------------
        # STEP 3: CONSTRUCT ATTIRE & FABRIC CONTEXT
        # -------------------------------------------------------------
        if parsed["attire_desc"]:
            attire_context = f"for {parsed['attire_desc']}"
        elif parsed["attire"]:
            attire_context = f"for bespoke {parsed['attire'][0]}"
        else:
            attire_context = "for bespoke haute couture fashion"

        # -------------------------------------------------------------
        # STEP 4: WEAVE IN CULTURAL TECHNIQUE (IF APPLICABLE)
        # -------------------------------------------------------------
        if parsed["cultural_region"]:
            reg = parsed["cultural_region"]
            matched_style = reg["style"]
            origin = reg["origin"]
            technique = reg["technique"]
            fabric = reg["fabric"]
            cultural_clause = f", authentic {reg['style']} {technique}, woven on {fabric}"
        else:
            matched_style = f"Haute Couture ({raw_query.title()})"
            origin = "Custom Atelier Studio"
            cultural_clause = ", fine textile weave texture"

        # -------------------------------------------------------------
        # STEP 5: ASSEMBLE 2D FLAT CAD SURFACE PROMPT
        # -------------------------------------------------------------
        # Tokens 1-25 contain the user's EXACT colors, motifs, style, and attire!
        engineered_prompt = (
            f"2D flat CAD textile print, seamless repeat tile, {core_subject} {attire_context}"
            f"{cultural_clause}, {layout}, orthogonal top-down flat lay view, "
            f"continuous surface pattern, crisp vector line contours, production textile swatch"
        )

        # Compact prompt to strictly under 70 tokens for 100% CLIP coverage
        tokens = engineered_prompt.split()
        if len(tokens) > 68:
            engineered_prompt = " ".join(tokens[:68])

        return {
            "matched_style": matched_style,
            "origin": origin,
            "engineered_prompt": engineered_prompt,
            "negative_prompt": strict_negative,
            "palette": ", ".join(palette_hexes[:4]),
            "extracted_colors": parsed["colors"],
            "extracted_attire": parsed["attire"],
            "extracted_styles": parsed["styles"]
        }


if __name__ == "__main__":
    store = TextileMotifStore()
    test_cases = [
        "emerald green and gold banarasi saree with peacocks",
        "navy blue and white houndstooth blazer fabric",
        "pastel pink floral dress material with silver embroidery",
        "yellow polka dots on white summer frock",
        "black and red tartan plaid suit",
        "kerala kasavu"
    ]
    for tc in test_cases:
        res = store.auto_expand_prompt(tc)
        print(f"\n==========================================")
        print(f"INPUT: '{tc}'")
        print(f"MATCHED: {res['matched_style']} ({res['origin']})")
        print(f"PALETTE: {res['palette']}")
        print(f"PROMPT: {res['engineered_prompt']}")
