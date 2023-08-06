"""-"""

import asyncio
import signal
import sys
from typing import Any, Awaitable, Callable, Union


def run_async(
        function: Callable[..., Awaitable[Any]],
        stop_flag: Union[asyncio.Event],
        debug: bool = False) -> None:
    """Calls asyncio.run with the specified function and
    sets a Proactor Event Loop on Windows.
    """

    async def __check_for_shutdown() -> None:
        """Wakes up the event queue in a specified interval"""
        while not stop_flag.is_set():
            await asyncio.sleep(0.1)

    async def __main() -> None:
        """Runs the main function and the shutdown check routine"""
        tasks = [
            asyncio.create_task(__check_for_shutdown()),
            asyncio.create_task(function())
        ]
        await asyncio.wait(
            tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in tasks:
            task.cancel()
        exceptions = await asyncio.gather(
            *tasks, return_exceptions=True)
        for exception in filter(None, exceptions):  # type: Exception
            if not isinstance(exception, asyncio.CancelledError):
                raise exception

    # Set ProactorEventLoop for Python < 3.8 on Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    asyncio.run(__main(), debug=debug)


def run_async_with_signals(
        function: Callable[..., Awaitable[Any]],
        debug: bool = False) -> None:
    """Extends asyncio.run to make it canceable when
    a shutdown signal is received on Windows.
    """

    stop_flag: asyncio.Event = asyncio.Event()

    def __signal_shutdown() -> Any:
        """-"""
        def _fn(*_: Any) -> None:
            stop_flag.set()
        return _fn

    signal.signal(signal.SIGTERM, __signal_shutdown())
    signal.signal(signal.SIGINT, __signal_shutdown())
    signal.signal(signal.SIGABRT, __signal_shutdown())

    if sys.platform == 'win32':
        signal.signal(signal.SIGBREAK, __signal_shutdown())

    run_async(function, stop_flag, debug)
