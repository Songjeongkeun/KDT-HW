import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


def melon_chart_search():
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    url = "https://www.melon.com/chart/index.htm"
    like_api_url = "https://www.melon.com/commonlike/getSongLike.json?contsIds=602024048%2C601807965%2C601899271%2C602115220%2C37928381%2C601719413%2C601479669%2C601332163%2C601719416%2C36730261%2C36397952%2C39504779%2C601879407%2C600287375%2C601013499%2C601237102%2C601555642%2C602193303%2C600299706%2C37473973%2C601968268%2C600243411%2C38626852%2C39307948%2C602248118%2C32061975%2C38733032%2C601555636%2C39298775%2C39166708%2C4446485%2C38123332%2C38300904%2C37390939%2C602313594%2C38429074%2C38104031%2C36617841%2C31927275%2C33241003%2C38242510%2C36699489%2C37228861%2C30244931%2C601965921%2C39161085%2C38629386%2C34061322%2C37323944%2C38071559%2C602066108%2C34753369%2C601555637%2C31666417%2C601555640%2C30962526%2C39156202%2C30232719%2C32872978%2C37140709%2C602193304%2C1556553%2C34657844%2C33411344%2C37323943%2C600354699%2C37347911%2C37375706%2C38120327%2C38426197%2C38123338%2C38444825%2C1121123%2C38635449%2C601555639%2C600320356%2C35454426%2C600359330%2C33496587%2C39566906%2C600513208%2C601356371%2C601379618%2C601555645%2C600791038%2C601555638%2C37901626%2C36985781%2C37145732%2C36382580%2C601461624%2C600280518%2C39765727%2C602193305%2C37053556%2C601587114%2C33548514%2C602193307%2C602248117%2C602011402"

    response = requests.get(url, headers=headers)
    like_response = requests.get(like_api_url, headers=headers)
    like_data = like_response.json()

    chart_data = []

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("tr.lst50, tr.lst100")

    for row, like in zip(rows, like_data['contsLike']):
        title_tag = row.select_one("div.ellipsis.rank01")
        artist_tag = row.select_one("div.ellipsis.rank02 a")
        album_tag = row.select_one("div.ellipsis.rank03")
        like_tag = like['SUMMCNT']\
        
        if title_tag is None:
            continue

        chart_data.append({
            "곡명": title_tag.get_text(strip=True),
            "아티스트": artist_tag.get_text(strip=True),
            "앨범명": album_tag.get_text(strip=True),
            "좋아요": like_tag
        })
        
    time.sleep(0.5)
    
    df = pd.DataFrame(chart_data)
    
    if not df.empty:
        df = df.drop_duplicates(subset=["곡명", "아티스트", "앨범명", "좋아요"])
        df.index = df.index + 1

    file_name = "melon_chart_top100"
    df.to_csv(file_name, encoding="utf-8-sig")
    
    print("csv 저장완료")
    
    return df


melon_chart_search()