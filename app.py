from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import logging
import os
import time

app = FastAPI()
@app.post('/')
async def endpoint(request: Request):
    try:
        data = await request.json()
        time.sleep(1)
        result = data
        return JSONResponse(result)
    except Exception as e:
        logging.warning(f"*** ERROR {e}")
        return JSONResponse(f"error ->{e}, , {data}")
    
if __name__ == "__main__":
    import multiprocessing
    mx_cpu_number = multiprocessing.cpu_count()
    n_worker = 1 
    uvicorn.run("test_error:app", port=5012, host='0.0.0.0', workers = 1, reload=True)
