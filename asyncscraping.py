from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiohttp
import aiofiles
import asyncio
from aiocsv import AsyncWriter


async def get_products(url):
    ua = UserAgent()

    headers = {
        'User-Agent': f'{ua.random}'
    }

    async with aiohttp.ClientSession() as session:

        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')
        page_count = int(soup.find('div', class_='pagination ng-star-inserted').find_all('li', class_='pagination__item ng-star-inserted')[-1].text.strip())
        async with aiofiles.open('/home/novikov/Python_projects/scraping/rozetka_laptops/file/file.csv',
                                 'w') as file:
            writer = AsyncWriter(file, delimiter=' ')

            await writer.writerow((
                'Title',
                'Old_price',
                'New_price',
                'Status',
                'link',
            ))
        for page in range(1, page_count + 1):
            url = f'https://rozetka.com.ua/notebooks/c80004/goods_with_promotions=promotion;page={page}/'
            response = await session.get(url=url, headers=headers)
            soup = BeautifulSoup(await response.text(), 'lxml')
            items = soup.find_all('li', class_='catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted')
            for item in items:
                title = item.find('a', class_='goods-tile__heading ng-star-inserted').text.strip()
                try:
                    old_price = item.find('div', class_='goods-tile__prices').find('div',
                                                                                   class_='goods-tile__price--old price--gray ng-star-inserted').text.strip()
                    new_price = item.find('div', class_='goods-tile__prices').find('p',
                                                                                   class_='ng-star-inserted').text.strip()
                except:
                    old_price = 'NULL'
                    new_price = 'NULL'
                status = item.find('div', class_='goods-tile__availability').text.strip()
                link = item.find('a', class_='goods-tile__heading ng-star-inserted').get('href').strip()

                async with aiofiles.open('/home/novikov/Python_projects/scraping/rozetka_laptops/file/file.csv',
                                         'a') as file:
                    writer = AsyncWriter(file, delimiter=' ')

                    await writer.writerow((
                        title,
                        old_price,
                        new_price,
                        status,
                        link,
                    ))
        return f'/home/novikov/Python_projects/scraping/rozetka_laptops/file/file.csv'


async def main():
    await get_products('https://rozetka.com.ua/notebooks/c80004/goods_with_promotions=promotion/')


if __name__ == '__main__':
    asyncio.run(main())
