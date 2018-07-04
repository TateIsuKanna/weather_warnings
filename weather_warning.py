import urllib.request
import re
import time

import json
with open("auth.json") as jfs:
    authdata=json.load(jfs)

import twitter
auth = twitter.OAuth(**authdata)
t = twitter.Twitter(auth=auth)

with open("web.json") as jfs:
    web_data=json.load(jfs)

while True:
    with urllib.request.urlopen("http://www.kobe-kosen.ac.jp/") as f:
        HTML=f.read().decode("Shift_JIS")
        emergency_str=re.search(r'<div id="emergency">.+?</div>',HTML,re.DOTALL).group()
        print(emergency_str)
        if emergency_str!=web_data["kcct_emergency"]:
            web_data["kcct_emergency"]=emergency_str
            sanitized_emergency_str=re.sub(r"(<.+?>|\n)","",emergency_str,re.DOTALL)
            print(sanitized_emergency_str)
            t.statuses.update(status="#連絡 #試験運用 sanitized_emergency_str http://www.kobe-kosen.ac.jp/#emergency")
    with urllib.request.urlopen("https://www.jma.go.jp/jp/warn/f_2810000.html") as f:
        HTML=f.read().decode()
        date_strfull=re.search(r"<tr><td>.+神戸地方気象台発表",HTML,re.DOTALL).group()
        mainwarnings_str=re.sub(r"<.+?>","",re.search(r'<td class="regLeft">.+?</td>',HTML,re.DOTALL).group())
        print(date_strfull,mainwarnings_str)
        if date_strfull!=web_data["jma"]:
            web_data["jma"]=date_strfull
            print(date_strfull)
            t.statuses.update(status="#連絡 #試験運用 神戸市 "+"\n"+mainwarnings_str+" https://www.jma.go.jp/jp/warn/f_2810000.html")
    with open("web.json","w") as jfs:
        json.dump(web_data,jfs)

    time.sleep(60)
