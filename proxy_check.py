import json
import asyncio
import aiohttp
import re

proxy = "YOUR_BRIGHTDATA_ROTATING_PROXY_URL_HERE"
tiktok_url = "https://www.tiktok.com/@therock"
instagram_url = "https://www.instagram.com/therock/" 

results = {
    "tiktok": {
        "200_count": 0,
        "captcha_count": 0
    },
    "instagram": {
        "200_count": 0,
        "captcha_count": 0
    }
}

async def check_tiktok(i):
    async with aiohttp.ClientSession() as session:
        async with session.get(tiktok_url) as response:
            html = await response.text()
            if not re.search("SIGI_STATE", html):
                results["tiktok"]["captcha_count"] += 1
            if response.status == 200:
                results["tiktok"]["200_count"] += 1
            print(f"TikTok task {i} done")

async def check_instagram(i):
    async with aiohttp.ClientSession() as session:
        async with session.get(instagram_url) as response:
            html = await response.text()
            if not re.search("Dwayne Johnson", html):
                results["instagram"]["captcha_count"] += 1
            if response.status == 200:
                results["instagram"]["200_count"] += 1
            print(f"Instagram task {i} done")

async def main():
    tasks = []
    for i in range(100):
        tasks.append(asyncio.create_task(check_instagram(i)))
        tasks.append(asyncio.create_task(check_tiktok(i)))

    for task in tasks:
        await task

    with open("bright_data_results.json", "w") as f:
        json.dump(results, f)

asyncio.run(main())
