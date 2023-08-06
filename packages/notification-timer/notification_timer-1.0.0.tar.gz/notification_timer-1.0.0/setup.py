

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="notification_timer", # Replace with your own username
    version="1.0.0",
    author="KARTHIKEYAN MUTHU",
    author_email="phenomenalkarthikeyan@gmail.com",
    description="Package To Push Notification and Keep User Motivated",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheMLEngineer/notification_timer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


