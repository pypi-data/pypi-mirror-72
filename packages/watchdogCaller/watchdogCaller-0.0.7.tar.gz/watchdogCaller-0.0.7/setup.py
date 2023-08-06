from setuptools import setup, find_packages
setup(
    name="watchdogCaller",
    version="0.0.7",
    packages=find_packages(),
    entry_points={
          'console_scripts': [
              'watchdog-caller = watchdogCaller.main:cli'
          ]
      },
    #   scripts=["watchdog-caller"],

    install_requires=["watchdog==0.10.2"],

    # metadata to display on PyPI
    author="John Alejandro González",
    author_email="johnalejandrog.g4@gmail.com",
    description="A Python script that calls an API when a directory is not modified in a especified timeout-time.",
    keywords="watchdog security python script filesystem api http https auth auditory timeout",
    url="https://github.com/KurtCoVayne/Watchdog-api-caller", 
    project_urls={
        "Bug Tracker": "https://github.com/KurtCoVayne/Watchdog-api-caller",
        "Documentation": "https://github.com/KurtCoVayne/Watchdog-api-caller",
        "Source Code": "https://github.com/KurtCoVayne/Watchdog-api-caller",
    },
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]

)