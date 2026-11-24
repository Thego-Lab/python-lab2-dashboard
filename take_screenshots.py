import os
import time
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "screenshots")
URL = "http://localhost:8505"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = ["数据概览", "维度统计", "趋势分析", "明细数据"]
HIDE_BARS = """
header[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
#MainMenu { display: none !important; }
"""


def layout(page):
    return page.evaluate(
        """(names) => {
            const els = [...document.querySelectorAll('h3, h2')];
            const tops = names.map(n => {
                const el = els.find(e => e.innerText.includes(n));
                return el ? el.getBoundingClientRect().top + window.scrollY : null;
            });
            const footer = [...document.querySelectorAll('div')]
                .find(e => e.innerText && e.innerText.startsWith('学生成绩数据看板 | 数据来源'));
            const end = footer ? footer.getBoundingClientRect().bottom + window.scrollY + 30 : document.body.scrollHeight;
            return {tops, end};
        }""",
        HEADERS,
    )


with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1400, "height": 2600})
    page.goto(URL, wait_until="networkidle")
    page.get_by_text("学生成绩数据看板").first.wait_for(timeout=60000)
    page.add_style_tag(content=HIDE_BARS)
    time.sleep(2)

    page.set_viewport_size({"width": 1400, "height": 2600})
    time.sleep(2)
    info = layout(page)
    tops, end = info["tops"], info["end"]
    print("tops:", tops, "end:", end)

    marks = [0, tops[1] - 40, tops[2] - 40, tops[3] - 40, end]
    names = ["01_数据概览.png", "02_维度统计.png", "03_趋势分析.png", "04_明细数据.png"]
    for i, name in enumerate(names):
        page.screenshot(
            path=os.path.join(OUTPUT_DIR, name),
            clip={"x": 0, "y": marks[i], "width": 1400, "height": marks[i + 1] - marks[i]},
        )
        print("saved", name, marks[i + 1] - marks[i])

    page.screenshot(
        path=os.path.join(OUTPUT_DIR, "05_完整看板.png"),
        clip={"x": 0, "y": 0, "width": 1400, "height": end},
    )
    print("saved 05_完整看板.png", end)
    browser.close()
print("done")