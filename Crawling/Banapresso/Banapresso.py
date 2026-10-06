import time
import pandas as pd
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_banapresso():
    url = "https://www.banapresso.com/"
    
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    driver.get(url)
    time.sleep(2)

    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    first_tag = driver.find_element(
        By.CSS_SELECTOR,
        "#wrap > header > div > ul > li:nth-child(2)"
    )

    second_tag = driver.find_element(
        By.CSS_SELECTOR,
        "#wrap > header > div > ul > li:nth-child(2) > ul > li:nth-child(1) > a"
    )

    action.move_to_element(first_tag)\
          .move_to_element(second_tag)\
          .click()\
          .perform()
          
    # 매장 목록이 화면에 나타날 때까지 대기
    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".store_name_map")
        )
    )      
        
    before_count = 0

    while True:
        store_names = driver.find_elements(
            By.CSS_SELECTOR,
            ".store_name_map .name"
        )

        current_count = len(store_names)
        print(f"현재 로딩된 매장 수: {current_count}")

        if current_count == before_count:
            break

        before_count = current_count

        driver.execute_script(
            """
            const listBox = document.querySelector('.store_shop_list');
            if (listBox) {
                listBox.scrollTop = listBox.scrollHeight;
            }
            """
        )

        time.sleep(1)
    
    # target = driver.find_element(By.CSS_SELECTOR, ".observer")

    # driver.execute_script(
    # "arguments[0].scrollIntoView();",
    # target
    # )
    # time.sleep(1)
    
    req = driver.page_source
    soup = BeautifulSoup(req, "html.parser")
    
    stores = soup.select(".store_name_map")
    store_data = []

    for store in stores:
        name_tag = store.select_one(".name")
        address_tag = store.select_one(".address")
        time_tag = store.select_one(".store-time-wrap")
        store_parking_tag = store.select_one(".parking")

        store_name = name_tag.get_text(strip=True) if name_tag else ""
        store_address = address_tag.get_text(strip=True) if address_tag else ""
        store_time = time_tag.get_text(" ", strip=True) if time_tag else ""
        store_parking = store_parking_tag.get_text(strip=True) if store_parking_tag else ""

        if store_name and store_address:
            store_data.append({
                "매장명": store_name,
                "주소": store_address,
                "영업정보": store_time,
                "주차 정보": store_parking
            })

    df = pd.DataFrame(store_data)
    df = df.drop_duplicates(subset=["매장명", "주소"])
    df.index = df.index + 1


    driver.quit()
    
    return df


banapresso_df = fetch_banapresso()

banapresso_df.to_csv(
    "banapresso.csv",
    index=False,
    encoding='utf-8-sig'
)
    
