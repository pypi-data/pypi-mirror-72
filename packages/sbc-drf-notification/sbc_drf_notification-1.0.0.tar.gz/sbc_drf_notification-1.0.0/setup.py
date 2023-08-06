'''
pytz setup script
'''
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

me = 'Abhinav Kotak'
memail = 'in.abhi9@gmail.com'

packages = ['sbc_drf_notification', 'sbc_drf_notification.migrations']
package_dir = {'sbc_drf_notification': 'src/sbc_drf_notification'}
install_requires = open('requirements.txt', 'r').readlines()

setup(
    name='sbc_drf_notification',
    version=re.sub(r'^v', '', os.environ.get('CI_COMMIT_TAG'), flags=re.IGNORECASE),
    zip_safe=True,
    description='Notification app for SBC project.',
    author=me,
    author_email=memail,
    maintainer=me,
    maintainer_email=memail,
    install_requires=install_requires,
    url='https://gitlab.stickboycreative.com/sbc-libs/py/sbc_drf_notification',
    license=open('LICENSE', 'r').read(),
    keywords=['djangorestframework', 'drf', 'notification'],
    packages=packages,
    package_dir=package_dir,
    platforms=['Independant'],
    classifiers=[
        'Development Status :: 1 - beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
