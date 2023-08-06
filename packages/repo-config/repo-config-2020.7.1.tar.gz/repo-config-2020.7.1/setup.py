import setuptools

setuptools.setup(
    name='repo-config',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/.repo-config-fullname','scripts/.repo-config-init','scripts/.repo-config-load','scripts/.repo-config-save','scripts/repo-config']
)
