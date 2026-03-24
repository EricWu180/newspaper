import json
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

RSS_FEEDS = [
    {'name': '新华网', 'url': 'http://www.news.cn/rss/news.xml'},
    {'name': '中国网', 'url': 'http://www.china.com.cn/rss/today.xml'},
    {'name': '央视新闻', 'url': 'https://www.cctv.com/rss/newsindex.xml'},
]

def fetch_rss(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.content)
        items = []
        for item in root.findall('.//item'):
            title = item.find('title')
            link = item.find('link')
            pubDate = item.find('pubDate')
            if title is not None:
                items.append({
                    'title': title.text,
                    'link': link.text if link
is not None else '',
                    'pubDate': pubDate.text if pubDate is not None else ''
                })
        return items[:3]
    except Exception as e:
        print(f"抓取失败 {url}: {e}")
        return []

def format_time(date_str):
    if not date_str:
        return '未知时间'
    try:
        date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        now = datetime.now(date.tzinfo)
        diff = (now - date).total_seconds() / 60
        if diff < 1:
            return '刚刚'
        elif diff < 60:
            return f'{int(diff)}分钟前'
        elif diff < 1440:
            return f'{int(diff/60)}小时前'
        else:
            return f'{int(diff/1440)}天前'
    except:
        return '未知时间'

def main():
    all_news = []
    for feed in RSS_FEEDS:
        items = fetch_rss(feed['url'])
        for item in items:
            all_news.append({
                'title': f"【{feed['name']}】{item['title']}",
                'source': feed['name'],
                'time': format_time(item['pubDate']),
                'link': item['link']
            })
    
    news_data = {
        'updateTime': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'news': all_
news[:10]
    }
    
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已更新 {len(news_data['news'])} 条新闻")

if __name__ == '__main__':
    main()