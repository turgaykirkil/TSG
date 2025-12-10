
import os

path = '/Users/nalanmerci/sicilius/backend/app/scraping_browser.py'
with open(path, 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
encoded_search = 'await page.goto("https://www.ticaretsicil.gov.tr/view/hizlierisim/ilangoruntuleme.php", wait_until="domcontentloaded")'
found = False

for line in lines:
    if encoded_search in line:
        found = True
        new_lines.append(line)
        # Inject our block
        new_lines.append('        try:\n')
        new_lines.append('            await page.wait_for_selector("select#SicilMudurluguId", timeout=30000)\n')
        new_lines.append('            await page.select_option("select#SicilMudurluguId", label=office_label)\n')
        new_lines.append('            await page.fill("input#TicSicNo", str(company.sicil_no))\n')
        new_lines.append('            await page.click("button[data-message=\'İlan Ara\']")\n')
        new_lines.append('        except Exception as e:\n') 
        new_lines.append('            import os\n')
        new_lines.append('            debug_dir = "/app/data/uploads"\n')
        new_lines.append('            if not os.path.exists(debug_dir): os.makedirs(debug_dir, exist_ok=True)\n')
        new_lines.append('            error_id = f"error_{company.id}_{company.sicil_no}"\n')
        new_lines.append('            screenshot_path = f"{debug_dir}/{error_id}.png"\n')
        new_lines.append('            html_path = f"{debug_dir}/{error_id}.html"\n')
        new_lines.append('            try:\n')
        new_lines.append('                await page.screenshot(path=screenshot_path)\n')
        new_lines.append('                with open(html_path, "w") as f: f.write(await page.content())\n')
        new_lines.append('                logger.error(f"TIMEOUT DEBUG: Saved screenshot to {screenshot_path}")\n')
        new_lines.append('            except Exception as snap_err:\n')
        new_lines.append('                logger.error(f"Failed to capture debug snapshot: {snap_err}")\n')
        new_lines.append('            raise e\n')
        
        skip = True
    elif skip:
        # Stop skipping when we hit the next section
        if 'scraping_state.add_log("FORM_SUBMITTED:' in line:
            skip = False
            new_lines.append(line)
        # Else ignore the old naive lines
    else:
        new_lines.append(line)

if found:
    with open(path, 'w') as f:
        f.writelines(new_lines)
    print("Successfully patched file.")
else:
    print("Could not find target line to patch.")
