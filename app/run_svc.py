import asyncio
import logging
import sys
import uvicorn
import argparse
import nest_asyncio

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chat_models.openai import ChatOpenAI


def parse_args():
    parser = argparse.ArgumentParser(prog="gonswap-agent", description="Run the gonswap agent service.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="host address")
    parser.add_argument("--port", type=int, default=8901, help="port number")
    parser.add_argument("--env", choices=["dev", "prod"], default="dev", help="environment")
    return parser.parse_args()


async def main():
    args = parse_args()

    root_path = Path(__file__).parent.parent.as_posix()
    sys.path.append(root_path)

    if args.env == "prod":
        import settings.production as settings
    else:
        import settings.develop as settings

    from chatter.chatter import Chatter
    from chatter.api import register_chatter_api

    logging.basicConfig(
        level=logging.getLevelName(settings.LOG_LEVEL),
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    chat_model = ChatOpenAI(**settings.CHAT_MODEL_ARGS)
    chatter = Chatter(chat_llm=chat_model)

    # setup service
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    app.include_router(register_chatter_api(chatter))

    # run app
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
