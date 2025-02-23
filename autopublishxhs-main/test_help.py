import json

import pytest
import requests

from xhs import help

from . import test_cookie


@pytest.fixture
def header():
    return {
        "cookie": test_cookie,
        "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                       "AppleWebKit/537.36 (KHTML, like Gecko)"
                       "Chrome/111.0.0.0 Safari/537.36")
    }


def test_sign():
    sign = help.sign("/api/sns/web/v1/user/otherinfo?"
                     "target_user_id=5ff0e6410000000001008400")
    print(sign)


@pytest.mark.skip(reason="sign is useless")
def test_sign_get(header):
    uri = ("/api/sns/web/v1/user/otherinfo?"
           "target_user_id=5ff0e6410000000001008400")
    cookie_dict = help.cookie_str_to_cookie_dict(header["cookie"])
    sign = help.sign(uri=uri, a1=cookie_dict.get("a1"))

    url = f"https://edith.xiaohongshu.com{uri}"

    headers = {
      'x-s': sign["x-s"],
      'x-t': sign["x-t"],
      'cookie': header['cookie'],
      'user-agent': header['user-agent'],
      "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    json_data = response.json()
    print(json_data)
    assert json_data["code"] == 0


@pytest.mark.skip(reason="sign is useless")
def test_sign_post(header):
    uri = "/api/sns/web/v1/feed"
    data = {"source_note_id": "63db8819000000001a01ead1"}
    cookie_dict = help.cookie_str_to_cookie_dict(header["cookie"])
    sign = help.sign(uri=uri, data=data, a1=cookie_dict.get("a1"))

    url = f"https://edith.xiaohongshu.com{uri}"

    payload = json.dumps(data, separators=(',', ':'))
    headers = {
      'x-s': sign["x-s"],
      'x-t': sign["x-t"],
      'cookie': header['cookie'],
      'user-agent': header['user-agent'],
      "Content-Type": "application/json"
    }
    print(headers)
    print(payload)
    response = requests.post(url, headers=headers, data=payload)
    json_data = response.json()
    print(json_data)
    assert json_data["code"] == 0


@pytest.mark.skip(reason="xhs website limit search numbers")
def test_search_id(header):
    search_id = help.get_search_id()
    uri = "/api/sns/web/v1/search/notes"
    data = {
      "keyword": "小红书",
      "page": 1,
      "page_size": 20,
      "search_id": search_id,
      "sort": "general",
      "note_type": 0
    }
    url = f"https://edith.xiaohongshu.com{uri}"
    sign = help.sign(uri=uri, data=data)
    payload = json.dumps(data,
                         separators=(',', ':'),
                         ensure_ascii=False).encode('utf-8')
    headers = {
      'x-s': sign["x-s"],
      'x-t': sign["x-t"],
      'cookie': header['cookie'],
      'user-agent': header['user-agent'],
      "Content-Type": "application/json"
    }
    print(headers)
    response = requests.post(url, headers=headers, data=payload)
    json_data = response.json()
    print(json_data)
    assert json_data["code"] == 0
    print(json_data["data"])


def test_cookie_to_dict():
    cookie = "a1=187d2defea8dz1fgwydnci40kw265ikh9fsxn66qs50000726043;webId=ba57f42593b9e55840a289fa0b755374;gid.sign=PSF1M3U6EBC/Jv6eGddPbmsWzLI=;gid=yYWfJfi820jSyYWfJfdidiKK0YfuyikEvfISMAM348TEJC28K23TxI888WJK84q8S4WfY2Sy;acw_tc=0ad5299117391796399982817e0f8dcb36836a9ec5f87b16910a2d9899f5c8;web_session=0400698c9f6a0a56f7cbe28e9c354bfc914eb8;"
    cookie_dict = help.cookie_str_to_cookie_dict(cookie)
    assert cookie_dict.get("a1")