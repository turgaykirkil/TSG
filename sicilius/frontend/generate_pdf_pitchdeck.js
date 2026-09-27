const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('🚀 Starting Pitch Deck PDF & Screenshot Generation...');

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 2
  });

  const page = await context.newPage();
  const indexPath = path.resolve(__dirname, 'public/presentation/index.html');
  const fileUrl = `file://${indexPath}`;

  await page.goto(fileUrl, { waitUntil: 'networkidle' });

  // Ensure output directories exist
  const docsAssetsDir = path.resolve(__dirname, '../docs/assets/presentation');
  const pdfOutputDir = path.resolve(__dirname, '../docs');
  fs.mkdirSync(docsAssetsDir, { recursive: true });

  const totalSlides = 10;
  const slideScreenshots = [];

  // Capture each slide screenshot for GitHub README and PDF
  for (let i = 1; i <= totalSlides; i++) {
    console.log(`📸 Capturing Slide ${i}/${totalSlides}...`);
    
    // Jump to slide by executing page JS
    await page.evaluate((slideNum) => {
      const slides = Array.from(document.querySelectorAll('.slide'));
      slides.forEach((slide, idx) => {
        slide.classList.remove('active', 'prev-slide');
        if (idx < slideNum - 1) {
          slide.classList.add('prev-slide');
        } else if (idx === slideNum - 1) {
          slide.classList.add('active');
        }
      });
      // Force trigger animations
      const activeSlide = slides[slideNum - 1];
      if (activeSlide) {
        activeSlide.querySelectorAll('.stat-num, .m-num').forEach(numElem => {
          const targetAttr = numElem.getAttribute('data-target');
          if (targetAttr) {
            const prefix = numElem.getAttribute('data-prefix') || '';
            const suffix = numElem.getAttribute('data-suffix') || '';
            numElem.innerText = `${prefix}${targetAttr}${suffix}`;
          }
        });
      }
    }, i);

    // Short pause to allow CSS animations to settle
    await page.waitForTimeout(600);

    const screenshotPath = path.join(docsAssetsDir, `slide_${String(i).padStart(2, '0')}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: false });
    slideScreenshots.push(screenshotPath);
  }

  console.log('✅ All slide screenshots captured in docs/assets/presentation/');

  // Generate PDF from captured high-res slides using PDFKit or HTML
  // We construct a print-friendly HTML containing high-res slide images
  const pdfHtmlPath = path.join(docsAssetsDir, 'pdf_print_template.html');
  let printHtml = `
  <!DOCTYPE html>
  <html>
  <head>
    <style>
      @page { size: 1920px 1080px; margin: 0; }
      body { margin: 0; padding: 0; background: #050b14; }
      .pdf-slide { width: 1920px; height: 1080px; page-break-after: always; display: flex; align-items: center; justify-content: center; }
      .pdf-slide img { width: 1920px; height: 1080px; object-fit: contain; }
    </style>
  </head>
  <body>
  `;

  slideScreenshots.forEach(imgPath => {
    printHtml += `<div class="pdf-slide"><img src="file://${imgPath}" /></div>`;
  });
  printHtml += `</body></html>`;

  fs.writeFileSync(pdfHtmlPath, printHtml);

  // Render PDF via Playwright
  const pdfPage = await context.newPage();
  await pdfPage.goto(`file://${pdfHtmlPath}`, { waitUntil: 'networkidle' });

  const pdfPath = path.join(pdfOutputDir, 'Sicilius_Girisim_Sunumu_PitchDeck.pdf');
  await pdfPage.pdf({
    path: pdfPath,
    width: '1920px',
    height: '1080px',
    printBackground: true,
    margin: { top: '0px', right: '0px', bottom: '0px', left: '0px' }
  });

  console.log(`🎉 Pitch Deck PDF successfully created at: ${pdfPath}`);

  await browser.close();
})();
