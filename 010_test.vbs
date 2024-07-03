Dim ws, filename
Set ws = CreateObject("Wscript.Shell")
filename = Replace(WScript.ScriptName, ".vbs", "")
ws.run "python " & filename & ".py --cond ./json/" & filename & ".json", vbhide
