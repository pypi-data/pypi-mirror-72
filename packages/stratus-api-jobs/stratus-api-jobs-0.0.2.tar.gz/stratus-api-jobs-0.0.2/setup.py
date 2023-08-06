import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
# with open('requirements.txt') as f:
#     requirements = f.readlines()

setuptools.setup(
    name="stratus-api-jobs",  # Replace with your own username
    version="0.0.2",
    author="DOT",
    author_email="dot@adara.com",
    description="Streamlined Celery Task",
    long_description="",
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://bitbucket.org/adarainc/stratus-api-tasks",
    setup_requires=['pytest-runner'],
    packages=['stratus_api.jobs'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "stratus-api-core>=0.0.8",
        "stratus-api-document>=0.0.4",
        "stratus-api-events>=0.0.3",
        "stratus-api-tasks>=0.0.4"
    ]
)
