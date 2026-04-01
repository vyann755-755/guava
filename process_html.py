import os
import re
import base64
from io import BytesIO
try:
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'Pillow'])
    from PIL import Image

NEW_IMAGE_PATH = "/Users/vyanntio/.gemini/antigravity/brain/254a1220-4295-4ddd-a050-77a15b26f4dc/guava_girl_enjoying_drink_1775034818748.png"

def image_to_base64_data_url(image_path, max_size=800):
    if not os.path.exists(image_path):
        return None
    with Image.open(image_path) as img:
        img.thumbnail((max_size, max_size))
        buffered = BytesIO()
        # Convert to RGB to save as JPEG for better compression if it has no alpha, but let's stick to JPEG for size
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(buffered, format="JPEG", quality=80)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return "data:image/jpeg;base64," + img_str

image_cache = {}
def get_b64(path):
    if path not in image_cache:
        image_cache[path] = image_to_base64_data_url(path)
    return image_cache[path]

replacements = {
    # English replacements
    "Relieve Bloating": "Joyful Digestion",
    "Comfortable Digestion": "Joyful Digestion",
    "Soothe Your Gut": "Joyful Digestion",
    
    "Diet Prone & Slim Down": "Healthy Slimming",
    "Natural Weight Wellness": "Healthy Slimming",
    "Discover Pure Comfort": "Healthy Slimming",
    
    "Guava ezGo & Guava Golden Enzyme for fresh, light, daily detox.": "Gently promotes natural movements for a totally joyful and comfortable gut.",
    "Slim down naturally with our immune-boosting signature products.": "Flushes toxins for healthier slimming and reveals clearer, brighter glowing skin.",
    "Enjoy Golden Enzyme for immune support & Guava ezGo to relieve bloating.": "Rich in natural antioxidants to keep your immunity maintained and strongly healthy.",
    "Gently promotes natural movements for a comfortable gut all day.": "Gently promotes natural movements for a totally joyful and comfortable gut.",
    "Flushes toxins to reveal clearer, brighter, and healthier skin.": "Flushes toxins for healthier slimming and reveals clearer, brighter glowing skin.",
    "Rich in natural antioxidants to keep you feeling strong.": "Rich in natural antioxidants to keep your immunity maintained and strongly healthy.",
    
    "Daily Detox": "Joyful Wellness Routine",
    "Your Daily Ritual": "Joyful Wellness Routine",
    "Radiant Days": "Glowing Smooth Skin",
    "Slim Down & Cleanse": "Healthy & Gentle Slimming",
    "Glow From Within": "Glowing Smooth Skin",
    
    # EDM specific
    "Fresh, Light & Slim Down": "Joyful Digestion & Glowing Skin",
    "Comfortable Digestions & Radiant Days": "Joyful Digestion & Glowing Skin",
    "The New Mr. Farmer": "Joyful Digestion & Glowing Skin",
    
    "Introducing Golden Enzyme & Guava ezGo. Relieving bloating has never looked this fresh.": "Promotes a naturally healthy slimming journey and maintains strong immunity.",
    "Promotes natural movements, flushes toxins, and supports immunity for radiant days.": "Promotes a naturally healthy slimming journey and maintains strong immunity.",
    
    "Experience the ultimate daily cleanse to support digestion and immune health.": "Experience a healthy beautiful slimming journey with Guava ezGo and Golden Enzyme.",
    "Experience our Natural Weight Wellness journey with Guava ezGo and Golden Enzyme.": "Experience a healthy beautiful slimming journey with Guava ezGo and Golden Enzyme.",
    
    "Relieves Bloating": "Joyful Digestion",
    "Pure Comfort": "Joyful Digestion",
    "Golden Enzyme": "Glowing Smooth Skin",
    "Natural Glow": "Glowing Smooth Skin",
    
    # Video specific
    "Find Your Glow": "Glowing Smooth Skin",
    "A moment of pure comfort.": "A truly comfortable moment of natural wellness and glowing skin.",
    "A moment of clear digestion and immune support.": "A truly comfortable moment of natural wellness and glowing skin.",
    "A moment of natural weight wellness and radiant days.": "A truly comfortable moment of natural wellness and glowing skin.",
    
    # Badges
    "Digestive Support": "Joyful Digestion",
    "SGS Certified": "Joyful Digestion",
    "Slim Down": "Healthy Slimming",
    "Nutri-Grade A": "Healthy Slimming",
    "Feeling Strong": "Maintained Immunity",
    "Immune Support": "Maintained Immunity",
    "11 kcal": "Maintained Immunity",
    "0g Sugar": "Glowing Skin",
    
    # Chinese replacements
    "告别腹胀 (Relieve Bloating)": "享受愉悦消化",
    "舒畅消化": "享受愉悦消化",
    "纯净安抚": "享受愉悦消化",
    "轻松瘦身 (Slim Down)": "健康轻盈之旅",
    "轻松瘦身": "健康轻盈之旅",
    "自然轻体": "健康轻盈之旅",
    "舒缓肠胃": "健康轻盈之旅",
    "芭乐黄金酵素与ezGo": "享受温和净化，为您带来健康舒适的轻体体验",
    "自然畅通，维持全天候肠胃舒适": "享受温和净化，为您带来健康舒适的轻体体验",
    "享受清新与净透之旅以提升免疫力": "排出体内毒素，让肌肤更加柔滑光泽、焕然一新",
    "排出毒素，展现更透亮的健康肌肤": "排出体内毒素，让肌肤更加柔滑光泽、焕然一新",
    "每日开启排毒新旅程，促进消化吸收": "维持强健免疫力，保持时刻健康的活力好状态",
    "富含天然抗氧化剂，让您时刻充满活力": "维持强健免疫力，保持时刻健康的活力好状态",
    "每日清体排毒": "健康柔滑美肌",
    "自然焕发光彩": "健康自然光彩",
    "黄金酵素提升免疫力，ezGo告别腹胀": "享受愉悦消化与塑造健康轻盈体态",
    "享受舒适消化与自然轻体的健康之旅": "享受愉悦消化与塑造健康轻盈体态",
    "芭乐 ezGo 与黄金酵素：为您带来每日排毒": "为您带来强健的免疫力与光滑的肌肤",
    "为您带来舒适消化与焕发光彩的每一天": "为您带来强健的免疫力与光滑的肌肤",
    "体验自然清新的轻盈净化之旅，轻松瘦身。": "体验自然轻盈的每一天，用健康的方式塑造美好身姿",
    "体验自然轻盈的每一天，轻松塑造健康体态。": "体验自然轻盈的每一天，用健康的方式塑造美好身姿",
    "缓解腹胀": "愉悦消化",
    "增强免疫": "强健免疫力",
    "强健活力": "强健免疫力",
    "由内而外焕发光彩": "柔滑光泽肌肤"
}

