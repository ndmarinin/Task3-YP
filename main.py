from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from models import *
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
app = FastAPI(title="Cервис для проведения промоакций и розыгрышей призов.")


class Status(BaseModel):
    message: str


@app.post("/promo/{promo_id}/participant")
async def create_participant(participant: ParticipantIn_Pydantic, promo_id: int):
    participant_obj = await Participant.create(**participant.dict(exclude_unset=True))
    my_promo = await Promo.filter(id=promo_id)
    my_promo[0].participants.append(participant_obj)
    return participant_obj.id

@app.post("/promo")
async def create_promo(promo: PromoIn_Pydantic):
    promo_obj = await Promo.create(**promo.dict(exclude_unset=True))
    return promo_obj.id

@app.get("/promo", response_model=List[Promo_Pydantic])
async def get_promos():
    return await Promo_Pydantic.from_queryset(Promo.all())

@app.delete("/promo/{promo_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_promo(promo_id: int):
    deleted_count = await Promo.filter(id=promo_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Promo {promo_id} not found")
    return Status(message=f"Deleted promo {promo_id}")

@app.put(
    "/promo/{promo_id}", response_model=Promo_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_promo(promo_id: int, promo: PromoIn_Pydantic):
    await Promo.filter(id=promo_id).update(**promo.dict(exclude_unset=True))
    return await Promo_Pydantic.from_queryset_single(Promo.get(id=promo_id))

@app.get(
    "/promo/{promo_id}", response_model=Promo_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_promo(promo_id: int):
    return await Promo_Pydantic.from_queryset_single(Promo.get(id=promo_id))

register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
