@echo off
set arg1=%1
IF %arg1%==test (
    pytest tests/ --asyncio-mode=strict
    )

IF %arg1%==isort (
    isort ./
    )

IF %arg1%==lint (
    pylint adapters/ client/ domain/ server/ service_layer/
    )

IF %arg1%==all (
    isort ./
    pytest tests/ --asyncio-mode=strict
    pylint adapters/ client/ domain/ server/ service_layer/
    )
