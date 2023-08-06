import setuptools

setuptools.setup(
    name="RobotFrameworkSlackNotifier", # Replace with your own username
    version="0.0.6",
    author="Patdroidz",
    author_email="patdroidz@gmail.com",
    description="RobotFrameworkSlackNotifier",
    long_description="RF Notifier for Slack",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
