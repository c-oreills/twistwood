import subprocess
import sys

subprocess.run(["python pwb.py twistwood"], cwd="pywikibot", shell=True, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin)