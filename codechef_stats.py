import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import os
import re
USERNAME = "bouquet_grape"
URL = f"https://www.codechef.com/users/{USERNAME}"
headers = {
    "User-Agent": "Mozilla/5.0"
}
def extract_rank(text):
    return text.strip() if text else "N/A"
try:
    res = requests.get(URL, headers=headers, timeout=15)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    rating_tag = soup.find("div", class_="rating-number")
    rating = rating_tag.text.strip() if rating_tag else "N/A"
    stars_tag = soup.find("span", class_="rating-star")
    stars = stars_tag.text.strip() if stars_tag else "N/A"
    global_rank = "N/A"
    country_rank = "N/A"
    for li in soup.select("li"):
        text = li.get_text(strip=True)
        if "Global Rank" in text:
            global_rank = re.sub(r"[^\d,]", "", text)
        if "Country Rank" in text:
            country_rank = re.sub(r"[^\d,]", "", text)
except Exception as e:
    rating = "N/A"
    stars = "N/A"
    global_rank = "N/A"
    country_rank = "N/A"
os.makedirs("assets", exist_ok=True)
WIDTH, HEIGHT = 495, 195
BG_COLOR = "#FFFDF7"  # Off-white/cream
BORDER_COLOR = "#E4E2E0"  # Light gray border
HEADER_COLOR = "#5B4638"  # CodeChef brown
ACCENT_COLOR = "#F5A623"  # CodeChef orange
TEXT_PRIMARY = "#2D2D2D"  # Dark text
TEXT_SECONDARY = "#666666"  # Gray text
img = Image.new("RGB", (WIDTH, HEIGHT), color=BG_COLOR)
draw = ImageDraw.Draw(img)
draw.rectangle([(0, 0), (WIDTH-1, HEIGHT-1)], outline=BORDER_COLOR, width=1)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    font_title = ImageFont.truetype(
        os.path.join(BASE_DIR, "DejaVuSans-Bold.ttf"), 18
    )
    font_label = ImageFont.truetype(
        os.path.join(BASE_DIR, "DejaVuSans.ttf"), 12
    )
    font_value = ImageFont.truetype(
        os.path.join(BASE_DIR, "DejaVuSans-Bold.ttf"), 14
    )
except Exception as e:
    font_title = font_label = font_value = ImageFont.load_default()

except Exception as e:
    font_title = font_label = font_value = ImageFont.load_default()
draw.text((20, 20), "CodeChef Stats", fill=HEADER_COLOR, font=font_title)
draw.text((20, 50), USERNAME, fill=TEXT_SECONDARY, font=font_label)
stats = [
    ("Current Rating", rating, 20, 80),
    ("Stars", stars, 260, 80),
    ("Global Rank", global_rank, 20, 135),
    ("Country Rank", country_rank, 260, 135),
]
for label, value, x, y in stats:
    draw.text((x, y), label, fill=TEXT_SECONDARY, font=font_label)
    value_color = ACCENT_COLOR if "Rating" in label or "Stars" in label else HEADER_COLOR
    draw.text((x, y + 20), str(value), fill=value_color, font=font_value)
output_path = "assets/codechef.png"
img.save(output_path, dpi=(300, 300))
