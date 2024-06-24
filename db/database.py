import asyncio
import aiosqlite

"""
INSERT INTO users(ID, NICKNAME, URL, SUBSCRIPTION_STATUS) VALUES(?, ?, ?, ?)

SELECT * FROM users WHERE ID = ?
async for row in cursor:
    return row
"""


class UserBase:
    def __init__(self, basename):
        self.basename = basename

        # asyncio.run(self.check_db())

    async def check_db(self):
        async with aiosqlite.connect(self.basename) as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS users (
                `ID` INTEGER,
                USERNAME TEXT,
                URL TEXT
            )
            """)

            await db.execute("""CREATE TABLE IF NOT EXISTS gifts (
                `ID` INTEGER,
                title TEXT,
                PRICE TEXT,
                PRICE_SEGMENT TEXT,
                DESCRIPTION TEXT,
                LINKS TEXT DEFAULT (0),
                IS_BOOKED INTEGER DEFAULT (0)
            )
            """)

            await db.commit()

    #-------------------------------------- USER ------------------------------------------------------------#
    async def add_user(self, id: int, username: str, url: str):
        async with aiosqlite.connect(self.basename) as db:
            await db.execute("""INSERT INTO users(ID, USERNAME, URL) VALUES(?, ?, ?)""", (id, username, url))
            await db.commit()

    async def get_user(self, id: int):
        async with aiosqlite.connect(self.basename) as db:
            async with db.execute("""SELECT * FROM users WHERE ID = ?""", [id]) as cursor:
                async for row in cursor:
                    return row

    #-------------------------------------- GIFT -------------------------------------------------------------#
    async def add_gift(self, title: str, price: str, description: str, links: list):
        links = '|'.join(links)

        async with aiosqlite.connect(self.basename) as db:
            await db.execute("""INSERT INTO gifts(ID, TITLE, PRICE, DESCRIPTION, LINKS) VALUES(?, ?, ?, ?, ?)""", (id, title, price, description, links))
            await db.commit()

    async def edit_gift(self, id: int, new_title: str, new_price: str, new_description: str, new_links: list):
        async with aiosqlite.connect(self.basename) as db:
            await db.execute("""UPDATE gifts SET TITLE = ?, PRICE = ?, DESCRIPTION = ?, LINKS = ? WHERE ID = ?""", (new_title, new_price, new_description, new_links, id))
            await db.commit()

    async def get_gift(self, id: int):
        async with aiosqlite.connect(self.basename) as db:
            async with db.execute("""SELECT * FROM gifts WHERE ID = ?""", [id]) as cursor:
                async for row in cursor:
                    return row
                
    async def get_gifts(self, segment: str):
        async with aiosqlite.connect(self.basename) as db:
            async with db.execute("""SELECT * FROM gifts WHERE PRICE_SEGMENT = ?""", (segment, )) as cursor:
                return [row async for row in cursor]
            
    async def get_count_gifts(self):
        async with aiosqlite.connect(self.basename) as db:
            async with db.execute("""SELECT * FROM gifts""") as cursor:
                return len([row async for row in cursor])
            
    async def get_all_gifts(self):
        async with aiosqlite.connect(self.basename) as db:
            async with db.execute("""SELECT * FROM gifts""") as cursor:
                return [row async for row in cursor]

    async def remove_gift(self, id: int):
        async with aiosqlite.connect(self.basename) as db:
            await db.execute("""DELETE FROM gifts WHERE ID = ?""", (id,))
            await db.commit()

    async def add_booked_user(self, id_user: int, id_gift: int):
        async with aiosqlite.connect(self.basename) as db:
            await db.execute("""UPDATE gifts SET IS_BOOKED = ? WHERE ID = ?""", (id_user, id_gift))
            await db.commit()

    async def remove_booked_user(self, id_gift: int):
        async with aiosqlite.connect(self.basename) as db:
            await db.execute("""UPDATE gifts SET IS_BOOKED = ? WHERE ID = ?""", (0, id_gift))
            await db.commit()

    async def get_booked_gifts(self, id_user: int):
        async with aiosqlite.connect(self.basename) as db:
            async with db.execute("""SELECT * FROM gifts WHERE IS_BOOKED = ?""", [id_user]) as cursor:
                return [row async for row in cursor]