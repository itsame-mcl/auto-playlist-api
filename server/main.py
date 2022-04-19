import server.theaudiodb_api as tadb
import server.lyricsovh_api as lyrs
from fastapi import FastAPI
from fastapi_health import health


app = FastAPI()
app.add_api_route(
    "/", health(conditions=[tadb.check_tadb_health, lyrs.check_lyrs_health]))
