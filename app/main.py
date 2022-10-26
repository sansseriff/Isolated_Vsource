import uvicorn

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from fastapi import fastApi
from pydantic import BaseModel

from vsource_controll import isolatedVSource
from pathlib import Path




source_state = {1: {"voltage": 0.0, "state": 'off'},
                2: {"voltage": 0.0, "state": 'off'},
                3: {"voltage": 0.0, "state": 'off'},
                4: {"voltage": 0.0, "state": 'off'},}


app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")


# use this to define the base directory because otherwise correct directories aren't found in docker
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=Path(BASE_DIR, 'static')), name="static")


templates = Jinja2Templates(directory=Path(BASE_DIR, 'templates'))

class VoltageChange(BaseModel):
    voltage: float
    channel: int
    state: str



## initialize Vsource
source = isolatedVSource('10.7.0.162', 3, 5005, 55180, 1)
source.connect()


@app.get("/", response_class=HTMLResponse)
async def return_index(request: Request):
    obj = {"request": request, 
    "voltage_1": source_state[1]["voltage"],
    "voltage_2": source_state[2]["voltage"],
    "voltage_3": source_state[3]["voltage"],
    "voltage_4": source_state[4]["voltage"]}
    return templates.TemplateResponse("index.html", obj)


@app.post("/submit")
async def voltage_set(request: Request, change: VoltageChange):
    print("channel: ", change.channel, " voltage: ", change.voltage)
    change.voltage = round(change.voltage,3)
    # ch_string = "ch" + str(change.channel)
    if change.channel >= 1 and change.channel <= 4:
        if change.state == 'off':
            # source_state[change.channel]["voltage"] = 0
            source_state[change.channel]["voltage"] = change.voltage
            source_state[change.channel]["state"] = 'off'
            print("turning off ", change.channel)
            print(source_state)

            # the state voltage may be nonzero, but because current state
            # is off, set to 0. 
            source.setVoltage(change.channel, 0)
            return change
        else: # turning on or already on
            source_state[change.channel]["voltage"] = change.voltage
            print(source_state[change.channel])
            if source_state[change.channel]["state"] == 'off':
                print("turning on ", change.channel)
                source_state[change.channel]["state"] = 'on'
            print(source_state)
            # this is where you send a voltage
            source.setVoltage(change.channel, change.voltage)
            return change
    else:
        raise HTTPException(status_code=404, detail="Channel not 1-4")

@app.get("/read")
async def voltage_read(channel: int):
    return source_state[channel]

@app.get('/full-state')
async def state():
    return source_state

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)