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
#rows = html.xpath('/html/body/div[@class="content-container"]//node()')
rows=html.xpath('/html/body/div[@class="content-container"]//div[3]')
#/html/body/div[2]/div[4]/div[2]/div[2]/table
print(rows)
for row in rows:
    # 使用XPath路径定位<a>标签中的文本内容
    text=html.xpath('/html/body/div[2]/div[4]/div[2]/div[2]/table/tbody/tr[4]/td[2]/text()')
    print(text)
    # 使用XPath路径定位<a>标签中的URL链接
    link = row.xpath('//@href')
    link1=row.xpath('//div[4]/div[2]/div[2]/table/tbody/tr[4]/td[1]//a[@href]')
    print(link)    

