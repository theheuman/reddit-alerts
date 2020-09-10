import os
from bs4 import BeautifulSoup
import typer
from typing import List


CODE_COVERAGE_GOAL_PERCENTAGE = 100


class TerminalColors:
    HEADER = "\033[95m"
    OK_BLUE = "\033[94m"
    OK_GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def run_coverage():
    typer.echo(f"{TerminalColors.HEADER}Running Code Coverage{TerminalColors.ENDC}\n")
    exit_code = os.system("coverage run --source=./src/ -m unittest testing.test")
    if exit_code != 0:
        typer.echo(f"{TerminalColors.FAIL}FAILED! Exiting...{TerminalColors.ENDC}")
        exit(exit_code)

    typer.echo(
        f"{TerminalColors.HEADER}Generating Report and Checking Code Coverage{TerminalColors.ENDC}"
    )
    os.system("coverage html")


def get_html(file_name) -> str:
    file = open(file_name, "r", encoding="utf8")
    return file.read()


def get_total_percentage(html: str) -> int:
    # now go parse the html lol
    soup = BeautifulSoup(html, "html.parser")
    total_row = soup.find("tr", {"class": "total"})
    total_cell = total_row.find("td", {"class": "right"})
    percent = int(total_cell.text[:-1])
    return percent


def get_individual_percentages(html: str) -> dict:

    soup = BeautifulSoup(html, "html.parser")
    percentages = {}

    individual_rows = soup.find_all("tr", {"class": "file"})
    for row in individual_rows:
        name_cell = row.find("td", {"class": "name"})
        name = name_cell.text
        percentage_cell = row.find("td", {"class": "right"})
        percent = int(percentage_cell.text[:-1])
        percentages[name] = percent
    return percentages


def main(
    args: List[str],
    goal_percentage_total: int = CODE_COVERAGE_GOAL_PERCENTAGE,
    goal_percentage_individual: int = CODE_COVERAGE_GOAL_PERCENTAGE,
):
    run_coverage()

    coverage_html_file = "coverage_html_report/index.html"
    html = get_html(coverage_html_file)

    total_percent = get_total_percentage(html)
    individual_percentages = get_individual_percentages(html)

    if total_percent < goal_percentage_total:
        typer.echo(
            f"\n{TerminalColors.FAIL}Code covered by tests does not exceed {CODE_COVERAGE_GOAL_PERCENTAGE}% check coverage_html_report/index.html for more information{TerminalColors.ENDC}"
        )
        exit(1)
    else:
        typer.echo(
            f"\n{TerminalColors.OK_BLUE}Code Coverage Goal Percentage of {CODE_COVERAGE_GOAL_PERCENTAGE}% Met!{TerminalColors.ENDC}"
        )


if __name__ == "__main__":
    typer.run(main)
