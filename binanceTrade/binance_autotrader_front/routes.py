from fastapi import Query, Request, Form
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND

# import db
from binance_autotrader_front.main import app, templates
from binance_autotrader_front.config import settings

from .db import current_session


@app.get("/")
async def home(request: Request):
    # prop = current_session.identity_map
    tpl = templates.TemplateResponse('index.html',
                                     {'request': request,
                                      'appName': settings.app_name,
                                      # 'info_session': prop
                                      }
                                     )
    print(settings.app_name)
    return tpl


@app.get("/cross")
async def cross(request: Request):
    # prop = current_session.identity_map
    tpl = templates.TemplateResponse('.html',
                                     {'request': request,
                                      'appName': settings.app_name,
                                      # 'info_session': prop
                                      }
                                     )
    print(settings.app_name)
    return tpl


@app.get("/userProfile")
async def userProfile(request: Request):
    # prop = current_session.identity_map
    tpl = templates.TemplateResponse('app/user-profile.html',
                                     {'request': request,
                                      'appName': settings.app_name,
                                      }
                                     )
    print(settings.app_name)
    return tpl


@app.get("/userPrivacy")
async def userPrivacy(request: Request):
    # prop = current_session.identity_map
    tpl = templates.TemplateResponse('app/user-privacy-setting.html',
                                     {'request': request,
                                      'appName': settings.app_name,
                                      }
                                     )
    print(settings.app_name)
    return tpl


@app.get("/signin")
async def signin(request: Request):
    # prop = current_session.identity_map
    tpl = templates.TemplateResponse('auth/sign-in.html',
                                     {'request': request,
                                      'appName': settings.app_name,
                                      }
                                     )
    print(settings.app_name)
    return tpl



# @app.post('/add')
# async def add(title: str = Form(...)):
#     new_todo = ToDo(title=title)
#     current_session.add(new_todo)
#     print('current_session.commit()')
#
#     url = app.url_path_for('home')
#     print('url')
#     return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
#
#
# @app.get('/update/{todo_id}')
# def update(todo_id: int):
#     todo = current_session.query(ToDo).filter(ToDo.id==todo_id).first()
#     todo.is_complete = not todo.is_complete
#     # current_session.commit()
#
#     url = app.url_path_for('home')
#     return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
#
#
# @app.get('/delete/{todo_id}')
# def delete(todo_id: int):
#     todo = current_session.query(ToDo).filter(ToDo.id==todo_id).first()
#     current_session.delete(todo)
#     # current_session.commit()
#
#     url = app.url_path_for('home')
#     return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#
#
# @app.get('/pair')
# async def get_pair(q: List[str] = Query(['ADAUSDT', '1h', 2], description='Search pair')):
#     return q