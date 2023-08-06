from concurrent import futures
import requests

def safeMapResToJson(results):
    res = []
    for r in results:
        try: res.append(r.json())
        except: res.append({})
    return res

def concurrentExecRequests(urls):
    with futures.ThreadPoolExecutor(max_workers=20) as executor:
        res = executor.map(executeAPICall,urls)
    return list(res)

def executeAPICall(url):
    return requests.get(url)