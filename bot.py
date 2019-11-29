from flask import Flask, request, jsonify
import sys
from bs4 import BeautifulSoup
import requests, re, json
from datetime import datetime


def getHtml(url):
    html = ""
    req = requests.get(url)     #html get request
    if req.status_code == 200: #1xx : informational, 2xx : success, 3xx : redirection, 4xx : client error, 5xx : server error
        html = req.text #html 소스 텍스트로 변환
    return html


def today_lunch():
    schoolMealCode = 2 # 1 아침 2 점심 3 저녁
    schoolYmd = datetime.today().strftime("%Y.%m.%d") #오늘 날짜 연.월.일 문자열
    weekday = datetime.today().weekday() + 1
    neis = (
            "https://stu.dje.go.kr/sts_sci_md01_001.do?"
            "schulCode=G100000167"
            "&schulCrseScCode=4"
            "&schulKndScCode=04"
            "&schMmealScCode=%d&schYmd=%s" % (schoolMealCode, schoolYmd)
    )
    html = getHtml(neis)                        ## BeautifulSoup으로 html소스를 python객체로 변환
    soup = BeautifulSoup(html, "html.parser")   ## 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시.
    element = soup.find_all("tr")
    element = element[2].find_all('td')
    try:
        element = element[weekday]
        element = str(element)
        element = element.replace('<br/>', '\n')                    #필요 없는 텍스트 지움
        element = element.replace('</td>', '')
        element = element.replace('<td class="textC">', '')
        element = element.replace('.', '')
        element = element.replace('<td class="textC last">', '')
        element = re.sub(r'\d', '', element)
        if element == " ":                                          #지웠을 때 남은 텍스트가 없으면 급식 없다고 리턴
            element = '\n급식이 없습니다.'
    except:
        element = "\n급식이 없습니다."                                 #element[weekday]가 없으면 오류 메세지 대신 리턴

    return element



def today_dinner():
    schoolMealCode = 3  # 1 = 아침 2 = 점심 3 = 저녁
    schoolYmd = datetime.today().strftime("%Y.%m.%d")
    weekday = datetime.today().weekday() + 1
    neis = (
            "http://stu.dje.go.kr//sts_sci_md01_001.do?"
            "schulCode=G100000167"
            "&schulCrseScCode=4"
            "&schulKndScCode=04"
            "&schMmealScCode=%d&schYmd=%s" % (schoolMealCode, schoolYmd)
    )
    html = getHtml(neis)
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find_all("tr")
    element = element[2].find_all('td')
    try:
        element = element[weekday]
        element = str(element)
        element = element.replace('<br/>', '\n')
        element = element.replace('</td>', '')
        element = element.replace('<td class="textC">', '')
        element = element.replace('.', '')
        element = element.replace('<td class="textC last">', '')
        element = re.sub(r'\d', '', element)
        if element == " ":
            element = '\n급식이 없습니다.'
    except:
        element = "\n급식이 없습니다."

    return element


def today_schedule():       #미완성
    neis = (
            "http://stu.dje.go.kr//sts_sci_md01_001.do?"
            "schulCode=G100000167"
            "&schulCrseScCode=4"
            "&schulKndScCode=04"
            "&schMmealScCode=%d&schYmd=%s" % (schoolMealCode, schoolYmd)
    )
    html = getHtml(neis)
    soup = BeautifulSoup(html, "html.parser")


app = Flask(__name__)

'''@app.route('/keyboard')         #왜 있는지는 더 공부해야하는데 아무튼 있어야함
def keyboard():
    datasend = {
    }
    return jsonify(datasend)'''

@app.route("/message", methods = ['POST']) # post 방식으로 입력을 받음
def Message():
    content = request.get_json()           #return json data
    content = content['userRequest']       # json 포맷
    content = content['utterance']         # 사옹자 발화

    lunch = today_lunch()
    dinner = today_dinner()

    if content == u"start":                #u"text" 유니코드 문자열
        print('test start')
        datasend = {                       #스킬 응답
            "version" : "2.0",
            "template" : {
                "outputs" : [
                    {
                        "simpleText" : {
                            "text" : "hello"
                        }
                    }
                ]
            }
        }
    elif content == u"오늘점심":
        print('test lunch')
        datasend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": lunch
                        }
                    }
                ]
            }
        }
    elif content == u"오늘석식":
        print('test dinner')
        datasend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": dinner
                        }
                    }
                ]
            }
        }
    else:
        print('test asdf')
        datasend = {
            "version" : "2.0",
            "template" : {
                "outputs" : [
                    {
                        "simpleText" : {
                            "text" : "존재하지 않는 명령어입니다."
                        }
                    }
                ]
            }
        }
    return jsonify(datasend)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)