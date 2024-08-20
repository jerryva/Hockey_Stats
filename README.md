# Hockey_Stats
This project is a web scraper that extracts data from multiple pages and saves the data into an Excel file. It uses asynchronous HTTP requests to fetch HTML content, parses the HTML to extract relevant data, and then aggregates and stores the data in an Excel file.

## Features

- Asynchronously fetches HTML content from multiple pages.
- Parses HTML to extract NHL team statistics.
- Saves raw HTML files and compresses them into a ZIP archive.
- Aggregates data and exports it to an Excel file with two sheets:
  - **NHL Stats 1990-2011**: Raw data from the HTML pages.
  - **Winner and Loser per Year**: Aggregated data showing the team with the most wins and the team with the fewest wins each year.

## Requirements

The script requires the following Python packages:

- `aiohttp`: For making asynchronous HTTP requests.
- `beautifulsoup4`: For parsing HTML.
- `openpyxl`: For creating and modifying Excel files.

You can install the required packages using the provided `requirements.txt` file.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository

2. Install depencies
   pip install -r requirements.txt
3. Run the python script
## Testing
To ensure that your code is working as expected, you can run the test suite using pytest. The tests cover parsing HTML, aggregating data, and creating Excel files.

Running Tests
1. Install pytest if you haven't already:
   pip install pytest
2. Run the test code with command:
   pytest
======================================
## Project Structure
a. hockey_data_stat v1.py: The main Python script that performs scraping, data processing, and Excel file creation.
b. requirements.txt: Lists the Python packages required to run the script.
c. README.md: This file, providing project details and instructions.
Test/: Directory for storing HTML files and ZIP archive.


### Instructions for Use:

1. **Replace Placeholder Text**:
   - Replace `your-username`, `your-repository`, `your_script_name.py`, and any other placeholders with the actual values relevant to your project.

2. **Add Licensing Details**:
   - Ensure you have a `LICENSE` file and update the license section accordingly.

3. **Test Directory**:
   - If you place test code in a separate `tests/` directory, mention it in the "Project Structure" section. Adjust paths if needed.

This `README.md` file will provide users with a clear understanding of your project, how to set it up, use it, and run tests.
