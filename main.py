from requests import get
from bs4 import BeautifulSoup
import user_agent, re

def scrape_pump_fun(address: str):
    symbol_pattern = re.compile("\((\w+?)\)")
    url = f"https://pump.fun/coin/{address.strip('/').strip()}"
    try:
        if not address or not address.endswith("pump") or not (32 <= len(address) <= 44):
            return {"error": "Address was wrong."}
        response = get(url, headers={'User-Agent': user_agent.generate_user_agent()})
        # response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception:
        return {"error": "Failed to fetch the page"}
    
    try:
        age = soup.select_one('body > main > div.md\:hidden.flex.flex-col.min-h-dvh.pb-14 > div.pt-2.pl-2.pr-2 > div.p-2 > div > div > div.inline-flex.items-center.gap-4.text-\[\#9DC4F8\].flex-shrink-0 > span').text
    except Exception:
        age = None
        
    try:
        mcap = soup.select_one('body > main > div.md\:hidden.flex.flex-col.min-h-dvh.pb-14 > div.pt-2.pl-2.pr-2 > div.p-2 > div > div > div.flex.flex-wrap.gap-2.text-green-300.items-center > span').text.split("$")[1]
    except Exception:
        mcap = None
        
    try:
        reply_count = soup.select_one('body > main > div.md\:hidden.flex.flex-col.min-h-dvh.pb-14 > div.pt-2.pl-2.pr-2 > div.p-2 > div > div > div.flex.gap-1.items-center.text-\[\#9DA3AE\].flex-shrink-0').text.split("replies: ")[1]
    except Exception:
        reply_count = None
        
    try:
        name = soup.select_one('body > main > div.md\:hidden.flex.flex-col.min-h-dvh.pb-14 > div.pt-2.pl-2.pr-2 > div.p-2 > div > div > div.text-\[\#F8FAFC\].text-sm.font-medium.flex-shrink-0').text
        symbol = s.group(1) if (s:=symbol_pattern.search(name)) else ""
        name = name.strip().removesuffix(f"({symbol})")
    except Exception:
        name = None
        symbol = None
        
    try:
        image = list(filter(lambda x: x["src"].startswith("http"), soup.select("img[data-sentry-element='Image']")))
        image = image[0]["src"] if image else None
    except Exception:
        image = None
        
    return {
        "address": address,
        "url": url,
        "name": name.strip(),
        "symbol": symbol.strip(),
        "age": age.strip(),
        "mcap": mcap.strip(),
        "reply_count": reply_count.strip(),
        "image": image.strip()
    }

from fastapi import FastAPI

app = FastAPI()

@app.get("/pumpfun/{address}")
def pump_fun(address: str, key: str):
    if key.lower().strip() != "gonecold":
        return {"error": "Invalid Access-Key"}
    return scrape_pump_fun(address)
