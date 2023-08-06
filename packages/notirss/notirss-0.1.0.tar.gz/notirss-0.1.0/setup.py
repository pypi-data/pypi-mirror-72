from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='notirss',
    py_modules=['notirss'],
    version='0.1.0',
    description='Simple CLI RSS real-time notifier via webhook.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ivan Gonzalez',
    author_email='alo@ivgo.me',
    entry_points={'console_scripts': ['notirss=notirss:cli']},
    install_requires=['feedparser', 'requests'],
    python_requires='>=3.6'
)
