import re
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def date_time(s):
    pattern = r'^([0-9]+)\/([0-9]+)\/([0-9]+), ([0-9]+):([0-9]+)\s?(AM|PM|am|pm)? -'
    result = re.match(pattern, s)
    if result:
        return True
    return False

def find_author(s):
    s = s.split(":")
    if len(s) == 2:
        return True
    else:
        return False

def getDatapoint(line):
    splitline = line.split(' - ')
    dateTime = splitline[0]
    date, time = dateTime.split(", ")
    message = " ".join(splitline[1:])
    if find_author(message):
        splitmessage = message.split(": ")
        author = splitmessage[0]
        message = " ".join(splitmessage[1:])
    else:
        author = None
    return date, time, author, message

data = []
conversation = 'WhatsApp Chat with +91 6205 889 432.txt'
with open(conversation, encoding="utf-8") as fp:
    fp.readline()
    messageBuffer = []
    date, time, author = None, None, None
    
    while True:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if date_time(line):
            date, time, author, message = getDatapoint(line)
            if messageBuffer:
                data.append([date, time, author, ' '.join(messageBuffer)])
            messageBuffer.clear()
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)

if messageBuffer:  # Append the remaining messages
    data.append([date, time, author, ' '.join(messageBuffer)])

df = pd.DataFrame(data, columns=["Date", 'Time', 'Author', 'Message'])
df['Date'] = pd.to_datetime(df['Date'])

# Now you can work with the DataFrame (df) as needed
print(df)
