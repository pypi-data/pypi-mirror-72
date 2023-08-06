import setuptools


# with open("README.md", "r") as fh:
# 	long_description = fh.read()

long_description = "wechat's utils"

setuptools.setup(
	name = "wechat-utils",
	version="2020.6.29.1",
	auth="hxh",
	author_email="13750192465@163.com",
	description=long_description,
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/cllen/wechat-utils",
	packages=setuptools.find_packages(),
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=[
		"peewee==3.13.1",
		"django_crequest==2018.5.11",
		"cryptography==2.3.1",
		"chardet==2.3.0",
		"flask_mongoengine==0.9.5",
		"lxml==4.5.0",
		"requests==2.21.0",
		"wechatpy==1.8.3",
		"itsdangerous==1.1.0",
		"Werkzeug==0.16.0",
		"flask_mongoengine_orm==0.0.6",
		"setuptools==41.0.1",
		"flask_restplus==0.12.1",
		"SQLAlchemy==1.3.11",
		"xmltodict==0.12.0",
		"six==1.10.0",
		"marshmallow==3.0.0b20",
		"Flask_Admin==1.5.5",
		"djangorestframework==3.11.0",
	],
)




