from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).parent

requirements_path = here / "requirements" / "prod.txt"


def read_requirements(path):
    try:
        with path.open(mode="rt", encoding="utf-8") as fp:
            return list(filter(bool, [line.split("#")[0].strip() for line in fp]))
    except IndexError:
        raise RuntimeError(f"{path} is broken")


setup(
    name="pyarmyknife",
    author="D. de Lange",
    author_email="14880945+ddelange@users.noreply.github.com",
    setup_requires=["setuptools_scm"],
    install_requires=read_requirements(requirements_path),
    use_scm_version={
        "version_scheme": "guess-next-dev",
        "local_scheme": "dirty-tag",
        "write_to": "src/pyarmyknife/_repo_version.py",
        "write_to_template": 'version = "{version}"\n',
        "relative_to": __file__,
    },
    extras_require={"sklearn": ["scikit-learn"]},
    python_requires=">=3.5.0",
    include_package_data=True,
    package_data={},
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
