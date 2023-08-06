from distutils.core import setup

setup(
    name='PassportSDK',
    version='0.0.1.1',
    description=(
      'SDK of passport-micro-service'
    ),
    author='NoahWang',
    author_email='234082230@qq.com',
    maintainer='noahwang',
    maintainer_email='234082230@qq.com',
    license='',
    py_modules=[
        'passportsdk.client',
        'passportsdk.common'
    ]
)
