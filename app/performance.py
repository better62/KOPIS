import requests
import xml.etree.ElementTree as ET
import datetime
from datetime import timedelta

service_key = "9e01c797c9504aa68b51104412042f2a"

def performance_analysis(performance):


    url = "http://www.kopis.or.kr/openApi/restful/prfstsPrfBy?service={}&cpage=1&rows=10&stdate=20100101&eddate=20241001&shprfnm={}".format(service_key, performance)
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)

        for child in root:
            for c in child:
                if c.tag == "mt20id":
                    performance_id = c.text
                    break

    url = "http://www.kopis.or.kr/openApi/restful/pblprfr/{}?service={}&newsql=Y".format(performance_id, service_key)
    response = requests.get(url)
    
    result = []
    if response.status_code == 200:
        root = ET.fromstring(response.content)
    
        for child in root:
            tmp = []
            for c in child:
                if c.tag == "prfcast":
                    tmp.append(("공연출연진", c.text))
                elif c.tag == "prfcrew":
                    tmp.append(("공연제작진", c.text))
                elif c.tag == "pcseguidance":
                    tmp.append(("티켓가격", c.text))
                elif c.tag == "prfpdfrom":
                    tmp.append(("공연시작일", c.text))
                elif c.tag == "prfpdto":
                    tmp.append(("공연종료일", c.text))
                elif c.tag == "fcltynm":
                    tmp.append(("공연시설명", c.text))
                elif c.tag == "dtguidance":
                    tmp.append(("공연시간", c.text))  
                elif c.tag == 'prfnm':
                    tmp.append(("공연명", c.text))  
            result.append(tmp)
            
    return result
