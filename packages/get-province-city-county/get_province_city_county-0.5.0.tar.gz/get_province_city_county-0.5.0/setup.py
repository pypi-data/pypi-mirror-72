import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="get_province_city_county", # Replace with your own username
    version="0.5.0",
    author="白旭东",
    author_email="2216403312@qq.com",
    description="这是一个从文本提取中文地区的包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oldlwhite/get_province_city_county",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
