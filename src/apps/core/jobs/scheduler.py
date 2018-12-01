from datetime import datetime

from rq_scheduler.scheduler import Scheduler

from .queues import (
    parse_contracts
)


scheduler = Scheduler()

scheduler.schedule(
    scheduled_time=datetime.utcnow(),
    func=parse_contracts, args=(), kwargs={}, interval=60 * 60 * 4,
    repeat=None, timeout=600, description='Parsing contracts'
)
