import sys, re, argparse

parser = argparse.ArgumentParser(description='Returns list of senders by recipient email')
parser.add_argument("to", type=str, help="email address of recipient")
args=parser.parse_args()
for line in sys.stdin:
    pattern=fr".*from.*{args.to}"
    if bool(re.search(pattern, line)) and "MAILER-DAEMON" not in line:
        m =re.search(r"(?<=<).+?(?=>)",line) 
        if m:
            sys.stdout.write(m.group()+"\n")

