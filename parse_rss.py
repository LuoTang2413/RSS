import asyncio
import aiohttp
import feedparser

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

asyncio.run(main())
