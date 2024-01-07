from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

def get_element(by, value):
    return driver.find_element(by=by, value=value)

def get_elements(by, value):
    return driver.find_elements(by=by, value=value)

def click_cookie():
    get_element(By.ID, "cookie").click()

def get_cookie_count():
    money_element = get_element(By.ID, "money").text.replace(",", "")
    return int(money_element)

def buy_upgrade(upgrade_id):
    get_element(By.ID, upgrade_id).click()

def main():
    timeout = time.time() + 5
    five_min = time.time() + 60 * 5

    while True:
        click_cookie()

        if time.time() > timeout:
            all_prices = get_elements(By.CSS_SELECTOR, "#store b")
            item_prices = [int(price.text.split("-")[1].strip().replace(",", "")) for price in all_prices if price.text]

            item_ids = [item.get_attribute("id") for item in get_elements(By.CSS_SELECTOR, "#store div")]

            cookie_upgrades = dict(zip(item_prices, item_ids))

            cookie_count = get_cookie_count()

            affordable_upgrades = {cost: id for cost, id in cookie_upgrades.items() if cookie_count > cost}

            if affordable_upgrades:
                highest_price_affordable_upgrade = max(affordable_upgrades)
                to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
                buy_upgrade(to_purchase_id)

            timeout = time.time() + 5

        if time.time() > five_min:
            cookie_per_s = get_element(By.ID, "cps").text
            print(cookie_per_s)
            break

if __name__ == "__main__":
    main()
