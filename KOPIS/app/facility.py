import requests
import xml.etree.ElementTree as ET
import datetime
from datetime import timedelta

service_key = "9e01c797c9504aa68b51104412042f2a"

def facility_analysis(facility):

    url = "http://www.kopis.or.kr/openApi/restful/prfplc?service={}&cpage=1&rows=5&shprfnmfct={}".format(service_key, facility)
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)

        for child in root:
            for c in child:
                if c.tag == "mt10id":
                    facility_id = c.text
                    break
    
    url = "http://www.kopis.or.kr/openApi/restful/prfplc/{}?service={}&newsql=Y".format(facility_id, service_key)
    response = requests.get(url)
    result = []
    if response.status_code == 200:
        root = ET.fromstring(response.content)

        for child in root:
            tmp = []
            for c in child:
                if c.tag == "fcltynm":
                    tmp.append(("공연시설명", c.text))
                elif c.tag == "opende":
                    tmp.append(("개관연도", c.text))
                elif c.tag == "fcltychartr":
                    tmp.append(("시설특성", c.text))
                elif c.tag == "seatscale":
                    tmp.append(("객석수", c.text))
                elif c.tag == "mt13cnt":
                    tmp.append(("공연장수", c.text))
                elif c.tag == "telno":
                    tmp.append(("전화번호", c.text))
                elif c.tag == "relateurl":
                    tmp.append(("홈페이지", c.text))
                elif c.tag == "adres":
                    tmp.append(("주소", c.text))
                elif c.tag == "restaurant":
                    tmp.append(("레스토랑", c.text))
                elif c.tag == "cafe":
                    tmp.append(("카페", c.text))
                elif c.tag == "store":
                    tmp.append(("상점", c.text))
                elif c.tag == "suyu":
                    tmp.append(("수유", c.text))
                elif c.tag == "parkbarrier":
                    tmp.append(("장애주차", c.text))
                elif c.tag == "restbarrier":
                    tmp.append(("장애화장실", c.text))
                elif c.tag == "runwbarrier":
                    tmp.append(("장애경사로", c.text))
                elif c.tag == "elevbarrier":
                    tmp.append(("장애엘리베이터", c.text))
            result.append(tmp)

    return result