files = [
    f for f in os.listdir('.') if f.startswith('new_mrfarmer_') and f.endswith('.html')
]

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix layout CSS overlapping the new centered image
    content = content.replace("background-position: left center;", "background-position: center top;")
    content = content.replace("background-position: right center;", "background-position: center top;")
    content = content.replace("background-position: center center;", "background-position: center top;")
    content = content.replace("top: 50%;\n  transform: translateY(-50%);\n  right: 24px;\n  width: 250px;", "bottom: 12px;\n  right: 12px;\n  left: 12px;\n  width: auto;\n  background: rgba(255, 255, 255, 0.95);")
    content = content.replace("bottom: 60px; left: 16px; right: 16px;", "bottom: 16px; left: 12px; right: 12px;")
    
    # Replace phrasing
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    # Find all inline urls or src
    # e.g. url('guava_lifestyle_user...png') or src="guava_hero_product...png"
    
    # Replace the lifestyle user image with the new gal
    content = re.sub(r"url\(['\"]?guava_lifestyle_user_.*?\.png['\"]?\)", "url('" + get_b64(NEW_IMAGE_PATH) + "')", content)
    content = re.sub(r'src=["\']guava_lifestyle_user_.*?\.png["\']', 'src="' + get_b64(NEW_IMAGE_PATH) + '"', content)
    
    # For other images, base64 them as is
    for match in re.finditer(r"url\(['\"]?(guava_.*?\.png)['\"]?\)", content):
        img_file = match.group(1)
        if os.path.exists(img_file):
            b64 = get_b64(img_file)
            content = content.replace(match.group(0), "url('" + b64 + "')")
            
    for match in re.finditer(r'src=["\'](guava_.*?\.png)["\']', content):
        img_file = match.group(1)
        if os.path.exists(img_file):
            b64 = get_b64(img_file)
            content = content.replace(match.group(0), 'src="' + b64 + '"')
            
    # Also we should change the output filename to indicate it is standalone
    out_filename = filename.replace('new_mrfarmer_', 'standalone_')
    with open(out_filename, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Processed {filename} -> {out_filename}")
