# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import sys
from bs4 import BeautifulSoup
import requests, re, json
from datetime import datetime


def getHtml(url):
    html = ""
    req = requests.get(url)  # html get request
    if req.status_code == 200:  # 1xx : informational, 2xx : success, 3xx : redirection, 4xx : client error, 5xx : server error
        html = req.text  # html 소스 텍스트로 변환
    return html


def today_lunch():
    schoolMealCode = 2  # 1 아침 2 점심 3 저녁
    schoolYmd = datetime.today().strftime("%Y.%m.%d")  # 오늘 날짜 연.월.일 문자열
    weekday = datetime.today().weekday() + 1
    neis = (
            "https://stu.dje.go.kr/sts_sci_md01_001.do?"
            "schulCode=G100000167"
            "&schulCrseScCode=4"
            "&schulKndScCode=04"
            "&schMmealScCode=%d&schYmd=%s" % (schoolMealCode, schoolYmd)
    )
    html = getHtml(neis)  ## BeautifulSoup으로 html소스를 python객체로 변환
    soup = BeautifulSoup(html, "html.parser")  ## 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시.
    element = soup.find_all("tr")
    element = element[2].find_all('td')
    try:
        element = element[weekday]
        element = str(element)
        element = element.replace('<br/>', '\n')  # 필요 없는 텍스트 지움
        element = element.replace('</td>', '')
        element = element.replace('<td class="textC">', '')
        element = element.replace('.', '')
        element = element.replace('<td class="textC last">', '')
        element = re.sub(r'\d', '', element)
        if element == " ":  # 지웠을 때 남은 텍스트가 없으면 급식 없다고 리턴
            element = '\n급식이 없습니다.'
    except:
        element = "\n급식이 없습니다."  # element[weekday]가 없으면 오류 메세지 대신 리턴

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


def month_schedule():
    strSchedule = ""
    neis = (
        "https://stu.dje.go.kr/sts_sci_sf01_001.do?schulCode=G100000167&schulKndScCode=04&schulCrseScCode=4"
    )
    html = getHtml(neis)
    soup = BeautifulSoup(html, "html.parser")

    div = soup.find_all('div', {"class" : "textL"})

    for element in div:
        strSchedule += element.text

    return strSchedule


app = Flask(__name__)




@app.route('/welcome', methods=['POST'])
def welcome():
    content = request.get_json()  # return json data
    content = content['userRequest']  # json 포맷
    content = content['utterance']

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "hello world!"
                    }
                }
            ]
        }
    }

    return jsonify(res)


@app.route('/lunch', methods=['POST'])
def lunch():
    content = request.get_json()  # return json data
    content = content['userRequest']  # json 포맷
    content = content['utterance']  # 사옹자 발화

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": today_lunch()
                    }
                }
            ]
        }
    }

    return jsonify(res)


@app.route('/dinner', methods=['POST'])
def dinner():
    content = request.get_json()  # return json data
    content = content['userRequest']  # json 포맷
    content = content['utterance']  # 사옹자 발화

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": today_dinner()
                    }
                }
            ]
        }
    }

    return jsonify(res)

@app.route('/schedule', methods=['POST'])
def schedule():

    content = request.get_json()  # return json data
    content = content['userRequest']  # json 포맷
    content = content['utterance']  # 사옹자 발화

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": month_schedule()
                    }
                }
            ]
        }
    }

    return jsonify(res)

@app.route('/fallback', methods=['POST'])
def fallback():
    content = request.get_json()  # return json data
    content = content['userRequest']  # json 포맷
    content = content['utterance']  # 사옹자 발화

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": '올바르지 않은 명령어입니다. \n 명령어 목록은 /help를 치면 출력됩니다.'
                    }
                }
            ]
        }
    }

    return jsonify(res)

@app.route('/place', methods = ['POST'])
def place():
    content = request.get_json()
    content = content['userRequest']
    content = content['utterance']

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": '네이처 - 네이처 게임랜드 2-2\n로고스 - 로고스 노래마당 수학실 수학카페\n마루 - 마루 지식회사 2-10\n메디컬 신드롬 - 폐병원의 비밀 예절실\n메이커스 - 레트로 카페, 조명 포토존&3D펜 체험 2-3\n빛나리 - 내일보다 빛나는 축제 영어전용교실\n아톰 - Merry 아톰 Mas 2-4\n이오 - 상큼하게 터져볼래? 제2외국어실\n익시드 - 호러 익시드 2-9\n프린키피아 - 향기나는 프린키피아 제2외국어실\nSCI와 함께 크리스마스를 2-11\n도래샘 - 민속촌 2-5\n메이트 - 크리스마스 메이트 2-6\n미라클 - 케빈을 피해랏! 물리실\n미르 - 미르 사진관\n사계동화 - 별 헤는 밤 지구과학실\n유네스코 - 유네스튜디오 2-7\n이젤 - 이젤 공방 지구과학실\n저스티스 - 저스티스 야놀자 2-8'
                    }
                }
            ]
        }
    }

    return jsonify(res)

@app.route('/help', methods = ['POST'])
def help():
    content = request.get_json()
    content = content['userRequest']
    content = content['utterance']

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": '오늘 점심, 오늘 석식, 동아리 부스'
                    }
                }
            ]
        }
    }

    return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)