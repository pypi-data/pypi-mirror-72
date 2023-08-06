"""multiple time schedule Implementation."""

from datetime import timedelta
from celery import schedules
from .utils import subtract_time


class multipletime(schedules.BaseSchedule):
    """multiple time schedule."""

    def __init__(self, timezone, times,
                 model=None, nowfun=None, app=None):
        """Initialize multiple time."""
        self.timezone = timezone
        times.sort()
        self.times = times
        super(multipletime, self).__init__(nowfun=nowfun, app=app)

    def remaining_estimate(self, last_run_at):
        times = []
        for i in range(len(self.times)):
            if self.times[i] >= last_run_at.time():
                times = self.times[i:]
                break
        now_time = self.now().astimezone(self.timezone).time()
        if times:
            return subtract_time(times[0], now_time)
        else:
            return subtract_time(self.times[0], now_time) + timedelta(hours=24)

    def is_due(self, last_run_at):
        last_run_at = last_run_at.astimezone(self.timezone)
        rem_delta = self.remaining_estimate(last_run_at)
        remaining_s = max(rem_delta.total_seconds(), 0)
        if remaining_s == 0:
            return schedules.schedstate(is_due=True, next=0)
        return schedules.schedstate(is_due=False, next=remaining_s)

    def __repr__(self):
        return '<multipletime: {} {}>'.format(self.timezone, self.times)

    def __eq__(self, other):
        if isinstance(other, multipletime):
            return self.times == other.times and \
                self.timezone == other.timezone
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __reduce__(self):
        return self.__class__, (self.timezone, self.times)
