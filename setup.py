from setuptools import setup

setup(
    name='punchout',
    version='0.1',
    py_modules=['punchout'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        punchout=punchout:cli
    ''',
)
