# webber 🕸️
> a command line tool for exploring leetcode profiles and stats.

## features
- view total questions solved by difficulty
- view streak info, active years and total active days
- view recently solved questions
- automatic cookie extraction via selenium (no manual copy-pasting)

## requirements
pip install requests selenium

you also need a browser driver installed:
- Chrome — [chromedriver](https://chromedriver.chromium.org/)
- Firefox — [geckodriver](https://github.com/mozilla/geckodriver)
- Edge — [edgedriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

## usage

```bash
python webber.py -u <username> [flag]
```

### flags

| flag | description |
|------|-------------|
| `-u`, `--username` | leetcode username (defaults to `leaderboard`) |
| `-l`, `--limit` | number of recent submissions to show (default = 5) |
| `-a`, `--all` | show all available info |
| `--qc` | questions solved by difficulty |
| `--gc` | streak info and active years |
| `--rs` | recently solved questions |
| `--cookies` | extract cookies from browser (`chrome`, `firefox`, `edge`) |

### examples

```bash
# question count for a user
python webber.py -u compiler-man --qc

# streak info
python webber.py -u compiler-man --gc

# last 10 recently solved
python webber.py -u compiler-man --rs -l 10

# all info
python webber.py -u compiler-man --all

# use cookies from chrome (needed for some profiles)
python webber.py -u compiler-man --qc --cookies chrome
```

## why cookies?
leetcode restricts some API calls from outside their website. the `--cookies` flag opens your browser via selenium, lets you log in, then automatically extracts your session cookies so the tool can make authenticated requests.

## how it works
leetcode uses an internal graphql api to power their website. this tool sends the same queries your browser does, directly from python, and formats the response in the terminal.

## notes
- some profiles have private submission history — `--rs` will say so instead of crashing
- cookies expire periodically, re-run with `--cookies` when that happens
- this uses leetcode's unofficial/undocumented api — it may break if they change it
