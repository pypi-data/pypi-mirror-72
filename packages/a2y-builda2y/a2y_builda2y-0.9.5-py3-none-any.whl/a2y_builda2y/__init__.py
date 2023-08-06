from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
from os.path import splitext as _splitext


def build_a2y(ext_src_name, version, description='', install_requires=[]):
	basic_name = _splitext(ext_src_name)[0]
	ext_name = 'a2y_%s' % basic_name
	src_name = ext_src_name
	ext = Extension(name=ext_name, sources=[src_name])
	pkg_name = ext_name
	md_name = 'README.md'

	with open(md_name, 'r', encoding='utf8') as fh:
		long_description = fh.read()

	setup(
		name=pkg_name,
		version=version,
		author='Yu Han',
		author_email='hanjunyu@163.com',
		description=description,
		license='Private',
		platforms=['Windows', 'Linux'],
		long_description=long_description,
		long_description_content_type='text/markdown',
		url='http://www.sorobust.com/a2y/%s.html' % basic_name,
		ext_modules=cythonize(ext),
		install_requires=install_requires,
		classifiers=[
			"Development Status :: 4 - Beta",
			"Intended Audience :: Developers",
			"License :: Free For Educational Use",
			"Programming Language :: Python :: 3.5",
			"Operating System :: Microsoft :: Windows :: Windows 10",
			"Operating System :: POSIX :: Linux",
		],
	)


build_bin_pkg = build_a2y


def build_src_pkg(ext_org_name, version, description='', install_requires=tuple()):
	ext_name = 'a2y_%s' % ext_org_name
	pkg_name = ext_name
	md_name = 'README.md'

	with open(md_name, 'r', encoding='utf8') as fh:
		long_description = fh.read()

	setup(
		name=pkg_name,
		version=version,
		author='Yu Han',
		author_email='hanjunyu@163.com',
		description=description,
		license='Private',
		platforms=['Windows', 'Linux'],
		long_description=long_description,
		long_description_content_type='text/markdown',
		url='http://www.sorobust.com/a2y/%s.html' % ext_org_name,
		packages=find_packages(),
		install_requires=list(install_requires),
		classifiers=[
			"Development Status :: 4 - Beta",
			"Intended Audience :: Developers",
			"License :: Free For Educational Use",
			"Programming Language :: Python :: 3.5",
			"Operating System :: Microsoft :: Windows :: Windows 10",
			"Operating System :: POSIX :: Linux",
		],
	)
