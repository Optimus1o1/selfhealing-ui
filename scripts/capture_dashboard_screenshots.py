"""Script to automate Playwright capture of all 9 Streamlit Dashboard sections.

Moon Sanctum Labs | Decode. Build. Evolve.
"""

import os
import subprocess
import sys
import time
import urllib.request
from playwright.sync_api import sync_playwright

SECTIONS = [
    ("Overview", "01_overview.png"),
    ("Live Execution", "02_live_execution.png"),
    ("Healing Analytics", "03_healing_analytics.png"),
    ("Locator Explorer", "04_locator_explorer.png"),
    ("Fingerprint Inspector", "05_fingerprint_inspector.png"),
    ("Intelligence Inspector", "06_intelligence_inspector.png"),
    ("Audit Centre", "07_audit_centre.png"),
    ("Baseline Manager", "08_baseline_manager.png"),
    ("Performance Monitor", "09_performance_monitor.png"),
]

SCREENSHOT_DIR = os.path.abspath("artifacts/screenshots/dashboard")
PORT = 8503
BASE_URL = f"http://127.0.0.1:{PORT}"

def wait_for_server(url: str, timeout: int = 30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False

def main():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    
    # Launch Streamlit in subprocess
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "src/selfheal/dashboard/app.py",
        f"--server.port={PORT}",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]
    print(f"Launching Streamlit dashboard on port {PORT}...")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        if not wait_for_server(BASE_URL, timeout=25):
            print("Streamlit server failed to start within timeout!")
            stdout, stderr = proc.communicate(timeout=3)
            print("STDOUT:", stdout)
            print("STDERR:", stderr)
            sys.exit(1)
        
        print("Streamlit server is ready. Launching Playwright to capture screenshots...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1600, "height": 1000})
            page = context.new_page()
            
            page.goto(BASE_URL, wait_until="networkidle")
            page.wait_for_selector('[data-testid="stRadio"]', timeout=15000)
            time.sleep(2)
            
            for section_name, filename in SECTIONS:
                print(f"Capturing section: {section_name} -> {filename}")
                
                # Click the radio button label in the sidebar
                label_loc = page.locator('[data-testid="stRadio"] label').filter(has_text=section_name)
                if label_loc.count() > 0:
                    label_loc.first.click()
                else:
                    print(f"Warning: Could not find radio label for {section_name}")
                
                # Allow Streamlit to re-render
                time.sleep(2.5)
                # Wait for any status/spinner to complete
                page.wait_for_load_state("networkidle")
                
                out_path = os.path.join(SCREENSHOT_DIR, filename)
                page.screenshot(path=out_path, full_page=True)
                print(f"  [SAVED] {out_path} ({os.path.getsize(out_path):,} bytes)")
            
            browser.close()
            print("All 9 dashboard sections captured successfully.")
            
    finally:
        print("Terminating Streamlit process...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()

if __name__ == "__main__":
    main()

