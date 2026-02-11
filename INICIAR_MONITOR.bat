@echo off
title MONITOR DE ERROS POWER BI
mode con: cols=100 lines=30
color 0A
cls
echo.
echo  ==================================================================================================
echo.
echo                            MONITOR DE ERROS - POWER BI
echo.
echo  ==================================================================================================
echo.
echo  [INFO] Iniciando o script de monitoramento...
echo  [INFO] Pressione CTRL+C para encerrar o monitoramento a qualquer momento.
echo.
echo  --------------------------------------------------------------------------------------------------
echo.
python monitor_email.py
echo.
echo  --------------------------------------------------------------------------------------------------
echo  [INFO] O monitor foi encerrado.
pause
exit
