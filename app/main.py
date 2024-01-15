from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer


from .src.model import Model


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def token_verification(token: str = Depends(oauth2_scheme)):
    if token != "fake_access_token":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token


app = FastAPI()
model = Model()


@app.post("/token")
async def generate_token():
    # In a real-world scenario,this would perform an actual authentication and generate a proper token
    return {"access_token": "fake_access_token", "token_type": "bearer"}


@app.get("/")
async def root(token: str = Depends(token_verification)):
    return RedirectResponse("/docs")


@app.get("/model-metrics")
async def get_model_metrics(token: str = Depends(token_verification)) -> dict[str, float]:
    return model.model_metrics


@app.get("/train")
async def train(token: str = Depends(token_verification)):
    model.train()
    return "Model trained"


@app.get("/test")
async def test(token: str = Depends(token_verification)) -> dict[str, float]:
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
    token: str = Depends(token_verification),
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
