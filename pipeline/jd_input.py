import trafilatura
import requests
from bs4 import BeautifulSoup

def fetch_jd_from_url(url):
    block_signals = ["enable javascript", "verification required", "captcha",
                      "security check", "access denied", "are you a robot"]

    def looks_blocked(text):
        low = text.lower()
        return any(sig in low for sig in block_signals)

    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        text = trafilatura.extract(downloaded)
        if text and len(text) > 150 and not looks_blocked(text):
            return text

    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        if len(text) > 150 and not looks_blocked(text):
            return text
        return None
    except Exception:
        return None

def get_jd_text(jd_input):
    if not jd_input:
        return None
    jd_input = jd_input.strip()
    if jd_input.startswith("http"):
        text = fetch_jd_from_url(jd_input)
        if not text:
            print("Could not fetch this URL automatically (common for LinkedIn/JS-heavy pages). "
                  "Paste the job description text directly instead.")
            return None
        return text
    return jd_input

print("JD input functions ready.")