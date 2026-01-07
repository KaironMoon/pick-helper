import base64

from ai_microservice import WebAppSettings
from ai_microservice.settings import DotEnvSettings, Setting
from pydantic import Field

# 기본적으로 WebAppSettings를 상속받는다.
# 프로젝트 별로 설정을 추가할 때 사용한다.
# 새로운 옵션을 추가할 경우에는 아래와 같이 선언하여 Settings에 추가한다.

# 예시
# .dev.env 에는 
# PROJECT_SPECIFIC__BLABLA=blabla
# 와 같은 형식으로 추가한다.

class SampleSetting(Setting):
    config: str = Field(default="sample-config")
    secret: str = Field(default="sample-secret")
    url: str = Field(default="localhost")

class DBSetting(Setting):
    name: str = Field(default="pickhelper_db")
    port: str = Field(default="5432")
    host: str = Field(default="localhost")
    user: str = Field(default="admin")
    password: str = Field(default="admin")

class InnerSettings(DotEnvSettings):
    sample: SampleSetting = Field(default_factory=SampleSetting)
    db: DBSetting = Field(default_factory=DBSetting)

class ProjectSettings(WebAppSettings):
    sample: SampleSetting = Field(default_factory=SampleSetting)
    db: DBSetting = Field(default_factory=DBSetting)

    def __init__(self):
        super().__init__()

        # 설정 객체 생성
        config_settings = InnerSettings(_yaml_file="yaml/configmap.yaml")
        secret_settings = InnerSettings(_yaml_file="yaml/secret.yaml")
        config_domain_settings = InnerSettings(_yaml_file="yaml/configmap-domain.yaml")

        # 설정 값 복사 및 디코딩
        self.sample = config_settings.sample
        self.sample.secret = _maybe_decode(secret_settings.sample.secret)
        self.sample.url = config_domain_settings.sample.url

        # DB 설정
        self.db = config_settings.db
        self.db.host = config_domain_settings.db.host
        self.db.user = _maybe_decode(secret_settings.db.user)
        self.db.password = _maybe_decode(secret_settings.db.password)

# base64 디코딩이 필요한지 자동으로 처리하는 헬퍼 함수
def _maybe_decode(value: str) -> str:
    try:
        val = value.strip()
        val += '=' * (-len(val) % 4)
        return base64.b64decode(val).decode()
    except Exception:
        return value
