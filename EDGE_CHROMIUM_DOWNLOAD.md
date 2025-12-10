# Edge & Chromium Browser Download Links

## Microsoft Edge for macOS

**Official Download Page:**
https://www.microsoft.com/edge/download

**Direct Download Links:**

### Apple Silicon (M1/M2/M3)
https://go.microsoft.com/fwlink/?linkid=2093504

### Intel Mac
https://go.microsoft.com/fwlink/?linkid=2093438

## Installation Instructions

1. Click the appropriate link above for your Mac (Apple Silicon or Intel)
2. Download the `.dmg` file
3. Open the downloaded file
4. Drag `Microsoft Edge.app` to your Applications folder
5. Open Applications and launch Microsoft Edge
6. Click "Open" when macOS asks for confirmation

## Alternative: Install via Playwright

If you prefer to use Chromium (open-source version of Edge) with Playwright:

```bash
# SSH to production server
ssh nalanmerci@192.168.1.5

# Install Chromium browser
export PATH=$PATH:/Users/nalanmerci/Library/Python/3.9/bin
playwright install chromium
```

This will download and install Chromium browser for use with Playwright.

## Browser Comparison

| Browser | Size | Use Case |
|---------|------|----------|
| **WebKit** | 77 MB | Already installed, good for general scraping |
| **Chromium** | ~150 MB | Chrome-like, best compatibility |
| **Edge** | ~200 MB | Full-featured browser, manual download needed |

## Which Browser for Scraping?

For your scraping needs:
- **Recommended:** WebKit (already installed, lightweight)
- **Alternative:** Chromium via Playwright (if you need Chrome compatibility)
- **Optional:** Edge (if you specifically need Edge features)

WebKit should work fine for most scraping tasks on Turkish government websites!
