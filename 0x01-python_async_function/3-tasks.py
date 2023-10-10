#!/usr/bin/env python3
"""This modules defines the function `task_wait_random`"""
import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Creates an eventloop for a task
    """
    event_loop = asyncio.get_event_loop()
    return event_loop.create_task(wait_random(max_delay))
