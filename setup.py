from setuptools import setup

setup(
    name="powermeter",
    description="Tools around the Hager powermeter inside shackspace",
    version="1.1.0",
    packages=["powermeter"],
    license="MIT",
    long_description=open("README.md").read(),
    author="Felix Richter",
    author_email="github@syntax-fehler.de",
    url="https://git.shackspace.de/rz/powermeter",
    install_requires=["pyserial","paho-mqtt","setuptools","redis"],
    tests_require=[],
    entry_points={
        "console_scripts": [
            "powermeter-mqtt2socket = powermeter.mqtt2socket:main",
            "powermeter-serial2mqtt = powermeter.serial2mqtt:main"
        ]
    },
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: System :: Software Distribution"
    ],
)

