import setuptools

setuptools.setup(
    name="rf_notifier-pkg-patdroidz", # Replace with your own username
    version="0.0.1",
    author="Patdroidz",
    author_email="patdroidz@gmail.com",
    description="RF Notifier",
    long_description="RF Notifier for Slack",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
