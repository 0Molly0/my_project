from datetime import datetime
from fastapi import FastAPI, status, Request, Form
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

from storage import database as db

app = FastAPI()
templates = Jinja2Templates(directory='templates')


# API
class NewStory(BaseModel):
    author: str
    title: str
    story: str


class Stories(NewStory):
    pk: int
    created_at: datetime


def _serialize_stories(story: list[tuple]) -> list[Stories]:
    story_serialized = [
        Stories(
            pk=stories[0],
            author=stories[1],
            title=stories[2],
            story=stories[3],
            created_at=stories[4],
        )
        for stories in story
    ]
    return story_serialized


@app.post("/api/add_story", status_code=status.HTTP_201_CREATED, tags=['API'])
def add_story(story: NewStory):
    db.add_story(author=story.author, title=story.title, story=story.story)
    return story


@app.get("/api/get_five_stories", tags=['API'])
@app.post("/api/get_five_stories", tags=['API'])
def get_stories() -> list[Stories]:
    story = db.get_first_five_newest()
    return _serialize_stories(story)


@app.get("/api/get_stories_search", tags=['API'])
def get_stories_search(query_str: str) -> list[Stories]:
    story = db.get_stories_by_title(query_str=query_str)
    return _serialize_stories(story)


# WEB

@app.get('/', tags=['web'], include_in_schema=False)
def main(request: Request):
    context = {
        'request': request,
    }

    return templates.TemplateResponse('add_story.html', context=context)


@app.get('/all-stories', tags=['WEB'])
@app.post('/search', tags=['WEB'])
def all_stories(request: Request, search_text: str = Form(None)):
    if search_text:
        stories = db.get_stories_by_title(query_str=search_text)
    else:
        stories = db.get_first_five_newest()
    stories_serialized = _serialize_stories(stories)
    context = {
        'title': f'Search result for text {search_text}' if search_text else 'Our books',
        'request': request,
        'stories': stories_serialized,
    }

    return templates.TemplateResponse('all_stories.html', context=context)


@app.get('/add-story', tags=['WEB'])
def all_story(request: Request):
    context = {
        'title': 'Add your story',
        'request': request,
    }

    return templates.TemplateResponse('add_story.html', context=context)


@app.post('/add-story', tags=['WEB'])
def all_story_final(
    request: Request,
    title: str = Form(),
    author: str = Form(),
    story: str = Form(),
):
    db.add_story(author=author, title=title, story=story)

    stories = db.get_first_five_newest()
    stories_serialized = _serialize_stories(stories)
    context = {
        'title': 'Add your story',
        'request': request,
        'stories': stories_serialized,
    }

    return templates.TemplateResponse('all_stories.html', context=context)
