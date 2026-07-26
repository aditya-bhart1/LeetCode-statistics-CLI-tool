import requests
import argparse
from selenium import webdriver


url = "https://leetcode.com/graphql"

user_agents = {
    "Chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Edge": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
}

headers = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
}

def questionCount(username: str = "leaderboard") -> list:

	query = """
	query($username: String!) {
		matchedUser(username: $username) {
			submitStats {
				acSubmissionNum {
					difficulty
					count
				}
			}
		}
	}
	"""

	output = list()
	data = requests.post(url, json={"query": query, "variables": {"username": username}}, headers= headers)
	one = data.json()
	required = one['data']['matchedUser']['submitStats']['acSubmissionNum']

	for i in required:
		output.append({i['difficulty']:i['count']})

	return output

def getStreaks(username: str = "leaderboard") -> list:

	query = """
	query($username: String!) {
		matchedUser(username: $username) {
			userCalendar {
			streak
			activeYears
			}
		}
	}
	"""

	output = list()
	data = requests.post(url, json={"query" : query, "variables": {"username": username}}, headers= headers)

	one = data.json()
	output.append({'all time max streak':one['data']['matchedUser']['userCalendar']['streak']})
	output.append({'active years':one['data']['matchedUser']['userCalendar']['activeYears']})

	addition = 0
	#time to find total active days
	queryTotalDays = """
	query($username: String!, $year: Int!) {
		matchedUser(username: $username) {
			userCalendar(year: $year) {
				totalActiveDays
			}
		}
	}
	"""
	for year in output[1]['active years']:
		additionData = requests.post(url, json={"query": queryTotalDays, "variables": {"username": username, "year": year}}, headers = headers)
		result = additionData.json()
		addition += result['data']['matchedUser']['userCalendar']['totalActiveDays']

	output.append({"total active days": addition})

	return output

def recentlySolved(username: str = "leaderboard", limit : int = 5) -> list:

	query = """
	query($username: String!, $limit: Int!) {
		recentAcSubmissionList(username: $username, limit: $limit) {
			id
			title
		}
	}
	"""

	output = list()
	data = requests.post(url, json={"query": query, "variables": {"username": username, "limit": limit}}, headers= headers)
	one = data.json()
	submissionList = one['data']['recentAcSubmissionList']
	limit = limit if len(submissionList) > limit else len(submissionList)

	if len(submissionList) == 0:
		output.append("recent submissions not available for this profile.")
		return output

	for i in range(limit):
		output.append(submissionList[i]['title'])

	return output

"""cell for when user calls flag '-h' or '--help' for help"""
description = "a python command line tool for exploring and comparing leetcode stats."
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-u", "--username", type = str, help = "a username (default = leaderboard)")
parser.add_argument("-l", "--limit", type = int, help = "number of recent submissions (default = 5), use with --rc or --recentlySolved")
parser.add_argument("-a", "--all", action = "store_true", help = "view all information i can show")

group = parser.add_mutually_exclusive_group()
group.add_argument("--qc", "--questionCount", action = "store_true", help = "to view total questions solved for each difficuilty")
group.add_argument("--gc", "--getStreaks", action = "store_true", help = "to view active years, max streak, total active days")
group.add_argument("--rs", "--recentlySolved", action = "store_true", help = "to view 'limit'(-l or --limit) recently solved questions")
group.add_argument("--recent", action="store_true", help="show recent accepted submissions")

#tasty tasty cookies
group.add_argument("--cookies", "--iwantyourcookies", type = str, help = "tool might not work sometimes due to website restrictions, hence cookies required." \
"type your browser name: chrome, firefox, edge")


args = parser.parse_args()

username = args.username if args.username else "leaderboard"
limit = args.limit if args.limit else 5
flag = -1

if args.cookies:
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

if args.qc:
	print(questionCount(username))

elif args.gc:
	print(getStreaks(username))

elif args.rs:
	print(recentlySolved(username, limit))

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