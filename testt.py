from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# 设置 Chrome 驱动路径
chrome_service = Service('H:\\chromedriver-win64\\chromedriver.exe')  # 替换为你的 ChromeDriver 路径

# 设置浏览器为全屏模式
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # 全屏显示

# 启动 Chrome 浏览器
driver = webdriver.Chrome(service=chrome_service, options=options)

def get_steam_next_sale():
    url = "https://steamdb.info/sales/history/"
    driver.get(url)
    time.sleep(2)  # 等待页面加载

    # 使用 BeautifulSoup 解析页面内容
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # 获取本地时间信息
    local_time_div = soup.find('div', class_='sale-local-time')
    local_time = local_time_div.text.strip() if local_time_div else "无法获取本地时间"

    # 获取倒计时信息
    countdown_span = soup.find('span', class_='huge-countdown')
    countdown = countdown_span.text.strip() if countdown_span else "无法获取倒计时信息"

    # 返回结果
    return f"{local_time}\n倒计时: {countdown}"

def get_top_steam_discounts():
    url = "https://steamdb.info/sales/"
    driver.get(url)
    time.sleep(2)  # 等待页面加载

    # 使用 BeautifulSoup 解析页面内容
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", class_="table-sales")
    top_discounts = []

    if table:
        rows = table.find("tbody").find_all("tr")[:10]  # 获取前10行
        for row in rows:
            cols = row.find_all("td")
            # 获取游戏名称
            name = cols[2].find('a').text.strip()

            # 获取折扣信息
            discount = cols[3].text.strip()

            # 获取价格信息
            price = cols[4].text.strip()

            # 将信息添加到列表
            top_discounts.append((name, discount, price))

    return top_discounts

# 调用示例并打印结果
if __name__ == "__main__":
    # 获取下次Steam打折倒计时
    print("下次Steam打折倒计时：")
    print(get_steam_next_sale())

    # 获取当前打折力度最大的10个游戏
    print("\n当前打折力度最大的10个游戏：")
    top_discounts = get_top_steam_discounts()
    for name, discount, price in top_discounts:
        print(f"游戏名: {name} | 折扣: {discount} | 价格: {price}")

    # 关闭浏览器
    driver.quit()
