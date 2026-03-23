Set objShell = CreateObject("Wscript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Pega a pasta atual onde este arquivo .vbs está salvo
strFolder = objFSO.GetParentFolderName(Wscript.ScriptFullName)

' Monta o comando para executar o script python no diretório atual
strCommand = "cmd.exe /c cd /d """ & strFolder & """ && python monitor_fabric.py"

' O número 0 no final significa que a janela será iniciada de forma totalmente OCULTA (invisível).
' O False significa que não vamos esperar o programa terminar para liberar este script.
objShell.Run strCommand, 0, False
