import subprocess
import sys
import os

__all__ = ("getProfile", "addProfile", "addPythonScript", "addPythonGrab", "escape",)

def getProfile() -> str:
  """Returns the path of the profile powershell script (it runs for every powershell session)."""
  return subprocess.run(["powershell", "-NoLogo", "-NoProfile", "-Command", "echo $profile"], text=True, stdout=subprocess.PIPE, encoding='windows-1252').stdout.strip()

def addProfile(code: str) -> None:
  """Adds `code` to the profile powershell script."""
  with open(getProfile(), "ab") as f:
    f.write(f"\n{code}".encode('utf-8'))

def addPythonScript(path: str, name: str|None = None) -> None:
  """Adds the python script under `path` as a powershell alias. The alias name is `name` if provided; the last path element otherwise."""
  if name is None:
    name = path.split("/")[-1].split("\\")[-1]

  addProfile("""
function %s() { python "%s" $args }
  """.strip() % (name, escape(path)))

def addPythonGrab(installerPath: str) -> None:
  """Adds the grab.py module under the directory where `installerPath` is located as a powershell alias."""
  try:
    import grab
  except:
    raise Exception("grab.py is required for addPythonGrab")

  path = os.path.dirname(installerPath)
  setup = grab.getmodulename(path)

  addPythonScript(path, setup)

def escape(text: str) -> str:
  """Escapes the given text for inclusion in a PowerShell string."""
  return text.replace('"', '`"').replace('$', '`$').replace("\n", "`n").replace("\r", "`r").replace("\a", "`a")
