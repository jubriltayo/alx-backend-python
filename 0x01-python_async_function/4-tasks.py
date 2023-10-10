#!/usr/bin/env python3
"""This module defines a function `task_wait-n`"""
import asyncio

task_wait_random = __import__('0-basic_async_syntax').wait_random


async def task_wait_n(n: int, max_delay: int) -> list[float]:
    """
    Returns a list of size n with random number between
    0 and max_delay
    """
    curated_list = []
    delays = []

    for i in range(n):
        task = task_wait_random(max_delay)
        curated_list.append(task)

    for task in asyncio.as_completed((curated_list)):
        delay = await task
        delays.append(delay)

    return delays
