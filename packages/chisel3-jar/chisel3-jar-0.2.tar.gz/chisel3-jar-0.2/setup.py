# coding:utf-8

from setuptools import setup

setup(
    name="chisel3-jar",
    url='https://github.com/jlsemi',
    packages=["chisel3_jar"],
    package_data={
        "chisel3_jar": [
            "jars/chisel3.jar",
        ],
    },
    use_scm_version={"relative_to": __file__, "write_to": "chisel3_jar/version.py",},
    author="Leway Colin@JLSemi",
    author_email="colinlin@jlsemi.com",
    description=(
        "Chisel3 Jar is a fat JAR with all of its dependencies."
    ),
    license="Apache-2.0 License",
    keywords=[
        "chisel",
    ],
    entry_points={"console_scripts": ["chisel3_jar = chisel3_jar.main:main"]},
    setup_requires=["setuptools_scm",],
    install_requires=[
    ],
    # Supported Python versions: 3.6+
    python_requires=">=3.6",
)
