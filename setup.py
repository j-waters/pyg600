from setuptools import setup, find_packages

setup(
	name='pyg600',
	version_config={
		"template": "{tag}",
		"dev_template": "{tag}.dev{ccount}+git.{sha}",
		"dirty_template": "{tag}.dev{ccount}+git.{sha}.dirty",
		"starting_version": "0.0.1",
		"version_file": "",
		"count_commits_from_version_file": False
	},
	author="James Waters",
	author_email="james@jcwaters.co.uk",
	description="Utility program for binding actions to keys on the Logitech G600 gaming mouse",
	url="https://github.com/j-waters/pyg600",
	py_modules=['g600'],
	install_requires=['PyYAML', 'Click', 'evdev'],
	setup_requires=['setuptools-git-versioning'],
	entry_points='''
        [console_scripts]
        pyg600=g600:main_loop
    ''',
	python_requires='>=3.7',
)
