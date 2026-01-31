import requests
from bs4 import BeautifulSoup

# 1. 目标 URL (根据你的截图地址栏)
url = 'http://www.qinfeng.gov.cn/jdpg1/xa.htm'

# 2. 发送请求
headers = {'User-Agent': 'Mozilla/5.0 ...'} # 模拟浏览器，防止被拦截
response = requests.get(url, headers=headers)
response.encoding = 'utf-8' # 解决中文乱码

# 3. 解析网页
soup = BeautifulSoup(response.text, 'html.parser')

#####################################################################################################

# # 4. 提取标题 (根据截图中显示的 class)
# titles = soup.find_all('p', class_='bgt_index_right_list_title')
# for t in titles:
#     print(t.get_text(strip=True))

#####################################################################################################

# 4. 提取标题和链接
titles = soup.find_all('p', class_='bgt_index_right_list_title')

for t in titles:
    # 在当前 <p> 标签下寻找 <a> 标签
    a_tag = t.find('a') 
    
    if a_tag:
        title_text = a_tag.get_text(strip=True) # 提取标题文字
        link = a_tag.get('href') # 提取 href 属性（链接）
        # 这里的链接可能是相对路径（如 xa/123.htm），需要拼接成完整 URL
        if not link.startswith('http'):
            # 使用 requests.compat.urljoin 自动处理路径拼接
            from requests.compat import urljoin
            full_link = urljoin(url, link)
        else:
            full_link = link
            
        print(f"标题: {title_text}")
        print(f"链接: {full_link}")
        print("-" * 30)