#!/usr/bin/env python
import sys
sys.path.append("/omx") #This path will be bound to the nbx folder in run.sh
import numpy as np
from nbx.pspace import ParameterSpace, Axis


sweep_params = ParameterSpace([
{% for k,v in sweep_args %}	Axis("{{k}}", {{v}}),
{% endfor %}])


def print_args(arg_dict):
	print(f"**nbx**\nRunning Experiment...")
	for k,v in arg_dict.items():
		print(f"\t{k}: {v}")


def run_nb_experiment({% for k,v in args %}{{k}}={{v}}, {% endfor %}**kwargs):
	"""
	This is an auto-generated function 
	based on the jupyter notebook 

	> {{name}}
	
	Don't judge, it might look ugly.
	"""
	print_args(locals())


	{% for line in func_body %}{{line}}{% if not loop.last %}
	{% endif %}{% endfor %}


	print("\n**nbx**\nExperiment finished.")

