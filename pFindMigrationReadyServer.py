import subprocess,re
# Run a simple shell command
# Capture the output of a command
result = subprocess.run(["df", "-BG"],capture_output=True, text=True)
#print(result.stdout)
result = result.stdout.splitlines()
result = [" ".join(line.split()) for line in result]
result = "".join(filter(lambda s: re.fullmatch("(?:\S+\s+){5}/var;|((?:\S+\s+){5}/)(?!.*/var)",s),result))
print(result)


