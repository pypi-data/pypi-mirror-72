from setuptools import setup, find_packages

setup(
    name='wechatntf',
    version='1.11.2',
    packages=find_packages(),
    data_files = ["/usr/local/wechatntf_config.ini"],
    install_requires=[
        "requests>=2.23.0"
    ],
    license='GNU General Public License v3.0',
    url = "https://www.mengma021.com",
    author='xinghuaizhen',
    author_email='xinghuaizhen1989@gmail.com',
    description='An wechat notification app, using api from WxPusher, only for personal '
)
