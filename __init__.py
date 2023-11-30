import uvicorn
from logger import logs
logger = logs.config_log(log_name='track-log')
from fastapi import FastAPI, UploadFile, File, Form,status
from fastapi.responses import JSONResponse, FileResponse
import os
import uuid
from settings import *
from connections.conn import *
from typing import Optional
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from typing import Optional
from pydantic import BaseModel
import time
import requests
import json
import re
from bs4 import BeautifulSoup
from fastapi.responses import StreamingResponse
import httpx