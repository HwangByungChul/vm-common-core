import logging
from datetime import datetime
from typing import Callable, Optional
from apscheduler.schedulers.background import BackgroundScheduler


logger = logging.getLogger(__name__)


class BaseScheduler:
    """
    APScheduler 기반 백그라운드 스케줄러 래퍼 클래스.
    이 클래스를 상속하여 프로젝트별 Job을 등록합니다.

    Usage:
        from common_core.scheduler import BaseScheduler

        class MyScheduler(BaseScheduler):
            def register_jobs(self):
                self.add_cron_job(my_daily_task, hour=7, minute=0, job_id="daily_task")
                self.add_interval_job(my_monitor, minutes=10, job_id="monitor")

        scheduler = MyScheduler()
        scheduler.start()
    """

    def __init__(self, timezone: str = "Asia/Seoul"):
        self._scheduler = BackgroundScheduler(timezone=timezone)
        self._timezone = timezone

    def add_cron_job(
        self,
        func: Callable,
        job_id: str,
        day_of_week: str = "mon-fri",
        hour: int = 9,
        minute: int = 0,
        **kwargs,
    ):
        """
        매일 특정 시각에 실행되는 Cron 잡을 등록합니다.

        Args:
            func:         실행할 함수
            job_id:       잡 고유 식별자 (중복 방지용)
            day_of_week:  실행 요일 (기본: "mon-fri" 평일만)
            hour:         실행 시 (0~23)
            minute:       실행 분 (0~59)
        """
        self._scheduler.add_job(
            func, "cron",
            day_of_week=day_of_week,
            hour=hour, minute=minute,
            id=job_id,
            **kwargs
        )
        logger.info(f"[스케줄러] Cron 잡 등록: {job_id} ({day_of_week} {hour:02d}:{minute:02d})")

    def add_interval_job(
        self,
        func: Callable,
        job_id: str,
        minutes: int = 10,
        **kwargs,
    ):
        """
        일정 간격(분)으로 반복 실행되는 잡을 등록합니다.

        Args:
            func:    실행할 함수
            job_id:  잡 고유 식별자
            minutes: 반복 간격 (분 단위, 기본: 10분)
        """
        self._scheduler.add_job(
            func, "interval",
            minutes=minutes,
            id=job_id,
            **kwargs
        )
        logger.info(f"[스케줄러] Interval 잡 등록: {job_id} ({minutes}분 주기)")

    def register_jobs(self):
        """
        서브클래스에서 재정의하여 프로젝트별 잡을 등록합니다.
        start() 호출 시 자동으로 실행됩니다.
        """
        pass

    def start(self):
        """스케줄러를 시작합니다."""
        self.register_jobs()
        self._scheduler.start()
        logger.info(f"[스케줄러] 시작됨 (timezone: {self._timezone})")

    def stop(self):
        """스케줄러를 안전하게 종료합니다."""
        self._scheduler.shutdown()
        logger.info("[스케줄러] 종료됨")
