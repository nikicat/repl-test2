import asyncio
from concurrent.futures import CancelledError

async def bad_coro():
    raise ValueError


async def long_coro():
  try:
    while True:
        await asyncio.sleep(10)
  except (CancelledError, asyncio.CancelledError):
    print('long coro cancelled')
    raise

async def short_coro():
  return 123

async def main():
    tasks = [
        asyncio.create_task(bad_coro()),
        asyncio.create_task(long_coro()),
        asyncio.create_task(short_coro()),
    ]
    await asyncio.sleep(1)
    await cancel2(*tasks)
    print(asyncio.all_tasks())

async def cancel2(*tasks):
  for t in tasks:
    t.cancel()
    try:
      res = await t
    except (CancelledError, asyncio.CancelledError) as exc:
      print(f'{t} is cancelled ({exc})')
    except Exception as exc:
      print(f'{t} exited with exception {exc}')
    else:
      print(f'{t} exited with {res}')
        
        
if __name__ == '__main__':
    asyncio.run(main())