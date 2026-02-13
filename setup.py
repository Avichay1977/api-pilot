from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='api-pilot',
    version='0.1.0',
    author='Avichay1977',
    description='Deterministic, CI-safe API key resolution with optional runtime validation (stdlib-only)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Avichay1977/api-pilot',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'api-pilot=api_pilot.cli:validate_cli',
            'api-pilot-doctor=api_pilot.cli:doctor',
        ],
    },
)
