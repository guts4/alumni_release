from django.shortcuts import render, redirect
import requests
import json
from django.template import loader
from django.http import HttpResponse, JsonResponse


def test(request):
    _data = {
        "data": [
            {
                "title": "트로트",
                "datas": [
                    {'title': '노래제목1', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목1', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목1', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목1', 'name': '가수', 'des': '가사'},
                ]
            },
            {
                "title": "댄스",
                "datas": [
                    {'title': '노래제목2', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목2', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목2', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목2', 'name': '가수', 'des': '가사'},
                ]
            },
            {
                "title": "힙합",
                "datas": [
                    {'title': '노래제목3', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목3', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목3', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목3', 'name': '가수', 'des': '가사'}
                ]
            }
        ]
    }
    return JsonResponse(_data)

def index(request):
    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'index.html', _context)

def kakaoLoginLogic(request):
    _restApiKey = '' # 입력필요
    _redirectUrl = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)

def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code']
    _restApiKey = '' # 입력필요
    _redirect_uri = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
    _res = requests.post(_url)
    _result = _res.json()
    request.session['access_token'] = _result['access_token']
    request.session.modified = True
    return render(request, 'loginSuccess.html')

def kakaoLogout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/logout'
    _header = {
      'Authorization': f'bearer {_token}'
    }
    # _url = 'https://kapi.kakao.com/v1/user/unlink'
    # _header = {
    #   'Authorization': f'bearer {_token}',
    # }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    if _result.get('id'):
        del request.session['access_token']
        return render(request, 'loginoutSuccess.html')
    else:
        return render(request, 'logoutError.html')

def methodsCheck(request, id):
    if(request.method == 'GET'):
        print(f"GET QS : {request.GET.get('data', '')}")
        print(f"GET Dynamic Path : {id}")
    
    # PostMan으로 Localhost 테스트를 위해 CSRF 해제
    # project/settings.py 파일에서 
    # MIDDLEWARE -> 'django.middleware.csrf.CsrfViewMiddleware' 주석 처리
    elif(request.method == 'POST'):
        print(f"POST QS : {request.GET.get('data', '')}")
        print(f"POST Dynamic Path : {id}")
        return HttpResponse("POST Request.", content_type="text/plain")
    return render(request, 'methodGet.html')