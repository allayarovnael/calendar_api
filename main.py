from fastapi import FastAPI, Form
from fastapi.responses import Response, FileResponse
from pydantic import BaseModel

import pandas as pd
from datetime import date

from feiertage import *

class Data(BaseModel):
    start_date: str
    end_date: str


app = FastAPI()

@app.get("/")
def index_page():
    with open('./templates/index.html', 'r') as f:
        export_page = f.read()
    return Response(export_page, media_type='text/html')


@app.post("/submitform")
def parse_user_input(start_date : str = Form(...), end_date : str = Form(...), time_choice : str = Form(...), geo_choice : str = Form(...)):
    
    report_name = '_'.join(['holidays_export', geo_choice, time_choice, start_date, end_date]) + '.csv'
    start_date = start_date.split('-')
    end_date = end_date.split('-')

    start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    end_date = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    report = FeiertagHandler(start_date=start_date, end_date=end_date, time_agg=time_choice, geo_agg=geo_choice)
    report_db = report.report_db
    #string = report.report_db.iloc[1,:].to_string()
    #return Response(string, media_type="text/html")
    report_db.to_csv(report_name, sep=';')
    #return FileResponse(path=report_db, filename=report_db, media_type='text/mp4')
