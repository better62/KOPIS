import requests
import xml.etree.ElementTree as ET
import datetime
from datetime import timedelta

service_key = "9e01c797c9504aa68b51104412042f2a"

def region_analysis(region, stdate, eddate):

    url = "http://www.kopis.or.kr/openApi/restful/prfstsArea?service={}&stdate={}&eddate={}&newsql=Y".format(service_key, stdate, eddate)
    response = requests.get(url)
    
    result = []
    if response.status_code == 200:
        root = ET.fromstring(response.content)
    
        for child in root:
            tmp = []
            for c in child:
                if c.tag == "fcltycnt":
                    tmp.append(("공연시설", format(int(c.text), ',')))
                elif c.tag == "prfplccnt":
                    tmp.append(("공연장", format(int(c.text), ',')))
                elif c.tag == "seatcnt":
                    tmp.append(("좌석수", format(int(c.text), ',')))
                elif c.tag == "prfprocnt":
                    tmp.append(("개막편수", format(int(c.text), ',')))
                elif c.tag == "prfcnt":
                    tmp.append(("공연건수", format(int(c.text), ',')))
                elif c.tag == "nmrs":
                    tmp.append(("판매수", format(int(c.text), ',')))
                elif c.tag == "nmrcancl":
                    tmp.append(("취소수", format(int(c.text), ',')))
                elif c.tag == "totnmrs":
                    tmp.append(("티켓판매수", format(int(c.text), ',')))
                elif c.tag == "amount":
                    tmp.append(("티켓판매액", format(int(c.text),',')))
                elif c.tag == "area" and c.text == region:
                    result.append(tmp)

    return result