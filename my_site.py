import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import sys
from threading import Thread

from loader import base

main_dir = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
templates = Jinja2Templates(directory=f"{main_dir}/templates")

@app.get('/')
async def index():
    return {"answer": 'Ok!'}


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

    links = '|'.join(links)

    if task == 'add':
        await base.add_gift(
            id=id_gift,
            title=title,
            price=price,
            price_segment=giftType,
            description=description,
            links=links
        )

    elif task == 'edit':
        await base.edit_gift(
            new_title=title,
            new_price=price,
            new_price_segment=giftType,
            new_description=description,
            new_links=links,
            id=id_gift
        )

def start():
    uvicorn.run("my_site:app", host="0.0.0.0", port=int(os.getenv("PORT")), reload=False)

def keep_alive():
    t = Thread(target=start)
    t.start()
