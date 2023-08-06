"""-"""

import asyncio
import enum
import os
import subprocess
import sys
import tempfile
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Tuple

import atomicwrites
import psutil

RUN_FLAG_DIR: str = os.path.join(tempfile.gettempdir(), "nwsubprocess")


@dataclass
class ProcessPipes:
    """stderr is redirected to stdout and can be easily parsed."""
    stdout: Any
    stdin: Any


class ProcessOutputType(enum.Enum):
    """-"""
    DEBUG = 0
    STDOUT = 1
    STDERR = 2

    def __str__(self) -> str:
        return str(self.name)


async def readline(pipe: Any) -> Tuple[ProcessOutputType, Optional[str]]:
    """Reads line from pipe and returns it together with
    the output type STDOUT|STDERR|DEBUG.
    Returns EOFError when pipe has reached the end/is closed.
    """

    data = await pipe.readline()
    if data:
        line = str(data.decode('utf-8').rstrip())
        if line.strip().startswith("INFO "):
            line = line.replace("INFO ", "")
            return (ProcessOutputType.STDOUT, line)
        elif line.strip().startswith("ERROR "):
            line = line.replace("ERROR ", "")
            return (ProcessOutputType.STDERR, line)
        else:
            if line.strip().startswith("DEBUG "):
                line = line.replace("DEBUG ", "")
            return (ProcessOutputType.DEBUG, line)

    raise EOFError()


def make_puid(pid: int, create_timestamp: int) -> str:
    """Process unique id (<pid>-<create_timestamp>)"""
    return "{}-{}".format(pid, create_timestamp)


def split_puid(puid: str) -> Tuple[int, int]:
    """Splits puid into pid and create timestamp"""
    try:
        pid: int = int(puid.split("-")[0])
        timestamp: int = int(puid.split("-")[1])
    except Exception:
        raise ValueError("Invalid puid")
    return (pid, timestamp)


class PollNotAvailable(Exception):
    """-"""


