import requests

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

#had to decide between doing one extra api call each time or adding more code to each function
def userExists(username: str) -> bool:
	query = """
	query($username: String!) {
		matchedUser(username: $username) {
			username
		}
	}
	"""

	data = requests.post(url, json={"query": query, "variables": {"username": username}}, headers = headers)
	one = data.json()

	return one['data']['matchedUser'] is not None

def questionCount(username: str) -> list:

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
	if not userExists(username):
		return ["no such user"]

	required = one['data']['matchedUser']['submitStats']['acSubmissionNum']

	for i in required:
		output.append({i['difficulty']:i['count']})

	return output

def getStreaks(username: str) -> list:

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
	if not userExists(username):
		return ["no such user"]

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

def recentlySolved(username: str, limit : int = 5) -> list:

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
	if not userExists(username):
		return ["no such user"]

	submissionList = one['data']['recentAcSubmissionList']
	limit = limit if len(submissionList) > limit else len(submissionList)

	if len(submissionList) == 0:
		output.append("recent submissions not available for this profile.")
		return output

	for i in range(limit):
		output.append(submissionList[i]['title'])

	return output

def typeSkills(username: str):
	query = """
	query($username: String!) {
		matchedUser(username: $username) {
			tagProblemCounts {
					advanced {
					tagName
					problemsSolved
				}
					intermediate {
					tagName
					problemsSolved
				}
					fundamental {
					tagName
					problemsSolved
				}
			}
		}
	}
	"""
	output = list()
	data = requests.post(url, json={"query": query, "variables": {"username": username}}, headers= headers)
	one = data.json()
	for i in one['data']['matchedUser']['tagProblemCounts']['advanced']:
		output.append({i['tagName']: i['problemsSolved']})
	output.append("------------------------------------------")
	for i in one['data']['matchedUser']['tagProblemCounts']['intermediate']:
		output.append({i['tagName']: i['problemsSolved']})
	output.append("------------------------------------------")
	for i in one['data']['matchedUser']['tagProblemCounts']['fundamental']:
		output.append({i['tagName']: i['problemsSolved']})
	
	
	return output

def compareProfiles(names: str):
	names = [i.strip() for i in names.split(',')]

	if len(names) != 2:
		return ["please provide exactly two usernames, e.g. 'nameOne,nameTwo'"]

	nameOne, nameTwo = names

	for name in names:
		if not userExists(name):
			return [f"user '{name}' does not exist."]

	output = list()

	# --- Question counts ---
	qcOne = questionCount(nameOne)
	qcTwo = questionCount(nameTwo)

	def toDict(qcList):
		merged = {}
		for d in qcList:
			merged.update(d)
		return merged

	qcOneDict = toDict(qcOne)
	qcTwoDict = toDict(qcTwo)

	output.append("----- Question Count -----")
	for difficulty in qcOneDict:
		oneCount = qcOneDict.get(difficulty, 0)
		twoCount = qcTwoDict.get(difficulty, 0)
		winner = nameOne if oneCount > twoCount else nameTwo if twoCount > oneCount else "tie"
		output.append({
			"difficulty": difficulty,
			nameOne: oneCount,
			nameTwo: twoCount,
			"ahead": winner
		})

	# --- Streaks ---
	gcOne = getStreaks(nameOne)
	gcTwo = getStreaks(nameTwo)

	streakOne = gcOne[0]['all time max streak']
	streakTwo = gcTwo[0]['all time max streak']
	activeDaysOne = gcOne[2]['total active days']
	activeDaysTwo = gcTwo[2]['total active days']

	output.append("----- Streaks -----")
	output.append({
		"max streak": {nameOne: streakOne, nameTwo: streakTwo,
			"ahead": nameOne if streakOne > streakTwo else nameTwo if streakTwo > streakOne else "tie"}
	})
	output.append({
		"total active days": {nameOne: activeDaysOne, nameTwo: activeDaysTwo,
			"ahead": nameOne if activeDaysOne > activeDaysTwo else nameTwo if activeDaysTwo > activeDaysOne else "tie"}
	})

	# --- Total questions solved (sum across difficulties) ---
	totalOne = sum(v for k, v in qcOneDict.items() if k != "All")
	totalTwo = sum(v for k, v in qcTwoDict.items() if k != "All")

	output.append("----- Overall -----")
	output.append({
		"total solved": {nameOne: totalOne, nameTwo: totalTwo,
			"ahead": nameOne if totalOne > totalTwo else nameTwo if totalTwo > totalOne else "tie"}
	})

	return output