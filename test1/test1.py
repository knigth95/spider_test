import requests
from lxml import etree

url = 'https://www.gd.gov.cn/gkmlpt/policy'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }

# 发送HTTP请求，获取网页内容
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
content = response.text

# 使用lxml解析网页
html = etree.HTML(content)
row=html.xpath('/html/body/div[2]')
# 使用XPath定位链接
links = html.xpath('//div[@class="content-wrapper__router"]/*/a[@href]/@href')

link1=html.xpath('//')
print(link1)
# 输出链接
for link in links:
    print("URL链接:", link)
