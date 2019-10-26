import re
from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).parent

init_path = here / "src" / "pyarmyknife" / "__init__.py"

requirements_path = here / "requirements" / "prod.txt"


def read_version(path):
    with path.open(mode="rt", encoding="utf-8") as fp:
        txt = fp.read()

    try:
        pattern = r'^__version__ = "([^"]+)"\r?$'
        return re.findall(pattern, txt, re.M)[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")


def read_requirements(path):
    try:
        with path.open(mode="rt", encoding="utf-8") as fp:
            return list(
                filter(
                    bool,
                    [
                        line.split("#")[0].strip()
                        for line in fp
                        if not line.startswith("git+")
                    ],
                )
            )
    except IndexError:
        raise RuntimeError(f"{path} is broken")


setup(
    name="pyarmyknife",
    author="D. de Lange",
    author_email="14880945+ddelange@users.noreply.github.com",
    version=read_version(init_path),
    install_requires=read_requirements(requirements_path),
    extras_require={"sklearn": ["scikit-learn"]},
    python_requires=">=3.3.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": ["*.csv", "*.xml", "*.yaml"]},
    include_package_data=True,
)
