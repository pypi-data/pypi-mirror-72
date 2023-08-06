import re
import requests
import click

pypi_website_url = "https://pypi.org/"

@click.group()
def statistics():
    """Get statistics of pypi.org. How many projects, how many releases, how many files and how many users?
    """
    pass

@statistics.command()
def projects():
    """Get how many projects on pypi.org.
    """
    response = requests.get(pypi_website_url)
    results = re.findall(b"""<p class="statistics-bar__statistic">[\r\n\t ]*([\d,]+) projects[\r\n\t ]*</p>""", response.content)
    projects = int(results[0].replace(b",", b"").decode())
    print(projects)

@statistics.command()
def releases():
    """Get how many releases on pypi.org.
    """
    response = requests.get(pypi_website_url)
    results = re.findall(b"""<p class="statistics-bar__statistic">[\r\n\t ]*([\d,]+) releases[\r\n\t ]*</p>""", response.content)
    releases = int(results[0].replace(b",", b"").decode())
    print(releases)

@statistics.command()
def files():
    """Get how many files on pypi.org.
    """
    response = requests.get(pypi_website_url)
    results = re.findall(b"""<p class="statistics-bar__statistic">[\r\n\t ]*([\d,]+) files</p>[\r\n\t ]*""", response.content)
    files = int(results[0].replace(b",", b"").decode())
    print(files)

@statistics.command()
def users():
    """Get how many users on pypi.org.
    """
    response = requests.get(pypi_website_url)
    results = re.findall(b"""<p class="statistics-bar__statistic">[\r\n\t ]*([\d,]+) users[\r\n\t ]*</p>""", response.content)
    users = int(results[0].replace(b",", b"").decode())
    print(users)

@statistics.command()
def all():
    """Get how many projects, release, files and users on pypi.org.
    """
    response = requests.get(pypi_website_url)
    content = response.content
    results = re.findall(b"""<p class="statistics-bar__statistic">[\r\n\t ]*([\d,]+) projects[\r\n\t ]*</p>""", response.content)
    projects = int(results[0].replace(b",", b"").decode())
    results = re.findall(b"""<p class="statistics-bar__statistic">[\r\n\t ]*([\d,]+) releases[\r\n\t ]*</p>""", response.content)
    releases = int(results[0].replace(b",", b"").decode())
    results = re.findall(b"""<p class="statistics-bar__statistic">[\r\n\t ]*([\d,]+) files[\r\n\t ]*</p>""", response.content)
    files = int(results[0].replace(b",", b"").decode())
    results = re.findall(b"""<p class="statistics-bar__statistic">[\r\n\t ]*([\d,]+) users[\r\n\t ]*</p>""", response.content)
    users = int(results[0].replace(b",", b"").decode())
    print("""{0:-11d} projects
{1:-11d} releases
{2:-11d} files
{3:-11d} users
    """.format(projects, releases, files, users))

if __name__ == "__main__":
    statistics()
