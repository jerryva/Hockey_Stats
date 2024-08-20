import pytest
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from pathlib import Path
from hockey_data_2 import parse_html, collect_data, create_excel_file

# Sample HTML content to use in tests
SAMPLE_HTML = """
<table>
    <tr>
        <th>Team Name</th>
        <th>Year</th>
        <th>Wins</th>
        <th>Losses</th>
        <th>OT Losses</th>
        <th>Win %</th>
        <th>Goals For (GF)</th>
        <th>Goals Against (GA)</th>
        <th>+/-</th>
    </tr>
    <tr>
        <td>Team A</td>
        <td>1990</td>
        <td>50</td>
        <td>30</td>
        <td>5</td>
        <td>62.5</td>
        <td>200</td>
        <td>150</td>
        <td>50</td>
    </tr>
    <tr>
        <td>Team B</td>
        <td>1990</td>
        <td>40</td>
        <td>40</td>
        <td>10</td>
        <td>50.0</td>
        <td>180</td>
        <td>160</td>
        <td>20</td>
    </tr>
    <!-- Add more rows as needed -->
</table>
"""

def test_parse_html():
    """Test the parse_html function"""
    data = parse_html(SAMPLE_HTML)
    assert len(data) == 2
    assert data[0] == {
        "Team Name": "Team A",
        "Year": "1990",
        "Wins": 50,
        "Losses": 30,
        "OT Losses": "5",
        "Win %": 62.5,
        "Goals For (GF)": 200,
        "Goals Against (GA)": 150,
        "+/-": 50
    }
    assert data[1] == {
        "Team Name": "Team B",
        "Year": "1990",
        "Wins": 40,
        "Losses": 40,
        "OT Losses": "10",
        "Win %": 50.0,
        "Goals For (GF)": 180,
        "Goals Against (GA)": 160,
        "+/-": 20
    }

def test_collect_data():
    """Test the collect_data function"""
    html_pages = [SAMPLE_HTML]
    data = collect_data(html_pages)
    assert len(data) == 2
    assert data[0]["Team Name"] == "Team A"
    assert data[1]["Year"] == "1990"

def test_create_excel_file(tmp_path):
    """Test the create_excel_file function"""
    test_path = tmp_path / "test_hockey_stats.xlsx"
    data = [
        {"Team Name": "Team A", "Year": "1990", "Wins": 50, "Losses": 30, "OT Losses": "5", "Win %": 62.5, "Goals For (GF)": 200, "Goals Against (GA)": 150, "+/-": 50},
        {"Team Name": "Team B", "Year": "1990", "Wins": 40, "Losses": 40, "OT Losses": "10", "Win %": 50.0, "Goals For (GF)": 180, "Goals Against (GA)": 160, "+/-": 20}
    ]
    create_excel_file(data)

    # Check if the Excel file was created
    wb = load_workbook(test_path)
    ws1 = wb["NHL Stats 1990-2011"]
    ws2 = wb["Winner and Loser per Year"]

    assert ws1['A1'].value == "Team Name"
    assert ws1['A2'].value == "Team A"

    assert ws2['A1'].value == "Year"
    assert ws2['A2'].value == "1990"

# To run the tests, use the following command in the terminal:
# pytest --maxfail=1 --disable-warnings -q
