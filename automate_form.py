import time
import sys

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except Exception as import_error:
    print("Selenium is not installed yet. Install requirements and run again.")
    print("Hint: open a terminal here and run: setup-venv (or) pip install -r requirements.txt")
    raise import_error


def open_form_and_submit(url: str) -> None:
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # Launch Chrome (uses system Chrome; ensure it's installed)
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 20)

        # Try to find text inputs and fill placeholder answers
        text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
        for idx, el in enumerate(text_inputs, start=1):
            try:
                el.clear()
                el.send_keys(f"Sample answer {idx}")
            except Exception:
                pass

        # Try to fill textareas
        textareas = driver.find_elements(By.CSS_SELECTOR, "textarea")
        for idx, el in enumerate(textareas, start=1):
            try:
                el.clear()
                el.send_keys(f"Longer sample answer {idx}")
            except Exception:
                pass

        # Try to click first radio button in each radio group
        radios = driver.find_elements(By.CSS_SELECTOR, "div[role='radio']")
        clicked = set()
        for r in radios:
            try:
                name = r.get_attribute("aria-label") or r.get_attribute("data-value") or str(id(r))
                if name in clicked:
                    continue
                r.click()
                clicked.add(name)
            except Exception:
                pass

        # Try to check first checkbox found (if any)
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "div[role='checkbox']")
        for c in checkboxes[:1]:
            try:
                c.click()
            except Exception:
                pass

        # Try to click Submit button
        try:
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button'][aria-label*='Submit'], span[text()='Submit'], div[role='button'] span"))
            )
            submit.click()
        except Exception:
            # Fall back: click any primary button visible
            buttons = driver.find_elements(By.CSS_SELECTOR, "div[role='button']")
            for b in buttons:
                try:
                    label = (b.get_attribute("aria-label") or "").lower()
                    if "submit" in label:
                        b.click()
                        break
                except Exception:
                    pass

        time.sleep(3)
    finally:
        driver.quit()


def main():
    if len(sys.argv) < 2:
        print("Usage: python automate_form.py <google_forms_url>")
        print("Example: python automate_form.py https://forms.gle/yourFormId")
        sys.exit(1)
    open_form_and_submit(sys.argv[1])


if __name__ == "__main__":
    main()



