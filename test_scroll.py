import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import cv2
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = ROOT_DIR / "skilline-landing-page" / "index.html"
url = TEMPLATE_PATH.as_uri()

STABILIZATION_CSS = """
*, *::before, *::after {
    transition: none !important;
    animation: none !important;
}
[data-aos] {
    opacity: 1 !important;
    transform: none !important;
    visibility: visible !important;
}
"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1000, "height": 800})
    page.goto(url, wait_until="load")
    page.add_style_tag(content=STABILIZATION_CSS)
    
    # Test Amazon logo with scroll_into_view
    loc = page.locator("img[src*='amazon.svg']")
    loc.scroll_into_view_if_needed()
    page.wait_for_timeout(100)
    
    b_bytes = page.screenshot()
    page.evaluate("document.querySelector(\"img[src*='amazon.svg']\").style.display = 'none'")
    page.wait_for_timeout(100)
    c_bytes = page.screenshot()
    
    img_b = cv2.imdecode(np.frombuffer(b_bytes, np.uint8), cv2.IMREAD_COLOR)
    img_c = cv2.imdecode(np.frombuffer(c_bytes, np.uint8), cv2.IMREAD_COLOR)
    diff_px = int(np.count_nonzero(cv2.absdiff(img_b, img_c)))
    print("Amazon test diff pixels:", diff_px)
    
    browser.close()
