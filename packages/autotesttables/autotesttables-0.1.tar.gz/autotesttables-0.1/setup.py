from distutils.core import setup

setup(
    name="autotesttables",
    packages=["autotesttables"],
    version="0.1",
    license="MIT",
    description="AutoTestTables is Python package made to further automate testing, by automatically generating test tables.",  # Give a short description about your library
    author="Ethan",
    author_email="skelmis.craft@gmail.com",
    url="https://github.com/Skelmis/autotesttables",
    download_url="https://github.com/Skelmis/autotesttables/archive/V0.1.tar.gz",
    keywords=[
        "Automated test tables",
        "testing",
        "unittest",
    ],  # Keywords that define your package best
    install_requires=["xlsxwriter",],
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
