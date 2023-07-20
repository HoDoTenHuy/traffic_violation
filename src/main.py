from fastapi import FastAPI
from uvicorn import run
from os import getenv

import utils.config
from routes.Note import initNoteRoutes

if __name__ == '__main__':
    app = FastAPI()

    initNoteRoutes(app)

    port = int(getenv('PORT'))
    run(app, host=getenv('HOST'), port=port)