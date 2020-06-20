import asyncio

async def func1():
    await asyncio.sleep(1)
    print('Hello ...')

async def func2():
    await asyncio.sleep(2)
    print('... World!')

async def main():
    await asyncio.gather(
        func2(),
        func1()
    )

asyncio.run(main())
