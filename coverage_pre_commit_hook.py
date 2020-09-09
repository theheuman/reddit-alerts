import os
from bs4 import BeautifulSoup

CODE_COVERAGE_GOAL_PERCENTAGE = 99


def run_coverage():
    exit_code = os.system("coverage run --source=./src/ -m unittest testing.test")
    if exit_code != 0:
        exit(exit_code)
    os.system("coverage html")


def get_total_percentage() -> int:
    # now go parse the html lol
    # open up the file, and get all the table rows
    coverage_html_file = "coverage_html_report/index.html"
    file = open(coverage_html_file, "r", encoding="utf8")
    html = file.read()
    soup = BeautifulSoup(html, "html.parser")
    total_row = soup.find("tr", {"class": "total"})
    total_cell = total_row.find("td", {"class": "right"})
    percent = int(total_cell.text[:-1])
    return percent


def main():
    run_coverage()
    total_percent = get_total_percentage()
    if total_percent < CODE_COVERAGE_GOAL_PERCENTAGE:
        print(
            "Code covered by tests does not exceed "
            + str(CODE_COVERAGE_GOAL_PERCENTAGE)
            + "% check coverage_html_report/index.html for more information"
        )
        exit(256)


if __name__ == "__main__":
    main()
