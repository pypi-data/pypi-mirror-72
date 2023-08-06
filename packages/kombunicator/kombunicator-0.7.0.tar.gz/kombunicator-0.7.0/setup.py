import sys
import setuptools
from pathlib import Path


# add kombunicator to path so we can import kombunicator.utils:get_version
ROOT = str(Path(__file__).resolve().parent)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


from kombunicator.utils import get_version  # noqa: E402


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kombunicator",
    version=get_version(file_name='release_info', version_string='RELEASE_VERSION'),
    author="Stefan Lasse",
    author_email="stefanlasse87+kombunicator@gmail.com",
    description="A threaded RabbitMQ message producer/consumer and RPC client/server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mbio/kombunicator",
    download_url="https://gitlab.com/mbio/kombunicator/-/archive/master/kombunicator-master.tar.gz",
    keywords=["AMQP", "RPC", "kombu", "celery"],
    packages=["kombunicator"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "celery>=4.4.2",
        "kombu>=4.6.8",
        "strongtyping>=1.1.17",
    ],
    python_requires='>=3.6',
    include_package_data=True
)
