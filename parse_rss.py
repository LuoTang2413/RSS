import feedparser

# 读取文件中的链接
with open("RSS Feed URL.txt", "r") as file:
    urls = file.readlines()

# 解析每个链接的内容
for url in urls:
    url = url.strip()  # 去除开头和结尾的空白字符
    feed = feedparser.parse(url)
    
    # 打印动态的标题和链接
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        print("标题:", title)
        print("链接:", link)
        print("-----")
