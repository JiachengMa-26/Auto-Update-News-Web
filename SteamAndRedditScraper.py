from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

class SteamAndRedditScraper:
    def __init__(self, driver_path):
        # 初始化 Chrome 浏览器驱动
        chrome_service = Service(driver_path)
        
        # 设置浏览器为全屏模式
        self.chrome_options = Options()
        self.chrome_options.add_argument("--start-maximized")  # 全屏显示
        self.driver = webdriver.Chrome(service=chrome_service, options=self.chrome_options)

    def get_reddit_posts(self, url):
        """通用函数，用于获取指定 Reddit 页面上的帖子。"""
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )
            time.sleep(2)
        except Exception as e:
            print(f"Error loading page {url}: {e}")
            return []

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        posts = soup.find_all('article')
        post_data = []

        for post in posts:
            title = post.get('aria-label', 'No title')
            content_div = post.find('div', {'class': 'mb-xs'})
            content = content_div.text.strip() if content_div else 'No content'
            post_data.append((title, content))

        return post_data

    def get_general_games_news(self):
        """获取 General 游戏新闻（/r/Games/hot）并返回第一个帖子"""
        url = "https://www.reddit.com/r/Games/hot/"
        posts = self.get_reddit_posts(url)
        return posts[0] if posts else ("No title", "No content")

    def get_lol_news(self):
        """获取 League of Legends 新闻（/r/leagueoflegends/hot）并返回第一个帖子"""
        url = "https://www.reddit.com/r/leagueoflegends/hot/"
        posts = self.get_reddit_posts(url)
        return posts[0] if posts else ("No title", "No content")

    def get_steam_next_sale(self):
        url = "https://steamdb.info/sales/history/"
        self.driver.get(url)
        time.sleep(2)

        # 使用 BeautifulSoup 解析页面内容
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # 获取本地时间信息
        local_time_div = soup.find('div', class_='sale-local-time')
        local_time = local_time_div.text.strip() if local_time_div else "无法获取本地时间"

        # 获取倒计时信息
        countdown_span = soup.find('span', class_='huge-countdown')
        countdown = countdown_span.text.strip() if countdown_span else "无法获取倒计时信息"

        return f"{local_time}\n倒计时: {countdown}"

    def get_top_steam_discounts(self):
        url = "https://steamdb.info/sales/"
        self.driver.get(url)
        time.sleep(2)

        # 使用 BeautifulSoup 解析页面内容
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        table = soup.find("table", class_="table-sales")
        top_discounts = []

        if table:
            rows = table.find("tbody").find_all("tr")[:10]  # 获取前10行
            for row in rows:
                cols = row.find_all("td")
                # 获取游戏名称
                name = cols[2].find('a').text.strip() if cols[2].find('a') else "无名称"

                # 获取折扣信息
                discount = cols[3].text.strip()

                # 获取价格信息
                price = cols[4].text.strip()

                # 将信息添加到列表
                top_discounts.append((name, discount, price))

        return top_discounts

    def close_driver(self):
        self.driver.quit()

# 示例调用函数并打印结果
if __name__ == "__main__":
    # 实例化类并传入 ChromeDriver 路径
    scraper = SteamAndRedditScraper(driver_path='H:\\chromedriver-win64\\chromedriver.exe')

    # 获取 General 游戏新闻
    general_title, general_content = scraper.get_general_games_news()
    print("General 游戏新闻：")
    print(f"标题: {general_title}")
    print(f"内容: {general_content}")
    print("-" * 40)

    # 获取 League of Legends 新闻
    lol_title, lol_content = scraper.get_lol_news()
    print("League of Legends 新闻：")
    print(f"标题: {lol_title}")
    print(f"内容: {lol_content}")
    print("-" * 40)

    # 获取下次 Steam 打折倒计时
    print("下次 Steam 打折倒计时：")
    print(scraper.get_steam_next_sale())
    print("-" * 40)

    # 获取当前打折力度最大的10个游戏
    print("当前打折力度最大的10个游戏：")
    top_discounts = scraper.get_top_steam_discounts()
    for name, discount, price in top_discounts:
        print(f"游戏名: {name} | 折扣: {discount} | 价格: {price}")
    print("-" * 40)

    # 关闭浏览器
    scraper.close_driver()
