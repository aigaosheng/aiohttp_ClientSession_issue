# aiohttp_ClientSession_issue
Investigate aiohttp.ClientSession randomly failure when batch calling APIs, e.g. Client error for XXX: Can not write request body for API_URL

# What is the issue?
The issue happends when you call your API endpoint (e.g. FastAPI server) from server side using batch. Normally we use asynchronous + semaphore + aiohttp to control traffic sent to server. Sometimes, it works fine. Sometime server return nothing, and the client catch errors, e.g. Client error for XXX: Can not write request body for server_url, e.g. http://0.0.0.0:port/...
Googling cannot find the reason what causes the issue. After reading the aiohttp.ClientSession source code, I guess the issue maybe caused by Timeout setting when calling ClientSession. Almost all use default setting. But default Timeout, total = 300 seconds. It maybe enough for adhoc usage. But for production, e.g. your server need to call OpenAPI API to do reasoning and process, only 1 openai API call may spending a few seconds (e.g. 6s, or even more > 10s in multi-modality & long response, e.g 2K output token). 
The issue looks randomly. You cannot repeat. 
The project is to test whether the issue is caused by Timeout.
