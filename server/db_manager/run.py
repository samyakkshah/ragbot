# run.py
import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


from db_manager import db_manager

if __name__ == "__main__":
    asyncio.run(db_manager.init_db())
