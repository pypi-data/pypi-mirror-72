from setuptools import setup
import distutils.command.check

class TestCommand(distutils.command.check.check):
    """Custom test command."""

    def run(self):

        # run tests using doctest
        import doctest
        
        # filters folder
        from rawls import scene
        from rawls import rawls
        from rawls import stats
        from rawls import utils

        print("==============================")
        print("Runs test command...")

        # pass test using doctest
        doctest.testmod(scene)
        doctest.testmod(rawls)
        doctest.testmod(stats)
        doctest.testmod(utils)

        distutils.command.check.check.run(self)


setup(
    name='rawls',
    version='1.0.1',
    description='RAW Light Simulation file reader/converter package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities'
    ],
    url='https://github.com/prise-3d/rawls',
    author='Jérôme BUISINE',
    author_email='jerome.buisine@univ-littoral.fr',
    license='MIT',
    packages=['rawls', 'rawls.scene'],
    install_requires=[
        'numpy',
        'Pillow',
        'scipy',
        'astropy'
    ],
    cmdclass={
        'test': TestCommand,
    },
    zip_safe=False)
