import asyncio
from time import time

import biblebot
from biblebot.api.mileage import *
from biblebot.api._mileage import *
from biblebot.api.base import ErrorData, ResourceData
from aiohttp_socks import ProxyConnector

proxy = "socks5://127.0.0.1:9050"
# proxy = "http://89.204.214.142:8080"


async def test_login():
    # response = await Login.fetch("bible", "biblebot12", proxies=proxy)  # 아이디 없음
    # assert response.status == 200
    # result = Login.parse(response)
    # assert isinstance(result, ErrorData)

    # response = await Login.fetch("bible", "biblebot12", proxies=proxy)  # 비밀번호 틀림
    # assert response.status == 200
    # result = Login.parse(response)
    # assert isinstance(result, ErrorData)

    response = await Login.fetch("bibleCS1", "biblebot12", proxies=proxy)  # 정
    assert response.status == 200
    result = Login.parse(response)
    assert isinstance(result, ResourceData)
    return result.data["cookies"]


async def test_search(cookies):
    # response = await Search.fetch(cookies, proxies=proxy)
    # assert response.status == 200
    # result = Search.parse(response)
    # assert len(result.data["body"]) > 0
    # print("전체데이터", result)

    s = time()
    sid = "201504021"
    param = SearchParamData().set_student_id(sid)
    response = await Search.fetch(cookies, param, proxies=proxy)
    assert response.status == 200
    result = Search.parse(response)
    assert len(result.data["body"]) == 1
    i = result.data["head"].index("카드번호")
    assert result.data["body"][0][i] == sid
    print("학번 검색데이터", result)
    print(time() - s)
    # phone = ("010", "8714", "0965")
    # param = SearchParamData().set_phone_number(*phone)
    # response = await Search.fetch(cookies, param, proxies=proxy)
    # assert response.status == 200
    # result = Search.parse(response)
    # assert len(result.data["body"]) == 1
    # i = result.data["head"].index("회원명")
    # assert result.data["body"][0][i] == "김태희"
    # print("핸드폰 검색데이터", result)

    cid = "00001229"
    param = SearchParamData().set_customer_id(cid)
    response = await Search.fetch(cookies, param, proxies=proxy)
    assert response.status == 200
    result = Search.parse(response)
    assert len(result.data["body"]) == 1
    i = result.data["head"].index("회원번호")
    assert result.data["body"][0][i] == cid
    print("고객번호 검색데이터", result)

    page_size = "20"
    page_num = "2"
    param = SearchParamData().set_page_size(page_size).set_page_num(page_num)
    response = await Search.fetch(cookies, param, proxies=proxy)
    assert response.status == 200
    result = Search.parse(response)
    assert len(result.data["body"]) == int(page_size)
    print("페이지 사이즈 제한 검색데이터", result)


async def test_statement(cookies):
    s = time()
    response = await Statement.fetch(
        cookies, StatementParamData().set_customer_id("00001229"), proxies=proxy
    )
    assert response.status == 200
    result = Statement.parse(response)
    assert isinstance(result, ResourceData)
    print(result)
    print(time() - s)


async def test_invalid_cookies():
    invalid_cookies = {"JSESSIONID": "8CF7F1D7CA5BF96A18D723DEB6230FDF"}
    response = await Search.fetch(invalid_cookies, proxies=proxy)
    assert response.status == 200
    result = Search.parse(response)
    assert isinstance(result, ErrorData)

    response = await Statement.fetch(
        invalid_cookies,
        StatementParamData().set_customer_id("00001229"),
        proxies=proxy,
    )
    assert response.status == 200
    result = Statement.parse(response)
    assert isinstance(result, ErrorData)


async def main():
    cookies = await test_login()

    await test_search(cookies)
    await test_statement(cookies)

    await test_invalid_cookies()


asyncio.run(main())

# java.lang.NullPointerException
# java.lang.Exception: 9000╋세션정보가 없음.
