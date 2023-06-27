import requests
from lxml import etree
import pandas as pd

def crawl_policy_info(url):
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }

    # 发送HTTP请求，获取网页内容
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    content = response.text

    # 使用lxml解析网页
    html = etree.HTML(content)

    # 提取政策信息
    policy_list = html.xpath('/html/body/div[@class="content-container"]/div[@class="content-wrapper"]/div[@class="content-box"]')

    result = []
    for policy in policy_list:
        index = policy.xpath('//td[contains(text(), "索引号")]/following-sibling::td//text()')[1]
        publishing_organization = policy.xpath('//td[@class="first" and contains(text(), "发布机构")]/following-sibling::td/span/text()')[0]
        date = policy.xpath('//td[@class="second" and contains(text(), "发布日期")]/following-sibling::td/span/text()')[0]
        title = policy.xpath('//span[@class="document-number"]/@title')[0]
        text = [text.strip().replace('\u3000', '') for text in policy.xpath('//div[@class="article-content"]/p[@style="text-align: justify;"]/text()')]
        attachment = policy.xpath('//div[@class="article-content"]/p[@style="text-align: justify;"]/a/@href')[0]
        result.append({
            '索引号': index,
            '发布机构': publishing_organization,
            '发布日期': date,
            '政策标题': title,
            '政策正文文本': text,
            '政策正文附件链接': attachment
        })
        
        # 将政策文本保存为txt文件
        with open(f'./{title}.txt', 'a', encoding='utf-8') as file:
            for line in text:
                file.write(line + '\n')

    # 将结果转换为DataFrame对象
    df = pd.DataFrame(result)

    return df

url=['https://www.gd.gov.cn/gkmlpt/content/4/4199/post_4199084.html#8',
     'https://www.gd.gov.cn/gkmlpt/content/4/4204/post_4204713.html#8',
     'https://www.gd.gov.cn/gkmlpt/content/4/4206/post_4206700.html#8']

# 读取已有的Excel文件作为初始DataFrame
try:
    original_df = pd.read_excel('policy_info.xlsx')
except FileNotFoundError:
    original_df = pd.DataFrame()

# 追加写入数据
for i in range(len(url)):
    df = crawl_policy_info(url[i])
    original_df = original_df.append(df, ignore_index=True)

# 保存结果到Excel文件
original_df.to_excel('policy_info.xlsx', index=False)

