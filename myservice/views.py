from django.shortcuts import render, redirect
from .forms import AdditionalInfoForm
import requests
import json
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import datetime
import jwt
from jwt.exceptions import PyJWTError
from .models import User

settings.JWT_SECRET = 'your_jwt_secret_key'  # 원하는 비밀키로 교체하세요.
settings.JWT_ALGORITHM = 'HS256'

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
    _restApiKey = 'd80f6e50cc3a6fbd378d6150e0363537' # 입력필요
    _redirectUrl = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)

# 추가 회원가입을 위한 코드
def additional_info(request, kakao_id):
    user = User.objects.get(kakao_id=kakao_id)
    if request.method == 'POST':
        form = AdditionalInfoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('login_success')
    else:
        form = AdditionalInfoForm(instance=user)
    return render(request, 'additional_info.html', {'form': form})

def login_success(request):
    return render(request, 'loginSuccess.html')


def kakaoLoginLogicRedirect(request):
    try:
        _qs = request.GET.get('code')
        _restApiKey = 'd80f6e50cc3a6fbd378d6150e0363537'  # 입력필요
        _redirect_uri = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
        _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
        _res = requests.post(_url)
        _result = _res.json()

        # 오류 확인을 위한 로그 추가
        print("Token Response:", _result)

        if 'access_token' in _result:
            access_token = _result['access_token']
            
            # 사용자 정보 요청
            user_info_url = "https://kapi.kakao.com/v2/user/me"
            headers = {"Authorization": f"Bearer {access_token}"}
            user_info_res = requests.get(user_info_url, headers=headers)
            user_info = user_info_res.json()

            print("User Info Response:", user_info)

            # 사용자 정보가 성공적으로 반환되었는지 확인
            if 'id' in user_info:
                kakao_id = user_info.get('id')
                kuser, created = User.objects.get_or_create(kakao_id=kakao_id)
                print(created)
                # 새로운 사용자 여부 반환
                is_new_user = created

                # 새로운 사용자일 경우 추가 정보 입력 페이지로 리디렉션
                if is_new_user:
                    return redirect('additional_info', kakao_id=kakao_id)

                # JWT 토큰 생성
                jwt_payload = {
                    'access_token': access_token,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 만료 시간 설정
                }
                jwt_token = jwt.encode(jwt_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

                return JsonResponse({'token': jwt_token, 'is_new_user': is_new_user})
            else:
                print("Failed to retrieve user info:", user_info)
                return JsonResponse({'error': 'Failed to retrieve user info'}, status=400)
        else:
            print("Failed to get access token:", _result)
            return JsonResponse({'error': 'Failed to get access token'}, status=400)
    except KeyError as e:
        print(f"KeyError: {e}")
        return JsonResponse({'error': f"KeyError: {e}"}, status=500)
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return JsonResponse({'error': f"RequestException: {e}"}, status=500)
    except jwt.PyJWTError as e:
        print(f"JWTError: {e}")
        return JsonResponse({'error': f"JWTError: {e}"}, status=500)
    except Exception as e:
        # 예외 발생 시 오류 로그 출력
        print(f"Exception: {e}")
        return JsonResponse({'error': f"Internal Server Error: {e}"}, status=500)

def kakaoLogout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/logout'
    _header = {
      'Authorization': f'bearer {_token}'
    }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    if _result.get('id'):
        del request.session['access_token']
        return JsonResponse({'message': 'Logout success'})
    else:
        return JsonResponse({'message': 'Logout error'}, status=400)

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