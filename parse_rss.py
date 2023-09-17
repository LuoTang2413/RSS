import asyncio
import aiohttp
import feedparser
import requests

async def parse_url(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                feed_content = await response.text()
                feed = feedparser.parse(feed_content)
                return feed.entries
            else:
                print(f"无法获取链接 {url}")
    except (aiohttp.ClientError, aiohttp.ClientConnectionError) as e:
        print(f"请求链接 {url} 时出现网络错误: {str(e)}")
    except feedparser.FeedParserError as e:
        print(f"解析链接 {url} 时出现错误: {str(e)}")

async def send_to_feishu(url, title, link):
    webhook_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/d6c7f1b5-3998-4b07-8504-cfb5a4e5b5c6'  # 替换为你的飞书机器人的Webhook URL
    message = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": "标题："
                            },
                            {
                                "tag": "a",
                                "text": title,
                                "href": link
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "链接："
                            },
                            {
                                "tag": "a",
                                "text": link,
                                "href": link
                            }
                        ]
                    ]
                }
            }
        }
    }

    response = requests.post(webhook_url, json=message)

    if response.status_code == 200:
        print("消息发送成功")

        # 保存推送的内容到文件
        with open("pushed_results.txt", "a") as file:
            file.write(message + "\n")
    else:
        print("消息发送失败")

async def main():
    async with aiohttp.ClientSession() as session:
        with open("RSS Feed URL.txt", "r") as file:
            urls = file.readlines()

        tasks = []
        for url in urls:
            url = url.strip()
            tasks.append(parse_url(session, url))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, list):
                for entry in result:
                    title = entry.title
                    link = entry.link
                    print("标题:", title)
                    print("链接:", link)
                    print("-----")
                    
                    await send_to_feishu(url, title, link)

asyncio.run(main())
