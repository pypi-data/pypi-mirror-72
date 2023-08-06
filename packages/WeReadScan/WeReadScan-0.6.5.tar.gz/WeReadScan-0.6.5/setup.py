from setuptools import setup, find_packages
 
setup(
    #pip install nnn
    name = "WeReadScan", 
    version = "0.6.5",
    keywords = ("weread", "scan", "pdf", "convert", "selenium"),
    description = "WeRead PDF Scanner",
    long_description = "Scan the book on WeRead and convert to pdf",
    #协议
    license = "GPL Licence",
 
    url = "https://github.com/Algebra-FUN/WeReadScan",
    author = "Algebra-FUN",
    author_email = "2593991307@qq.com",
 
    #自动查询所有"__init__.py"
    packages = find_packages(),
    include_package_data = True,
    platforms = "window",
    #提示前置包
    install_requires = ['pillow','numpy','matplotlib','img2pdf','opencv-python']
)