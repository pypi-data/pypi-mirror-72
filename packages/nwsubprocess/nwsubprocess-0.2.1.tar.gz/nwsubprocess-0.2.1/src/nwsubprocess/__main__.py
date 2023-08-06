"""-"""

import logging
import sys
from typing import List

from nwsubprocess import utils
from nwsubprocess.execution import run_command


async def main() -> None:
    """-"""

    logging.basicConfig(format="%(levelname)s %(message)s")
    logging.getLogger("nw.execution").setLevel(logging.INFO)
    logger = logging.getLogger("nw.main")
    logger.setLevel(logging.DEBUG)

    stop_timeout: float = 3.0
    parent_puid: str = ""
    run_flag_path: str = ""

    if len(sys.argv) >= 5:
        if sys.argv[1] != "x":
            run_flag_path = str(sys.argv[1])

        stop_timeout = float(sys.argv[2])

        if sys.argv[3] != "x":
            parent_puid = str(sys.argv[3])

        program: str = sys.argv[4]
        args: List[str] = sys.argv[5:]

        logger.debug(run_flag_path)
        logger.debug(stop_timeout)
        logger.debug(parent_puid)
        logger.debug(program)
        logger.debug(args)

    else:
        raise Exception("Not enough arguments")

    await run_command(
        program,
        args=args,
        run_flag_path=run_flag_path,
        stop_timeout=stop_timeout,
        parent_puid=parent_puid)

if __name__ == "__main__":
    utils.run_async_with_signals(main, debug=True)
