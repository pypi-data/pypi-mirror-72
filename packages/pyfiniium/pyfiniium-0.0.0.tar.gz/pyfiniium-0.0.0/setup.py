import setuptools
import versioneer

REQUIREMENTS = ["h5py", "pandas", "python >=3.6"]

setuptools.setup(
    name="pyfiniium",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Interact with Infiniium oscilloscopes",
    author="trent rehberger",
    author_email="trent@medtronic.com",
    packages=["pyfiniium"],
    install_requires=REQUIREMENTS,
    classifiers=["Programming Language :: Python :: 3",],
)
