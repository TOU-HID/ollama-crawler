import asyncio
import json
import os
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from extractors import extract_with_ollama

URL = "https://bangla.themirrorasia.net/"

async def main():
    print(f"🌐 Fetching: {URL}")
    browser_config = BrowserConfig()
    run_config = CrawlerRunConfig()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        try:
            result = await crawler.arun(url=URL, config=run_config)
            html = result.html
            shtml = html[:2000]  # only sending 2k characters for testing
            print(f"✅ Fetched HTML ({len(html)} characters)")
            print(html)
        except Exception as e:
            print(f"❌ Failed to crawl the page: {e}")
            return

    # 🧠 Run Ollama-based extractor
    print("🔍 Extracting articles using Ollama...")
    articles = extract_with_ollama(shtml)

    if articles:
        os.makedirs("data", exist_ok=True)
        with open("data/extracted.json", "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        print("✅ Extracted data saved to data/extracted.json")
    else:
        print("⚠️ No structured data extracted.")

if __name__ == "__main__":
    asyncio.run(main())
