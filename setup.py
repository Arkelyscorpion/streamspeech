from setuptools import setup, find_packages
from pathlib import Path 

from streamspeech.version import __version__
link_to_use = "https://github.com/Nelson-Gon/streamspeech/archive/refs/tags/v"+__version__+".zip"
install_reqs = []
with open(f"{Path(__file__).parent}/requirements.txt", "r") as file:
    for line in file:
        install_reqs.append(line.replace("\n", ""))
setup(name='streamspeech',
      version=__version__,
      description='Text to Speech with Generative AI',
      url="http://www.github.com/Nelson-Gon/streamspeech",
      download_url=link_to_use,
      author='Nelson Gonzabato',
      author_email='gonzabato@hotmail.com',
      license='MIT',
      keywords="generative-ai speechbrain tts text-to-speech gan artificial-intelligence ai",
      packages=find_packages(),
      long_description=open('README.md', encoding="utf-8").read(),
      long_description_content_type='text/markdown',
      install_requires=install_reqs,
      python_requires='>=3.9',
      zip_safe=False)