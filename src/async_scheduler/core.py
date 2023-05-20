import asyncio
import datetime
import time
from asyncio import AbstractEventLoop
from logging import Logger, getLogger
from threading import Thread
from typing import Callable, Coroutine, Optional, Union

import schedule


class AsyncScheduler(schedule.Scheduler):
    __kill = None

    def __init__(
        self,
        *,
        loop: Optional[AbstractEventLoop] = None,
        logger: Optional[Logger] = None,
    ) -> None:
        """
        :type logger: you can specify a logger which will be used for logging (as default gets from getLogger)
        :param loop: event loop for async invoking, optional (as default gets from get_event_loop)
        """
        super().__init__()
        self.__loop = loop or asyncio.get_event_loop()
        self.__logger = logger or getLogger()

    def start(self) -> "AsyncScheduler":
        """
        Method for start schedule checking in second thread
        :return: this scheduler instance
        :raise Exception if thread is already started
        """
        if self.__kill is None or self.__kill == True:
            self.__kill = False
            Thread(target=self.__infinity_loop).start()
            self.__logger.debug("Schedule handling in second thread started")
        else:
            self.__logger.error("Schedule handling already started")
            raise Exception("Schedule handling already started")
        return self

    def stop(self) -> "AsyncScheduler":
        """
        Method for stop schedule checking in second thread
        :return: this scheduler manager instance
        :raise Exception if thread is not started
        """
        if not self.__kill:
            self.__kill = True
            self.__logger.debug("Schedule handling in second thread stopped")
        else:
            self.__logger.error("Schedule handling in second thread is not started")
            raise Exception("Schedule handling in second thread is not started")
        return self

    def __infinity_loop(self) -> None:
        """
        Method which controls schedule checking
        """
        while not self.__kill:
            self.run_pending()
            time.sleep(1)

    def do_task(
        self,
        for_run: Union[Callable, Coroutine, "AsyncTask"],
        once: bool = False,
        *args,
        **kwargs,
    ) -> Union[None, schedule.CancelJob]:
        """
        Synchronous method for run asynchronous task in event loop
        :param for_run: asynchronous function, Coroutine or AsyncTask which will be run
        :param once: is cancel task after doing? (Optional, as default False)
        :return: None or instance CancelJob
        """
        if asyncio.iscoroutine(for_run):
            coro = for_run
        elif asyncio.iscoroutinefunction(for_run):
            coro = for_run(*args, *kwargs)
        elif isinstance(for_run, AsyncTask):
            coro = for_run.func(*args, **kwargs)
        else:
            raise ValueError(
                "Parameter 'for_run' must be async function, coroutine or AsyncTask instance"
            )
        self.__logger.debug("Running asynchronous task in event loop")
        if self.__loop.is_running():
            result = self.__loop.create_task(coro)
        else:
            result = self.__loop.run_until_complete(coro)
        self.__logger.debug(f"Scheduled task result: {result}")
        if once:
            return schedule.CancelJob()

    def task(self, *, once: bool = False) -> Union[Callable, "AsyncTask"]:
        """
        decorator for register async function as scheduler task
        :param once: is cancel task after doing? (Optional, as default False)
        :return: instance of AsyncTask
        """

        def wrapper(func: Callable) -> AsyncTask:
            if not asyncio.iscoroutinefunction(func):
                raise ValueError("Function must be asynchronous")
            return AsyncTask(self, func, once)

        return wrapper

    def apply_task(
        self, at: str, for_run: Callable, once: bool = False, *args, **kwargs
    ) -> schedule.Job:
        """
        Method for add coroutine to scheduling as job
        :param at: timestring, in formats ("HH:mm:ss", "HH:mm")
        :param for_run: coroutine of function which will be run on schedule
        :param once: is cancel task after doing? (Optional, as default False)
        :return: instance of added job, can tag it for be able to cancel
        """
        job = self.every().day.at(at).do(self.do_task, for_run, once, *args, **kwargs)
        self.__logger.info(f"Saved job: {job}")
        return job


class AsyncTask:
    def __init__(
        self, scheduler: AsyncScheduler, func: Callable, once: bool = False
    ) -> None:
        """
        :param scheduler: instance of SchedulerTread which will be manage this task
        :param func: async function which will be call as task
        """
        self.scheduler = scheduler
        self.func = func
        self._at = None
        self.once = once

    def __call__(self, *args, **kwargs) -> Coroutine:
        """
        Method for to be able to call the function of this task
        :param args and :param kwargs: must match with args and kwargs of task function
        :return: coroutine from this task function
        """
        return self.func(*args, **kwargs)

    def at(self, _at: Union[datetime.datetime, str]) -> "AsyncTask":
        """
        Method for setting task execution time
        :param _at: timestring, in formats ("HH:mm:ss", "HH:mm")
        :return: this task instance
        """
        if isinstance(_at, datetime.datetime):
            _at_with_tz_offset = _at - datetime.timedelta(seconds=time.timezone)
            self._at = _at_with_tz_offset.time().isoformat(timespec="minutes")
        elif isinstance(_at, str):
            self._at = _at
        else:
            raise ValueError("wrong format")
        return self

    def do(self, *args, **kwargs) -> schedule.Job:
        """
        Method for add this task to scheduler as job
        :param args: and :param kwargs: must match with args and kwargs of task function
        :return: instance of added job, can tag it for be able to cancel
        """
        return self.scheduler.apply_task(self._at, self.func, self.once, *args, *kwargs)
