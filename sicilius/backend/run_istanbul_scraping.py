import asyncio
import sys
import logging
from app.scraping_browser import start_enhanced_scraping_process, browser_manager
from app.core.config import settings

logging.basicConfig(level=logging.INFO)

async def main():
    print("Opening browser (headless mode)...")
    await browser_manager.open_browser(headless=True)
    
    print("Starting scraping for İSTANBUL (10 items)...")
    # Using mode='city_fill' triggers the city based approach
    await start_enhanced_scraping_process(count=10, city="İSTANBUL", mode="city_fill")
    
    print("Closing browser...")
    await browser_manager.close_browser()
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
