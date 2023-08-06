from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="lb_controller",
      version="0.0.9",
      description="A controller to auto configure k8s load balancer on premise",
      long_description=long_description,
      install_requires=[
        "kubernetes==10.0.1",
        "kubernetes_asyncio==10.0.0",
        "jinja2==2.10.3",
        "multidict==4.6.1",
        "aiohttp==3.6.1",
        "prometheus-client==0.7.1"],
      extras_require={"tests": ["pytest==4.6.3"]},
      packages=find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
)
