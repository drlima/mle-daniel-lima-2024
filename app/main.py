from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .src.model import Model

app = FastAPI()
model = Model()


@app.get("/")
async def root():
    return RedirectResponse("/docs")


@app.get("/model-metrics")
async def get_model_metrics() -> dict[str, float]:
    return model.model_metrics


@app.get("/train")
async def train():
    model.train()
    return "Model trained"


@app.get("/test")
async def test():
    model.test()
    return model.model_metrics


@app.post("/predict")
async def predict(
    type: str,
    sector: str,
    net_usable_area: float,
    net_area: float,
    n_rooms: float,
    n_bathroom,
    latitude: float,
    longitude: float,
) -> dict[str, float]:
    return {
        "price": model.predict(
            type=type,
            sector=sector,
            net_usable_area=net_usable_area,
            net_area=net_area,
            n_rooms=n_rooms,
            n_bathroom=n_bathroom,
            latitude=latitude,
            longitude=longitude,
        )
    }
