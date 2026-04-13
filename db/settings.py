import json
import os
from pydantic import BaseModel
from typing import Optional


class BaseSettings(BaseModel):
    """
    JSON 파일 기반 동적 시스템 설정 관리 기반 클래스.
    프로젝트별로 이 클래스를 상속하여 필요한 설정 필드를 추가합니다.

    Usage:
        # my_project/settings.py
        from common_core.db.settings import BaseSettings, load_settings, save_settings

        class AppSettings(BaseSettings):
            feature_flag: bool = False
            max_users: int = 100

        settings = load_settings(AppSettings, "app/settings.json")
    """
    app_name: str = "My App"
    debug: bool = False


def load_settings(model_class: type, filepath: str) -> BaseModel:
    """
    JSON 파일에서 설정을 불러옵니다. 파일이 없으면 기본값으로 생성합니다.

    Args:
        model_class: BaseSettings를 상속한 Pydantic 모델 클래스
        filepath:    설정 파일 경로 (예: "app/settings.json")

    Returns:
        설정 모델 인스턴스
    """
    if not os.path.exists(filepath):
        default = model_class()
        save_settings(default, filepath)
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return model_class(**data)
    except Exception as e:
        print(f"[Settings] 로드 오류 ({filepath}): {e} — 기본값 사용")
        return model_class()


def save_settings(settings: BaseModel, filepath: str) -> None:
    """
    설정 모델 인스턴스를 JSON 파일로 저장합니다.

    Args:
        settings: 저장할 설정 모델 인스턴스
        filepath: 저장 경로
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(settings.dict(), f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Settings] 저장 오류: {e}")
