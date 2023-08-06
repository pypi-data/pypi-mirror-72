"""-"""

import asyncio
import logging
import os
import signal
import subprocess
from typing import Any, List, Optional

from nwsubprocess.process import ProcessHandle, get_run_flag_link_path


async def process_output(stream: Any, level: int) -> None:
    """-"""

    exec_logger = logging.getLogger("nw.execution")

    while True:
        try:
            data = await stream.readline()
            if not data:
                break
        except asyncio.CancelledError as ex:
            raise ex
        except Exception as ex:  # pylint: disable=broad-except
            exec_logger.critical("[EXECUTION] %s %s", type(ex).__name__, ex)

        try:
            line = data.decode('ascii').rstrip()
            exec_logger.log(level, line)
        except asyncio.CancelledError as ex:
            raise ex
        except Exception as ex:  # pylint: disable=broad-except
            exec_logger.critical("[EXECUTION] %s %s", type(ex).__name__, ex)


def terminate_process(process: Any) -> None:
    """-"""
    try:
        if os.name == "nt":
            # process.send_signal(signal.CTRL_C_EVENT)
            process.send_signal(signal.CTRL_BREAK_EVENT)
        else:
            process.terminate()
    except ProcessLookupError:
        pass
    except Exception as ex:  # pylint: disable=broad-except
        print("{} {}".format(type(ex).__name__, ex), flush=True)


async def wait_for_run_flag(run_flag_path: str) -> None:
    """-"""

    while True:
        if os.path.exists(run_flag_path):
            return
        await asyncio.sleep(0.2)


def cleanup(run_flag_path: str) -> None:
    """-"""

    try:
        with open(run_flag_path) as file:
            puid: str = file.read()
            if isinstance(puid, bytes):
                puid = str(puid, "utf-8")
    except FileNotFoundError:
        return

    run_flag_link_path = get_run_flag_link_path(puid)

    try:
        os.remove(run_flag_path)
    except FileNotFoundError:
        return

    try:
        os.remove(run_flag_link_path)
    except FileNotFoundError:
        return


async def run_command(
        program: str,
        args: List[str],
        run_flag_path: str = "",
        stop_timeout: float = 3,
        parent_puid: str = "") -> None:
    """-"""

    stdout_reader: Optional[asyncio.Task[Any]] = None
    stderr_reader: Optional[asyncio.Task[Any]] = None

    if run_flag_path:
        try:
            await asyncio.wait_for(wait_for_run_flag(run_flag_path), 5)
        except asyncio.TimeoutError:
            return

    process = await asyncio.create_subprocess_exec(
        program,
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )

    if process.stdout:
        stdout_reader = asyncio.create_task(
            process_output(process.stdout, logging.INFO))
    if process.stderr:
        stderr_reader = asyncio.create_task(
            process_output(process.stderr, logging.ERROR))

    try:
        while process.returncode is None:
            if parent_puid:
                if not await ProcessHandle.find(parent_puid):
                    break
            if run_flag_path:
                if not os.path.exists(run_flag_path):
                    break
            await asyncio.sleep(0.5)

    except asyncio.CancelledError as ex:
        raise ex
    finally:
        terminate_process(process)
        try:
            await asyncio.wait_for(process.wait(), stop_timeout)
        except asyncio.TimeoutError:
            try:
                print("Stop timeout exceeded, process needs to be killed.", flush=True)
                process.kill()
            except Exception as ex:  # pylint: disable=broad-except
                pass
        await process.wait()

        if stdout_reader:
            stdout_reader.cancel()
            await asyncio.gather(stdout_reader, return_exceptions=True)
        if stderr_reader:
            stderr_reader.cancel()
            await asyncio.gather(stderr_reader, return_exceptions=True)
        if run_flag_path:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None, cleanup, run_flag_path)
