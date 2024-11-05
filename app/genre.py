import requests
import xml.etree.ElementTree as ET
import datetime
from datetime import timedelta

service_key = "9e01c797c9504aa68b51104412042f2a"

def genre_analysis(genre, stdate, eddate):
    url = "http://www.kopis.or.kr/openApi/restful/prfstsCate?service={}&stdate={}&eddate={}".format(service_key, stdate, eddate)
    response = requests.get(url)
    
    result = []
    if response.status_code == 200:
        root = ET.fromstring(response.content)
    
        for child in root:
            tmp = []
            for c in child:
                if c.tag == "prfprocnt":
                    tmp.append(("개막편수", format(int(c.text), ',')))
                elif c.tag == "prfdtcnt":
                    tmp.append(("상연횟수", format(int(c.text), ',')))
                elif c.tag == "amount":
                    tmp.append(("매출액", format(int(c.text), ',')))
                elif c.tag == "amountshr":
                    tmp.append(("매출액점유율", c.text))
                elif c.tag == "nmrs":
                    tmp.append(("관객수", format(int(c.text), ',')))
                elif c.tag == "nmrsshr":
                    tmp.append(("관객점유율", c.text))
                elif c.tag == "cate" and c.text == genre:
                    result.append(tmp)

    return result
