@echo off
set arg1=%1
IF %arg1%==test (
    pytest tests/ --asyncio-mode=strict
    )

IF %arg1%==isort (
    isort src/
    )

IF %arg1%==lint (
    pylint src/
    )

IF %arg1%==server (
    python -m src.entrypoints.server.main
    )

IF %arg1%==client (
    python -m src.entrypoints.client.main
    )

IF %arg1%==all (
    isort src/
    pytest tests/ --asyncio-mode=strict
    pylint src/
    )
