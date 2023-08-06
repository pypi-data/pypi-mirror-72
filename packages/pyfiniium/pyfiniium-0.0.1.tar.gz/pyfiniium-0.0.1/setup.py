import setuptools
import versioneer

REQUIREMENTS = ["h5py", "pandas"]

setuptools.setup(
    name="pyfiniium",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url="https://github.com/misterWiz/pyfiniium.git",
    description="Interact with Infiniium oscilloscopes",
    author="trent rehberger",
    author_email="trent@medtronic.com",
    packages=["pyfiniium"],
    install_requires=REQUIREMENTS,
    python_requires=">=3.6",
    classifiers=["Programming Language :: Python :: 3",],
)
