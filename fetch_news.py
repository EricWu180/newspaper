import json
import requests
from datetime import datetime

# ⚠️ 替换成你的 API Key
API_KEY = '0c91863211557aa1efea0cec5d111e5f'

def fetch_news():
    try:
        url = f'http://api.tianapi.com/general/index?key={API_KEY}&num=10'
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data['code'] == 200:
            news = []
            for item in data['newslist'][:10]\:
                news.append({
                    'title': item['title'],
                    'source': item['source'] or '未知',
                    'time': format_time(item['ctime'])
                })
            return news
        else:
            print(f"API 错误：{data.get('msg', '未知错误')}")
            return []
    except Exception as e:
        print(f"API 抓取失败：{e}")
        return []

def format_time(time_str):
    try:
        date = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        now = datetime.now()
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
    news = fetch_news()
    if not news:
        news = [{'title': '【系统】新闻加载失败，请检查 API Key', 'source': '系统', 'time': '刚刚'}]
    
    news_data = {
        'updateTime': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'news': news
    }
    
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已更新 {len(news)} 条新闻")

if __name__ == '__main__':
    main()
