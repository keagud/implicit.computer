""" 
Watch the blog and resume repos for changes
"""

from collections.abc import Callable, Coroutine
from concurrent import futures
from dataclasses import dataclass
from pathlib import Path
from contextlib import contextmanager
from subprocess import CalledProcessError, SubprocessError
from definitions import RESUME_DIR, ROOT_DIR
import asyncio


async def async_cmd(cmd: list[str], cwd: Path, *args, **kwargs) -> str:
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        *args,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        **kwargs,
    )

    stdout, stderr = await proc.communicate()

    if (ret := proc.returncode) is not None and ret != 0:
        raise CalledProcessError(ret, cmd, stdout, stderr)

    return stdout.decode("utf-8").strip()


async def get_commit_hash(cwd) -> str:
    hash = await async_cmd(["git", "rev-parse", "HEAD"], cwd=cwd)
    return hash.strip()


async def fetch_resume(verbose = False) -> bool:
    old_commit_hash = await get_commit_hash(RESUME_DIR)
    pull_reply = await async_cmd(["git", "submodule", "update", "--remote"], cwd=RESUME_DIR)
    if verbose:
        print(pull_reply)

    new_commit_hash = await get_commit_hash(RESUME_DIR)
    return old_commit_hash != new_commit_hash


async def fetch_blog() -> bool:
    old_commit_hash = await get_commit_hash(ROOT_DIR)
    await async_cmd(["git", "pull"], cwd=ROOT_DIR)
    new_commit_hash = await get_commit_hash(ROOT_DIR)
    return old_commit_hash != new_commit_hash


class Watcher:
    def __init__(
        self,
        blog_callback: Coroutine,
        resume_callback: Coroutine,
        poll_interval_secs: float = 60,
    ) -> None:
        self.blog_callback = blog_callback
        self.resume_callback = resume_callback


def start_watch(
    blog_callback: Callable, resume_callback: Callable, poll_interval_secs: float = 10
):
    async def _resume():
        if await fetch_resume(verbose=True):
            resume_callback()

    async def _blog():
        #if await fetch_blog():
         blog_callback()

    async def _main():
        while True:
            print("Polling")
            await asyncio.gather(_resume(), _blog())
            await asyncio.sleep(poll_interval_secs)

    asyncio.run(_main())


