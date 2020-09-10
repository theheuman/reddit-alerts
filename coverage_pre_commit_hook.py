import os
from bs4 import BeautifulSoup
import typer
from typing import List, Tuple


CODE_COVERAGE_GOAL_PERCENTAGE = 80


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


def passes_total_percentage(html: str, goal_percentage: int) -> bool:
    # now go parse the html lol
    soup = BeautifulSoup(html, "html.parser")
    total_row = soup.find("tr", {"class": "total"})
    total_cell = total_row.find("td", {"class": "right"})
    percent = int(total_cell.text[:-1])
    return percent >= goal_percentage


def passes_individual_percentages(html: str, goal_percentage: int) -> Tuple[bool, dict]:

    soup = BeautifulSoup(html, "html.parser")
    percentages = {}
    passes_percentage = True

    individual_rows = soup.find_all("tr", {"class": "file"})
    for row in individual_rows:
        name_cell = row.find("td", {"class": "name"})
        name = name_cell.text
        percentage_cell = row.find("td", {"class": "right"})
        percent = int(percentage_cell.text[:-1])
        if percent < goal_percentage:
            passes_percentage = False
            percentages[name] = percent

    return passes_percentage, percentages


def main(
    args: List[str],
    goal_percentage_total: int = CODE_COVERAGE_GOAL_PERCENTAGE,
    goal_percentage_individual: int = CODE_COVERAGE_GOAL_PERCENTAGE,
):
    run_coverage()

    coverage_html_file = "coverage_html_report/index.html"
    html = get_html(coverage_html_file)

    if not passes_total_percentage(html, goal_percentage_total):
        typer.echo(
            f"\n{TerminalColors.FAIL}Total code coverage is less than {goal_percentage_total}% check coverage_html_report/index.html for more information{TerminalColors.ENDC}"
        )
        exit(1)

    typer.echo(
        f"\n{TerminalColors.OK_BLUE}Total code coverage goal percentage of {goal_percentage_total}% Met!{TerminalColors.ENDC}"
    )

    passed_check, individual_percentages = passes_individual_percentages(
        html, goal_percentage_individual
    )
    if not passed_check:
        for file_name, percentage in individual_percentages.items():
            typer.echo(
                f"\n{TerminalColors.FAIL}Code coverage in {file_name} is only {percentage}% and does not exceed {goal_percentage_total}% check\n{TerminalColors.OK_GREEN}file://{os.getcwd()}/{coverage_html_file}\a\a{TerminalColors.ENDC}{TerminalColors.FAIL}\nfor more information{TerminalColors.ENDC}"
            )
        exit(1)

    typer.echo(
        f"\n{TerminalColors.OK_BLUE}Individual code coverage goal percentage of {goal_percentage_individual}% Met!{TerminalColors.ENDC}"
    )


if __name__ == "__main__":
    typer.run(main)
