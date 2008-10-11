from distutils.core import setup
import os

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

# snippet from http://django-registration.googlecode.com/svn/trunk/setup.py
for dirpath, dirnames, filenames in os.walk('ogone'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        print dirpath, filenames
        prefix = dirpath[6:] # Strip "ogone/" or "ogone\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(
	name='ogone',
	version='0.1',
	description='Django application for interfacing with Ogone (payment service provider)',
	author='Sander Smits',
	author_email='Sander Smits <jhmsmits@gmail.com>',
	url='http://github.com/jsmits/django-payment-ogone/',
	package_dir={'ogone': 'ogone'},
    packages=packages,
    package_data={'ogone': data_files},
	classifiers=[
		'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
	]
)
