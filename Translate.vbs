Set WshShell = WScript.CreateObject("WScript.Shell")
WshShell.Run "runTrans.bat", 2 ' 2 represents SW_SHOWMINIMIZED
WScript.Quit
