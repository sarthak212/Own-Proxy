import setuptools

with open('README.md','r') as fl:
    long_description = fl.read()

setuptools.setup(
        name="Own Custom Proxy",
        version="0.0.1",
        author="Shoaib Ahmed, Sarthak Kaushik",
        author_email="shoib@shoib.com, kaushiksarthak@yandex.com",
        description="Create Proxy on your remote linux server",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/sarthak212/Own-Proxy",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "Licese :: OSI Approved :: MIT License",
            "Operating System :: Linux",
            ],
        python_requires='>=3.6',
        entry_points = {
            'console_scripts' : ['ownproxy-client=client._main:run',
                                'ownproxy-server=server._main:run'],
            }
)
