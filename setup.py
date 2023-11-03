from setuptools import setup

setup(
    name='robit',
    version='0.4.4',
    author='Nathan Johnson & Wesley Howery',
    author_email='info@stratusadv.com',
    description='Chronological Automation Service Framework',
    keywords=['automation', 'bot', 'cron', 'cronjob', 'chronological', 'worker', 'job'],
    long_description=open('README.md').read(),
    url='https://github.com/stratusadv/robit',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=['pytz'],
)