import click
import gzip
import requests

# TODO: repo and stats_len should be settings
repo = "http://ftp.uk.debian.org/debian/dists/stable/main"
stats_len = 10
packages_sum = {}


@click.command()
@click.argument("arch")
def main(arch):
    try:
        is_valid_arch(arch)
        file = f"Contents-{arch}.gz"
        url = f"{repo}/{file}"
        dest = f"/tmp/{file}"  # TODO: This should be a setting too
        download_file(url, dest)
        process_file(dest)
        print(result(packages_sum))
    except ValueError as e:
        print(e)  # TODO: Provide better messages ;-)
    except FileNotFoundError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print(e)


def is_valid_arch(arch):
    valid_archs = [
        "amd64",
        "arm64",
        "armel",
        "armhf",
        "i386",
        "mips",
        "mips64el",
        "mipsel",
        "ppc64el",
        "s390x",
        "source",
    ]
    if arch not in valid_archs:
        raise ValueError("You selected a wrong architecture")

    return True


def download_file(url, dest):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def process_file(dest):
    with gzip.open(dest, "r") as file:
        for line in file.readlines():
            packages = get_packages(line.decode("UTF-8"))
            for p in packages:
                total = packages_sum.get(p, 0) + 1
                packages_sum[p] = total


def get_packages(line):
    pack = line.split(" ")[-1].split(",")
    return [x.split("/")[-1].rstrip("\n") for x in pack]


def result(pkg):
    listR = sorted(pkg.items(), reverse=True, key=lambda x: x[1])[
        0:stats_len
    ]

    formP = str(max([len(x[0]) for x in listR])) + "s"
    formQ = str(max([len(str(x[1])) for x in listR])) + "d"
    ret = ''

    # TODO: Improve output format (using tabulate?)
    for i in range(stats_len):
        p = listR[i][0]
        t = listR[i][1]
        ret += f"{i+1:2d}. {p:{formP}} : {t:{formQ}}" + "\n"

    return ret
