import finnhub
import pandas as pd
# verify that not historically backwards

finnhub_client = finnhub.Client(api_key="cfj73ghr01que34nr220cfj73ghr01que34nr22g")
df = pd.DataFrame(finnhub_client.company_earnings('AAPL'))

print(df["actual"])


average_beat = 0    # average percent surprise each quarter
i = 0
while i < len(df["surprisePercent"]):

    average_beat += df["surprisePercent"][i]    # increment total beat percentage
    i += 1

average_beat = average_beat / len(df["surprisePercent"])

# % change between first and last quarters
overall_eps_increase = ((df["actual"][0] / df["actual"][len(df["actual"]) - 1]) - 1) * 100

print(average_beat)
print(overall_eps_increase)


percent01 = (df["actual"][0] / df["actual"][1] - 1) * 100
print(percent01)
percent12 = (df["actual"][1] / df["actual"][2] - 1) * 100
print(percent12)
percent23 = (df["actual"][2] / df["actual"][3] - 1) * 100
print(percent23)


ab_result = 0
oei_result = 0

if average_beat >= 4:
    ab_result += 30
elif average_beat >= 0:
    ab_result += 15

if overall_eps_increase > 10:
    oei_result += 70
elif 5 < overall_eps_increase <= 10:
    oei_result += 50
elif 0 < overall_eps_increase <= 5:
    oei_result += 30

print("final score: ", ab_result + oei_result)


