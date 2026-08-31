import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import cv2
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

TEMPLATE_PATH = ROOT_DIR / "skilline-landing-page" / "index.html"
url = TEMPLATE_PATH.as_uri()

from generate_dataset import MUTATIONS, STABILIZATION_CSS

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1000, "height": 800})
    
    for item in MUTATIONS:
        idx = item["id"]
        scroll_y = item["scroll_y"]
        js_code = item["js"]
        
        page.goto(url, wait_until="load")
        page.add_style_tag(content=STABILIZATION_CSS)
        page.evaluate(f"window.scrollTo(0, {scroll_y});")
        page.wait_for_timeout(100)
        
        # Take baseline bytes
        base_bytes = page.screenshot()
        
        # Run mutation and check return value
        res = page.evaluate(f"""() => {{
            try {{
                {js_code}
                return "OK";
            }} catch(e) {{
                return "ERROR: " + e.message;
            }}
        }}""")
        page.wait_for_timeout(100)
        
        # Take current bytes
        curr_bytes = page.screenshot()
        
        # Compare
        img_b = cv2.imdecode(np.frombuffer(base_bytes, np.uint8), cv2.IMREAD_COLOR)
        img_c = cv2.imdecode(np.frombuffer(curr_bytes, np.uint8), cv2.IMREAD_COLOR)
        diff_px = int(np.count_nonzero(cv2.absdiff(img_b, img_c)))
        
        print(f"Sample {idx:02d} [{item['name']}]: JS Result='{res}' | Diff Pixels={diff_px}", flush=True)
        
    browser.close()
