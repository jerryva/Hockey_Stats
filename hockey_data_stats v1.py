import aiohttp
import asyncio
import zipfile
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from openpyxl import Workbook
from pathlib import Path

provided_url = "https://www.scrapethissite.com/pages/forms/"
output_dir = Path("./Test")
loc_html = output_dir / "HTML_Files"  # dir for html files to be saved
path_zipfile = output_dir / "html_files.zip"
path_excel = output_dir / "hockey_stats.xlsx"

#dir check
def curr_dir(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)

async def fetch_page(session: aiohttp.ClientSession, page_number: int) -> str:
    url = f"{provided_url}?page={page_number}"
    async with session.get(url) as response:
        response.raise_for_status()  # To handle HTTP errors
        return await response.text()

async def scrape_data() -> List[str]:
    curr_dir(loc_html)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, page_number) for page_number in range(1, 25)]
        return await asyncio.gather(*tasks)

def save_html_files(html_pages: List[str]) -> None:
    for i, html in enumerate(html_pages, start=1):
        file_path = loc_html / f"{i}.html"
        file_path.write_text(html, encoding='utf-8')

def create_zip_file() -> None:
    with zipfile.ZipFile(path_zipfile, "w") as zipf:
        for i in range(1, 25):
            file_path = loc_html / f"{i}.html"
            zipf.write(file_path, f"{i}.html")

def parse_html(html: str) -> List[Dict[str, Optional[str]]]:
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")[1:] 
    data = []
    for row in rows:
        cols = row.find_all("td")
        data.append({
            "Team Name": cols[0].text.strip(),
            "Year": cols[1].text.strip(),
            "Wins": int(cols[2].text.strip() or '0'),
            "Losses": int(cols[3].text.strip() or '0'),
            "OT Losses": str(cols[4].text.strip() or '0'),  
            "Win %": float(cols[5].text.strip().replace('%', '') or '0'),
            "Goals For (GF)": int(cols[6].text.strip() or '0'),
            "Goals Against (GA)": int(cols[7].text.strip() or '0'),
            "+/-": int(cols[8].text.strip() or '0')
        })
    return data

def collect_data(html_pages: List[str]) -> List[Dict[str, Optional[str]]]:
    return [item for html in html_pages for item in parse_html(html)]

def create_excel_file(data: List[Dict[str, Optional[str]]]) -> None:
    wb = Workbook()

    ws1 = wb.active
    ws1.title = "NHL Stats 1990-2011"
    headers = ["Team Name", "Year", "Wins", "Losses", "OT Losses", "Win %", "Goals For (GF)", "Goals Against (GA)", "+/-"]
    ws1.append(headers)
    for row in data:
        ws1.append([row.get(col, '') for col in headers])

    ws2 = wb.create_sheet(title="Winner and Loser per Year")
    ws2.append(["Year", "Winner", "Winner Num. of Wins", "Loser", "Loser Num. of Wins"])

    year_stats = {}
    for row in data:
        year = row["Year"]
        team = row["Team Name"]
        wins = row["Wins"]

        if year not in year_stats:
            year_stats[year] = {"winner": team, "winner_wins": wins, "loser": team, "loser_wins": wins}
        else:
            if wins > year_stats[year]["winner_wins"]:
                year_stats[year]["winner"] = team
                year_stats[year]["winner_wins"] = wins
            if wins < year_stats[year]["loser_wins"]:
                year_stats[year]["loser"] = team
                year_stats[year]["loser_wins"] = wins

    for year, stats in year_stats.items():
        ws2.append([year, stats["winner"], stats["winner_wins"], stats["loser"], stats["loser_wins"]])

    wb.save(path_excel)

def main() -> None:
    html_pages = asyncio.run(scrape_data())
    save_html_files(html_pages)
    create_zip_file()
    data = collect_data(html_pages)
    create_excel_file(data)

if __name__ == "__main__":
    main()
