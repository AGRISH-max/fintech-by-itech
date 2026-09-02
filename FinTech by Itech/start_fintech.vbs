Set WshShell = CreateObject("WScript.Shell")

WshShell.Run "cmd /c python app.py", 0, False

WScript.Sleep 3000

WshShell.Run "http://127.0.0.1:5000"