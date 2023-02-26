import asyncio, aiohttp, datetime
from more_itertools import chunked
from models import Session, Base, SwapiPeople, engine

CHUNK_SIZE = 10


async def get_people(session, page_id):
    async with session.get(f'https://swapi.dev/api/people/{page_id}') as response:
        json_data = await response.json()
        return json_data


async def paste_to_db(results):
    async with Session() as session:
        for swapi in results:
            try:
                name = swapi["name"]
                height = swapi["height"]
                mass = swapi["mass"]
                hair_color = swapi["hair_color"]
                skin_color = swapi["skin_color"]
                eye_color = swapi["eye_color"]
                birth_year = swapi["birth_year"]
                gender = swapi["gender"]
            except: pass
            try:
                url = swapi["homeworld"]
                async with aiohttp.ClientSession() as sess:
                    async with sess.get(url) as res:
                        data_1 = await res.json()
                        homeworld = data_1["name"]
            except:
                pass
            try:
                url_2 = swapi["vehicles"]
                vehicles = ""
                for i in url_2:
                    async with aiohttp.ClientSession() as sess:
                        async with sess.get(i) as res:
                            data_2 = await res.json()
                            vehicles += data_2["name"]
                            vehicles += ','
            except: pass
            try:
                url_3 = swapi["species"]
                species = ""
                for i in url_3:
                    async with aiohttp.ClientSession() as sess:
                        async with sess.get(i) as res:
                            data_3 = await res.json()
                            species += data_3["name"]
            except: pass
            try:
                url_4 = swapi["starships"]
                starships = ""
                for i in url_4:
                    async with aiohttp.ClientSession() as sess:
                        async with sess.get(i) as res:
                            data_4 = await res.json()
                            starships += data_4["name"]
                            starships += ','
            except: pass
            try:
                url_5 = swapi["films"]
                films = ""
                for i in url_5:
                    async with aiohttp.ClientSession() as sess:
                        async with sess.get(i) as res:
                            data_5 = await res.json()
                            films += data_5["title"]
                            films += ','
            except: pass

            swapi_people = SwapiPeople(name=name, height=height, mass=mass, hair_color=hair_color,
                                       skin_color=skin_color, eye_color=eye_color, birth_year=birth_year,
                                       gender=gender, homeworld=homeworld, vehicles=vehicles, species=species,
                                       starships=starships, films=films)
            session.add(swapi_people)
            await session.commit()


async def main():
    start = datetime.datetime.now()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with aiohttp.ClientSession() as session:
        coros = (get_people(session, i) for i in range(1, 85))
        for chunked_coros in chunked(coros, CHUNK_SIZE):
            results = await asyncio.gather(*chunked_coros)
            asyncio.create_task(paste_to_db(results))
    set_tasks = asyncio.all_tasks()
    for task in set_tasks:
        if task != asyncio.current_task():
            await task

    print(datetime.datetime.now() - start)


asyncio.run(main())
