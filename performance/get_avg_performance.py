import pandas as pd

def get_average(tool_durations):
    averages = {}
    for tool, durations in tool_durations.items():
        averages[tool] = sum(durations) / len(durations)
    return averages

path = 'results.csv'

df = pd.read_csv(path)

tool_durations = {}

for index, row in df.iterrows():
    tool = row["toolid"]
    duration = row["duration"]

    if tool not in tool_durations:
        tool_durations[tool] = []
    tool_durations[tool].append(duration)

average_durations = get_average(tool_durations)

for tool, avg_duration in average_durations.items():
    print(f"Tool: {tool}, Average Duration: {avg_duration}")