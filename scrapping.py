import requests
import pandas as pd
from bs4 import BeautifulSoup

data1 = []
for i in range(1):
    resp = requests.get('https://www.securitymagazine.com/articles/topic/2236-cyber-security-news?page='+str(i+1))
    soup = BeautifulSoup(resp.text, 'html.parser')
    ShortSummary = soup.select('[class="post-meta"]')
    print(len(ShortSummary))
    for shortSum in ShortSummary:
        summary = shortSum.select('[class="author-bylines"]')
        print(len(summary))
        if len(summary) == 0:
            data1.append("No summary")
        else:
            data1.append((summary[0].getText()).replace("\n", ""))
    df = pd.DataFrame(data1)
    print(df)
    df.columns= ['Author']
    df.to_excel('author.xlsx', index=False, header=True)