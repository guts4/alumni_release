from django.db import models

class User(models.Model):
    kakao_id = models.CharField(max_length=255, unique=True, primary_key=True)
    
    # 추가 정보 입력
    phone_number = models.CharField(max_length=15, unique=True, default='000-000-0000')
    is_hearing_impaired = models.BooleanField(default=False)
    communication_method = models.CharField(max_length=255, null=True, blank=True)
