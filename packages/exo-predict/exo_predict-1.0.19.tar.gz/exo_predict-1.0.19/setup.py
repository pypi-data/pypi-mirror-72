from setuptools import setup, find_packages

setup(
    name='exo_predict',
    version= '1.0.19',
    description='exo_predict will help you determine how likely you are to find an exoplanet!',
    url='https://github.com/Rob685/codeastro_ml_planets',
    author='Jea Adams, Rob Tejada, Sofia Covarrubias',
    python_requires='>=3.6',
    packages=find_packages(),
    package_data={'data': ['*.p']},
    install_requires=[
        'pandas',
        'sklearn',
        'numpy',
        'xgboost'
    ]
)
