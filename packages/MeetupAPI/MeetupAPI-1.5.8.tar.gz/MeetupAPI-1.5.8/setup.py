import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MeetupAPI",  # Replace with your own username
    version="1.5.8",
    author="Marco",
    author_email=None,
    description="Use the combined power of the official Meetup API and a web scraper to implement Meetup into your project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glowingkitty/Meetup-API",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'PyWebScraper',
        'geopy',
        'langdetect'
    ]
)
