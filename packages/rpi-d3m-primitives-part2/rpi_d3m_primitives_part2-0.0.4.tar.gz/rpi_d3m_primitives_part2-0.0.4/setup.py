from setuptools import setup, find_packages
import os
import subprocess
try:
	subprocess.call(["update-java-alternatives", "-s", "java-1.8.0-openjdk-amd64"])
except:
	pass


setup(
	name='rpi_d3m_primitives_part2',  
	version='0.0.4',  
	author='Naiyu Yin, Zijun Cui, Yuru Wang, Qiang Ji',
	author_email='yinn2@rpi.edu',
	url='https://gitlab.com/N.Yin/rpi-d3m-part2.git',
	description='Partial RPI primitives for D3M. Including structured classifier and global causal discovery.',
	platforms=['Linux', 'MacOS'],
        keywords = 'd3m_primitive',
	entry_points = {
		'd3m.primitives': [
            'classification.structured.RPI = rpi_d3m_primitives_part2.StructuredClassifier:StructuredClassifier',
            'classification.global_causal_discovery.RPI = rpi_d3m_primitives_part2.GlobalCausalDiscovery:GlobalCausalDiscovery'
			],
	},
	install_requires=[
		'd3m', 
		'javabridge==1.0.19',
		'pgmpy==0.1.9', 
		'pydot',
		'networkx', 
		'numpy', 
		'scipy', 
		'pandas', 
		'torch', 
		'pyparsing', 
		'statsmodels', 
		'tqdm', 
		'joblib'
	],
	packages=find_packages()
)
