import requests
import xml.etree.ElementTree as ET
import datetime
from datetime import timedelta

service_key = "9e01c797c9504aa68b51104412042f2a"

def date_analysis(stdate):
    ststype = "month"
    today = datetime.date.today()
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.strftime("%Y%m%d")
    eddate = yesterday[:4]

    if len(stdate)==4:
        date = stdate
        pass
    elif len(stdate)==8:
        ststype = "dayWeek"
        date = stdate[:4]+'-'+stdate[4:6]+'-'+stdate[6:]
        eddate = stdate
    elif len(stdate)==6:
        ststype = "day"
        date = stdate[:4]+'-'+stdate[4:6]
        eddate = yesterday[:6]

    url = "http://www.kopis.or.kr/openApi/restful/prfstsTotal?service={}&ststype={}&stdate={}&eddate={}&newsql=Y".format(service_key, ststype, stdate, eddate)
    response = requests.get(url)
    
    result = []
    tmp = []
    open, run, amount, people, cell, cancel = 0, 0, 0, 0, 0, 0

    if response.status_code == 200:
        root = ET.fromstring(response.content)

        for child in root:
            for c in child:
                if c.tag == "prfprocnt":
                    open += int(c.text)
                elif c.tag == "prfdtcnt":
                    run += int(c.text)
                elif c.tag == "amount":
                    amount += int(c.text)
                elif c.tag == "prfcnt":
                    people += int(c.text)
                elif c.tag == "ntssnmrs":
                    cell += int(c.text)
                elif c.tag == "cancelnmrs":
                    cancel += int(c.text)
                
    tmp.append(("개막편수", format(open, ',')))
    tmp.append(("상영횟수", format(run, ',')))
    tmp.append(("관객수", format(people, ',')))
    tmp.append(("판매수", format(cell, ',')))
    tmp.append(("취소수", format(cancel, ',')))
    tmp.append(("매출액", format(amount, ',')))
    tmp.append(("날짜", date))
    result.append(tmp)

    return result
