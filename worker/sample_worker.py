from common.settings import ProjectSettings
from config import get_settings


# class SampleWorker(AsyncIOScheduler): // 스케줄러의 경우
class SampleWorker():
    def __init__(self, _settings: ProjectSettings):
        self.settings = _settings

    def run(self):
        print(self.settings.project_specific.blabla)

if __name__ == "__main__":
    settings = get_settings()
    worker = SampleWorker(settings)
    worker.run()
