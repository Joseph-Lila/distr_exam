import asyncio
import csv
import pathlib
from typing import List, Optional, Dict

import aiocsv
import aiofiles as aiofiles
from aiocsv import AsyncWriter, AsyncDictWriter
from loguru import logger

from config import get_csv_tables_names, get_csv_headers


async def create_tables(paths: Optional[Dict[str, str]] = get_csv_tables_names(), headers=get_csv_headers()):
    current_paths_list = paths or list(get_csv_tables_names().values())
    for key, path in current_paths_list.items():
        if not pathlib.Path(path).exists():
            logger.info(f"{path} doesn't exists. Let's create it!")
            async with aiofiles.open(path, mode="w", encoding="utf-8", newline="") as afp:
                logger.info(f"{path} created successfully!")
                writer = AsyncDictWriter(afp, headers.get(key), restval="NULL", quoting=csv.QUOTE_ALL)
                await writer.writeheader()
    logger.info("Tables are created!")


if __name__ == "__main__":
    asyncio.run(create_tables())
