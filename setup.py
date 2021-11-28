from setuptools import setup, find_packages


setup(
    name='django-paddle',
    version='0.0.11',
    packages=find_packages(),
    description='Django models for integrating Paddle.com subscriptions',
    url='https://github.com/kennell/django-paddle',
    author='Kevin Kennell',
    author_email='kevin@kennell.de',
    install_requires=[
        'django',
        'requests',
        'cryptography',
        'phpserialize'
    ],
    extras_require={
        'dev': [
            'responses',
        ]
    }
)
