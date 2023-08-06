'''Look at spinner'''

import asyncio
from asyncspinner import Spinner, styles

async def main():
    async with Spinner('Spinning'):
        await asyncio.sleep(1)
        print('This')
        await asyncio.sleep(1)
        print('is')
        await asyncio.sleep(1)
        print('a')
        await asyncio.sleep(1)
        print('demo.')
        await asyncio.sleep(1)
    print('Finished.')


if __name__ == "__main__":
    asyncio.run(main())
