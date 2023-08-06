from setuptools import setup

def readme():
	with open('README.md') as f:
		README= f.read()
	return README

setup(
	name="aws-django-deploy",
	version = "1.0.1",
	description="A Python package to deploy django applications on AWS cloud ec2 instance",
	long_description=readme(),
	long_description_content_type="text/markdown",
	url="https://github.com/avinashkatariya/awsdjangodeploy",
	author="Avinash Katariya",
	author_email="avinashkatariya810@gmail.com",
	license="MIT",
	classifiers = [
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.7",
	],
	packages = ["awsdjangodeploy"],
	include_package_data = True,
	install_requires = [],
	entry_points = {
		"console_script":[
		 	"aws_django_deploy = awsdjangodeploy.cc:main",
		]
	}
)


