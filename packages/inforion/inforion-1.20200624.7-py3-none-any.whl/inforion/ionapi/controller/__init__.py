
from inforion.ionapi.controller import *
from inforion.ionapi.model import * 

class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
    ):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter) 
    session.mount('https://', adapter)
    return session


    

def sendresults(url,headers, data,timeout=65):
    
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "POST","GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    
    
    
    try:
                    
        #response = requests.request("POST", url, headers=headers, data=json.dumps(data),timeout=15)
        response = http.request("POST", url, headers=headers, data=json.dumps(data),timeout=timeout)
               
        if response.status_code == 200:
            try:
                r =  response.json()        
    
            except ValueError:
                r = " JSON Error"
        else:
            r = "Error Respone Code" + str (response.status_code)
    except requests.exceptions.Timeout:
        print ("Timeout")
        r = "Error Timeout"
    except requests.exceptions.TooManyRedirects:
        print ("Too many redirects")
        r = "Error - Too many redirects"
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print ("OOps: Something Else",e)
        raise SystemExit(e)
        r = "Error"
    
    return r

def saveresults(r,df,program,index,chunk,elements=1):

    #print (r)
    max_elements = elements
    try:
        if chunk == 0:
            newindex = index - MaxChunk
        else:
            newindex = index - MaxChunk + chunk
        if newindex < 0: 
            newindex = 0
        cmethod = None
        if len(r)>0:
            if 'results' in r.keys():
                
                if len(r['results'])>0:
                    
                    for key in r['results']:

                        methode = key['transaction']
                        
                        
                        if 'errorMessage' in key:
                            message = key['errorMessage']
                            message = message.rstrip("\r\n")
                            message = ' '.join(message.split())
                            #print ("Fehler in Record " + str(i) + " " + message)
                            df.loc[newindex, methode] = message

                        else:
                            message = 'Ok'
                            df.loc[newindex, methode] = message
                        
                        if elements == 1:
                            newindex = newindex + 1
                            elements = max_elements
                        else:
                            elements = elements - 1

              
                else:
                    
                    df.loc[df.index.to_series().between(newindex,index), 'MESSAGE'] = "Results are empty"
            else:
                
                df.loc[df.index.to_series().between(newindex,index), 'MESSAGE'] = "Results are missing"
        else:
            for newindex in range(index):
                #print('Write JSON Error:', str(newindex))
                df.loc[newindex, 'MESSAGE'] = ' JSON Error'
    except:
        print (r)
        df.loc[df.index.to_series().between(newindex,index), 'MESSAGE'] = 'Unclear Error'


    chunk = MaxChunk
    data = {'program': program,
    'cono':    409 }
    
    return df, data,chunk

