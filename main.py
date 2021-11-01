import random
from typing import Optional

import httpx
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field, validator
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()


class PlanetModel(BaseModel):
    name: str = Field(..., description='Name of the planet')
    population: Optional[int] = Field(None, description='Population')

    @validator('population', pre=True)
    def validate_population(cls, value):
        if value == 'unknown':
            return None
        return value


@app.get(
    path='/api/v1/planets',
    response_model=list[PlanetModel]
)
async def characters() -> list[dict]:
    """
    Planets in Star Wars
    """
    async with httpx.AsyncClient() as client:
        response = await client.get('https://swapi.dev/api/planets')
        return [planet for planet in response.json()['results']]


templates = Jinja2Templates(directory="templates/")


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse(
        'thumbsup.html',
        {
            'request': request,
            'name': random.choices(
                ['Jonas', 'Ingvald', 'Stine', 'Vibeke', 'Bendik', 'Hans Olav'],
                weights=[50, 10, 10, 10, 10, 10],
                k=1
            )[0]
        }
    )
