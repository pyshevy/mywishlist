from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import aiosqlite

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/form", response_class=HTMLResponse)
async def get_form(request: Request, title: str = '', price: str = '', price_segment: str = '', description: str = '', links: str = '', task: str = 'add', id_gift: int = 0):
    data = {
        "links": links.split('|') if links else [],
        'task': task,
        "title": title,
        'price': price,
        'description': description,
        'price_segment': price_segment,
        'id_gift': id_gift
    }
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@app.post('/submit-form')
async def send_data(request: Request):
    data = await request.json()

    title = data.get("title")
    price = data.get("price", None)
    description = data.get("description", None)
    giftType = data.get("giftType", None)
    links = data.get("links", None)
    task = data.get("task", None)
    id_gift = data.get("id_gift", None)

    result = {
        "giftType": giftType,
        'task': task,
        'title': title,
        'description': description,
        'price': price,
        'links': links if giftType != 'book' else [],
        'id_gift': id_gift
    }

    print(result)

    # Закомментированный код для работы с базой данных
    path = os.path.dirname(os.path.abspath(__file__))
    path = path.removesuffix('\\sit')

    links = '|'.join(links)

    async with aiosqlite.connect(f"{path}\\bot\\db.db") as db:
        if task == 'add':
            await db.execute("""INSERT INTO gifts(ID, TITLE, PRICE, PRICE_SEGMENT, DESCRIPTION, LINKS) VALUES(?, ?, ?, ?, ?, ?)""", (id, title, price, giftType, description, links))
            await db.commit()
        elif task == 'edit':
            await db.execute("""UPDATE gifts SET TITLE = ?, PRICE = ?, DESCRIPTION = ?, LINKS = ? WHERE ID = ?""", (title, price, description, links, id_gift))
            await db.commit()
