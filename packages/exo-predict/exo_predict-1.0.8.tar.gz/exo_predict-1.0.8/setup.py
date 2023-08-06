from setuptools import setup

setup(
    name='exo_predict',
    version= '1.0.8',
    description='exo_predict will help you determine how likely you are to find an exoplanet!',
    url='https://github.com/Rob685/codeastro_ml_planets',
    author='Jea Adams, Rob Tejada, Sofia Covarrubias',
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'sklearn',
        'numpy',
        'xgboost'
    ]
)
