import subprocess,re, pathlib
userHomeDir=pathlib.Path.home()
pathlib.Path(f"{userHomeDir}/pkzStats").mkdir(parents=True, exist_ok=True)
result = subprocess.run(["df", "-BG"],capture_output=True, text=True)
print(pathlib.Path(f"{userHomeDir}/pkzStats").resolve())
print(list(pathlib.Path(f"{userHomeDir}/pkzStats").glob("pleskAvailableSpace*"))[-1])
result = result.stdout.splitlines()
result = [" ".join(line.split()) for line in result]
result = "".join(filter(lambda s: re.fullmatch("(?:\S+\s+){5}/var;|((?:\S+\s+){5}/)(?!.*/var)",s),result))
print(result)