@dataclass
class ProcessHandle:
    """-"""

    pid: int
    create_timestamp: int
    process: Optional[psutil.Process]

    handle_poll: Optional[Callable[..., Optional[int]]] = field(
        default=None, init=False)

    async def poll(self) -> Optional[int]:
        """Returns returncode of the process.
        Will raise PollNotAvailable when the process
        was not created in the calling process.
        """
        if not self.handle_poll:
            raise PollNotAvailable()
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, self.handle_poll)

    def __eq__(self, other: Any) -> bool:
        return bool(self.puid == other.puid)

    @property
    def puid(self) -> str:
        """Process unique id (<pid>:<create_timestamp>)"""
        return make_puid(self.pid, self.create_timestamp)

    @property
    def run_flag_link_path(self) -> str:
        """-"""
        return get_run_flag_link_path(self.puid)

    @staticmethod
    async def find(puid: str) -> Optional["ProcessHandle"]:
        """-"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, find_process, puid)

    @staticmethod
    async def find_by_pid(pid: int) -> Optional["ProcessHandle"]:
        """-"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, find_process_by_pid, pid)

    @staticmethod
    async def find_by_run_id(run_id: int) -> Optional["ProcessHandle"]:
        """-"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, find_process_by_run_id, run_id)

    @staticmethod
    async def get_current() -> "ProcessHandle":
        """-"""
        handle = await ProcessHandle.find_by_pid(os.getpid())
        assert handle
        return handle

    def create_run_flag(self, run_id: str) -> None:
        """-"""
        os.makedirs(RUN_FLAG_DIR, exist_ok=True)
        with atomicwrites.atomic_write(self.run_flag_link_path) as file:
            file.write(run_id)
        run_flag_path = get_run_flag_path(run_id)
        with atomicwrites.atomic_write(run_flag_path) as file:
            file.write(self.puid)

    async def wait(self) -> Optional[int]:
        """-"""

        if not self.process:
            return await self.poll()

        loop = asyncio.get_running_loop()
        while True:
            try:
                return await loop.run_in_executor(
                    None, self.process.wait, 1)
            except psutil.TimeoutExpired:
                pass

    def _stop(self) -> None:
        """-"""

        try:
            with open(self.run_flag_link_path) as file:
                run_id: str = file.read()
                if isinstance(run_id, bytes):
                    run_id = str(run_id, "utf-8")
        except FileNotFoundError:
            return

        try:
            run_flag_path = get_run_flag_path(run_id)
            os.remove(run_flag_path)
        except FileNotFoundError:
            return

        try:
            os.remove(self.run_flag_link_path)
        except FileNotFoundError:
            return

    async def stop(self) -> None:
        """-"""

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._stop)


def find_process(puid: str) -> Optional[ProcessHandle]:
    """-"""

    pid, timestamp = split_puid(puid)
    try:
        process = psutil.Process(pid)
        if int(process.create_time()) != timestamp:
            return None
        return ProcessHandle(pid, timestamp, process)
    except psutil.NoSuchProcess:
        return None


def find_process_by_pid(pid: int) -> Optional[ProcessHandle]:
    """-"""

    try:
        process = psutil.Process(pid)
        return ProcessHandle(
            process.pid,
            int(process.create_time()),
            process)
    except psutil.NoSuchProcess:
        return None


def find_process_by_run_id(run_id: str) -> Optional[ProcessHandle]:
    """-"""
    try:
        with open(get_run_flag_path(run_id)) as file:
            puid = file.read()
            if isinstance(puid, bytes):
                puid = str(puid, "utf-8")
    except FileNotFoundError:
        return None

    return find_process(puid)


def get_run_flag_path(run_id: str) -> str:
    """-"""
    return os.path.join(RUN_FLAG_DIR, "run-flag-{}".format(run_id))


def get_run_flag_link_path(puid: str) -> str:
    """-"""
    return os.path.join(RUN_FLAG_DIR, "run-flag-link-{}".format(puid))


def _start_detached_subprocess(params: List[str], hide: bool = True) -> "subprocess.Popen[Any]":
    """-"""

    startupinfo = subprocess.STARTUPINFO()
    if hide:
        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

    stdout = None
    stderr = None
    stdin = None

    if hide:
        stdout = subprocess.DEVNULL
        stderr = subprocess.DEVNULL
        stdin = subprocess.DEVNULL

    popen = subprocess.Popen(
        params,
        stdout=stdout,
        stderr=stderr,
        stdin=stdin,
        startupinfo=startupinfo,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NEW_CONSOLE
    )
    return popen


async def start_subprocess(
        program: str,
        args: Optional[List[str]] = None,
        stop_timeout: float = 3,
        detached: bool = False,
        use_output: bool = False,
        hide: bool = True,
        run_id: str = "") -> Tuple[ProcessHandle, ProcessPipes]:
    """Starts a new process that will be killed when the
    parent (caller of this function) dies.
    If 'detached' is set to true the child process will live on.
    Pipes are not supported for detached processes therefore
    'use_output' and 'use_input' will be ignored.
    """

    loop = asyncio.get_running_loop()

    parent: Optional[ProcessHandle] = None
    if not detached:
        parent = await ProcessHandle.get_current()

    if not run_id:
        run_id = str(uuid.uuid1())
    run_flag_path: str = get_run_flag_path(run_id)
    python_dir = os.path.dirname(sys.executable)

    stdout = None
    stderr = None

    # Always open at least one pipe, otherwise it could
    # happen that the program termination is not forwarded
    # when the process is not properly waited for when
    # it terminates. (Applies for attached processes)
    stdin = subprocess.PIPE

    if use_output:
        stdout = subprocess.PIPE
        stderr = subprocess.STDOUT

    params: List[str] = [
        "-m",
        "nwsubprocess",
        run_flag_path,
        str(stop_timeout),
        parent.puid if parent else "x",
        program
    ]
    if args:
        for arg in args:
            params.append(arg)

    pipes = ProcessPipes(None, None)
    handle: Optional[ProcessHandle] = None
    returncode: Optional[int] = None
    process: Any = None

    if os.name == "nt":
        # 'No module named c' is a bug and occurs when the Python debugger
        # attaches itself to the subprocess. You can prevent this by disabling
        # it in the IDE e.g. vscode python launche config -> subprocess: false,
        # or by using a different executor, such as cmd /c python ...
        # If you use cmd /c, you have a command length restriction (Windows sucks)

        if not detached:
            startupinfo = subprocess.STARTUPINFO()
            if hide:
                startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

            process = await asyncio.create_subprocess_exec(
                os.path.join(python_dir, "python"),
                *params,
                stdout=stdout,
                stderr=stderr,
                stdin=stdin,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NEW_CONSOLE
            )
            pipes = ProcessPipes(
                stdout=process.stdout,
                stdin=process.stdin
            )
            handle = find_process_by_pid(process.pid)
            if handle:
                handle.handle_poll = (lambda: None if process.returncode is None else int(
                    process.returncode))
            returncode = process.returncode

        else:
            popen: "subprocess.Popen[Any]" = await loop.run_in_executor(
                None, _start_detached_subprocess,
                [os.path.join(python_dir, "python")] + params,
                hide)
            handle = find_process_by_pid(popen.pid)
            if handle:
                handle.handle_poll = popen.poll
            returncode = await loop.run_in_executor(
                None, popen.poll)

    else:
        raise NotImplementedError()

    if returncode is None:
        if handle:
            handle.create_run_flag(run_id)
        else:
            raise Exception("Should not happen, investigate!")
    else:
        if process:
            await process.wait()
        handle = ProcessHandle(process.pid, -1, None)
        handle.handle_poll = lambda: returncode

    return handle, pipes
