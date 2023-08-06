# -*- coding: utf-8 -*-
import timeit, time, sys
from .session import ProfilerSession
from pyinstrument_cext import setstatprofile
from pyinstrument.profiler import Profiler

try:
    from time import process_time
except ImportError:
    process_time = None

timer = timeit.default_timer


class Profiler(Profiler):

    def stop(self):
        setstatprofile(None)
        if process_time:
            cpu_time = process_time() - self._start_process_time
            self._start_process_time = None
        else:
            cpu_time = None

        self.last_session = ProfilerSession(
            frame_records=self.frame_records,
            start_time=self._start_time,
            duration=time.time() - self._start_time,
            sample_count=len(self.frame_records),
            program=' '.join(sys.argv),
            start_call_stack=self._start_call_stack,
            cpu_time=cpu_time,
        )
        return self.last_session
