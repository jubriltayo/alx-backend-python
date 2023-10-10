#!/usr/bin/env python3
"""This module defines a function `wait_n`"""
import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> list[float]:
    """
    Returns a list of size n with random number between
    0 and max_delay
    """


    currated_list = [wait_random(max_delay) for x in range(n)]
    result = await asyncio.gather(*currated_list)
    return sorted(result)
