import requests
from bs4 import BeautifulSoup

def get_fox_news_headline_as_link():
    url = "https://www.foxnews.com/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 查找头版头条的 h3 标签
        headline_tag = soup.find("h3", class_="title")
        
        if headline_tag:
            headline_text = headline_tag.text.strip()
            headline_link = headline_tag.find("a")["href"]
            
            # 检查链接是否为完整URL
            if not headline_link.startswith("http"):
                headline_link = "https://www.foxnews.com" + headline_link
            
            # 返回HTML格式的可点击链接
            clickable_link = f'<a href="{headline_link}" target="_blank">{headline_text}</a>'
            return clickable_link
        else:
            return "无法找到头版头条，请检查选择器。"
    else:
        return "无法访问Fox News网站，请检查网络连接。"

# 调用函数并打印HTML格式的结果
clickable_headline = get_fox_news_headline_as_link()
print("头版头条链接：", clickable_headline)
