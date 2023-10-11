#!/usr/bin/env python3
"""This module defines a function `measure_runtime`"""
import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """measures runtime for coroutine"""
    start = time.time()
    tasks = [async_comprehension() for i in range(4)]
    await asyncio.gather(*tasks)
    end = time.time()
    return (end - start)
