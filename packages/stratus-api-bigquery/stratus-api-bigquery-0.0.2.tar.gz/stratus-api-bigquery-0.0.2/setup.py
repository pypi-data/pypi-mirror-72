import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
# with open('requirements.txt') as f:
#     requirements = f.readlines()

setuptools.setup(
    name="stratus-api-bigquery",  # Replace with your own username
    version="0.0.2",
    author="DOT",
    author_email="dot@adara.com",
    description="Streamlined Celery Task",
    long_description="",
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://bitbucket.org/adarainc/stratus-api-tasks",
    setup_requires=['pytest-runner'],
    packages=['stratus_api.bigquery'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "stratus-api-core>=0.0.6",
        "stratus-api-jobs>=0.0.2",
        "celery[redis]==4.4.2"
    ]
)
