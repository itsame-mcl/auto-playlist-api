from . import theaudiodb_api as tadb
from fastapi import FastAPI
from fastapi_health import health


app = FastAPI()
app.add_api_route("/", health(conditions=[tadb.check_api_health]))
