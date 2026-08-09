import argparse
from selenium import webdriver
from api import headers
from api import user_agents
from api import getStreaks, userExists, questionCount, recentlySolved, typeSkills, compareProfiles

""" FLAGS """
description = "a python command line tool for exploring and comparing leetcode stats."
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-u", "--username", type = str, help = "a username (default = leaderboard)")
parser.add_argument("-l", "--limit", type = int, nargs = '?', const = 5, help = "number of recent submissions (default = 5), use with --rc or --recentlySolved")
parser.add_argument("-a", "--all", action = "store_true", help = "view all information i can show")
parser.add_argument("-c", "--compare", action = "store_true", help = "compare two leetcode profiles with given flags. 'nameOne, nameTwo'")

group = parser.add_mutually_exclusive_group()
group.add_argument("--qc", "--questionCount", action = "store_true", help = "to view total questions solved for each difficuilty")
group.add_argument("--gc", "--getStreaks", action = "store_true", help = "to view active years, max streak, total active days")
group.add_argument("--rs", "--recentlySolved", action = "store_true", help = "to view 'limit'(-l or --limit) recently solved questions")
group.add_argument("--recent", action="store_true", help="show recent accepted submissions")
group.add_argument("--qt", "--questionSkills", action = "store_true", help = "to view advanced, intermediate and fundamental skills.")

#tasty tasty cookies
group.add_argument("--cookies", "--iwantyourcookies", type = str, help = "tool might not work sometimes due to website restrictions, hence cookies required." \
"type your browser name: chrome, firefox, edge and let us automatically take your cookies (completely safe btw).")


args = parser.parse_args()

username = args.username if args.username else "leaderboard"
limit = args.limit if args.limit else 5
browsser = args.browser if args.browser else "Chrome"

#get cookies

def getCookies(browser: str):
    browser = args.cookies.title()
    if browser == "Chrome":
        flag = 1
        driver = webdriver.Chrome()
    elif browser == "Firefox":
        flag = 2
        driver = webdriver.Firefox()
    elif browser == "Edge":
        flag = 3
        driver = webdriver.Edge()
    else:
        print(f"Browser '{browser}' not supported. Use chrome, firefox, edge.")

    driver.get("https://www.leetcode.com")
    cookies = driver.get_cookies()

    if flag == 1:
        headers["Cookie"] = cookies[2]["value"]
        headers["x-csrftoken"] = cookies[2]["value"]
    elif flag == 2:
        headers["Cookie"] = cookies[7]["value"]
        headers["x-csrftoken"] = cookies[7]["value"]
    elif flag == 3:
        headers["Cookie"] = cookies[3]["value"]
        headers["x-csrftoken"] = cookies[3]["value"]

    headers["User-Agent"] = user_agents[browser]

    return None

if args.cookies:
	getCookies(args.browser)

elif args.qc:
	print(questionCount(username))

elif args.gc:
	print(getStreaks(username))

elif args.rs:
	print(recentlySolved(username, limit))

elif args.qt:
	print(typeSkills(username))

elif args.limit:
	print(recentlySolved(username, limit))

elif args.username:
	print(f"user exists: {userExists(username)}")

elif args.compare:
	compareProfiles()

elif args.all:
	print("questions and their difficuilties")
	print(questionCount(username))
	print()

	print("information about your streaks")
	print(getStreaks(username))
	print()

	print("5 most recently solved questions")
	value = recentlySolved(username)
	print(value)