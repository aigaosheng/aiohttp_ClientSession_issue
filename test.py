import os
import json
import asyncio
import aiohttp
import psycopg2
import pandas as pd
import random
import time

ENDPOINT_URL = "http://0.0.0.0:5012/"
BATCH_SIZE = 2 #50
INSERT_INTERVAL = 60

async def call_endpoint(session, company, date):
    """Calls the endpoint for a company with specified indicators. Handles errors and appends time taken."""
    start_time = time.perf_counter()  # Start time
    try:
        async with session.post(
            ENDPOINT_URL, json={"symbol": company, "latest_dt": date}
        ) as response:
            end_time = time.perf_counter()  # End time after receiving response
            time_taken = round(end_time - start_time, 2)  # Calculate time taken

            if response.status == 200:
                result = await response.json()
                result['time_taken'] = time_taken  # Append time taken to result
                return result
            else:
                print(f"Error calling endpoint for {company}: {response.status}")
                return None
    except aiohttp.ClientError as e:
        print(f"Client error for {company}: {e}")
        return None
    except aiohttp.http_exceptions.HttpProcessingError as e:
        print(f"HTTP error for {company}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error for {company}: {e}")
        return None
    
semaphore = asyncio.Semaphore(BATCH_SIZE)
company = [f"tt{tick}" for tick in range(100)]
timeout = aiohttp.ClientTimeout(total=1.01)#, sock_connect=0.2)
tt2 = aiohttp.ClientTimeout()
q1 = asyncio.Queue()
q2 = asyncio.Queue()
async def main():
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async def ff(ss, cc, dd):
            async with semaphore:
                    # Call the endpoint and get the response
                    response = await call_endpoint(ss, cc, dd)
                    print(f"****  {response}")
                    await q1.put('s')
        try:
            tsk = []
            for vv in company:
                tsk.append(asyncio.create_task(ff(session, vv, "date")))
            await asyncio.gather(*tsk)
        except Exception as e:
            print(f"*** err -> {e}")
            await q2.put('e')

asyncio.run(main())    
print(f"** success {q1.qsize()}, fail {q2.qsize()}")    
