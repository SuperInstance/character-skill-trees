"""
Setup configuration for character-skill-trees package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_file(filename):
    """Read file contents."""
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, filename), encoding='utf-8') as f:
        return f.read()

setup(
    name='character-skill-trees',
    version='1.0.0',
    author='LucidDreamer Team',
    author_email='contact@luciddreamer.ai',
    description='Advanced skill progression and specialization system for AI characters',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/luciddreamer/character-skill-trees',
    packages=find_packages(exclude=['tests', 'tests.*', 'examples', 'docs']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='ai, characters, skills, progression, rpg, game-development, skill-trees',
    python_requires='>=3.8',
    install_requires=[
        'numpy>=1.20.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.950',
        ],
        'examples': [
            'matplotlib>=3.5.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'skill-demo=character_skill_trees.demo:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/luciddreamer/character-skill-trees/issues',
        'Source': 'https://github.com/luciddreamer/character-skill-trees',
        'Documentation': 'https://github.com/luciddreamer/character-skill-trees/blob/main/README.md',
    },
)
