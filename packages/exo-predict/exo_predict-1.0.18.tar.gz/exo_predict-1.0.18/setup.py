from setuptools import setup, find_packages

setup(
    name='exo_predict',
    version= '1.0.18',
    description='exo_predict will help you determine how likely you are to find an exoplanet!',
    url='https://github.com/Rob685/codeastro_ml_planets',
    author='Jea Adams, Rob Tejada, Sofia Covarrubias',
    python_requires='>=3.6',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'sklearn',
        'numpy',
        'xgboost'
    ]
)
