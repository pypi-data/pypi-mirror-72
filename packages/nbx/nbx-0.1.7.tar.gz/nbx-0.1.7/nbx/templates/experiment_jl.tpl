#!/usr/bin/env julia
include("pspace.jl")

sweep_params = ParameterSpace([
{% for k,v in sweep_args %}	Axis("{{k}}", {{v}}),
{% endfor %}])


"""
This is an auto-generated function 
based on the jupyter notebook 

    {{name}}

Don't judge, it might look ugly.
"""
function run_nb_experiment({% for k,v in sweep_args %}{{k}}{% if not loop.last %}, {% endif %}{% endfor %}; {% for k,v in const_args %}{{k}}={{v}}{% if not loop.last %}, {% endif %}{% endfor %})

	{% for line in func_body %}{{line}}{% if not loop.last %}
	{% endif %}{% endfor %}


	println("\n**nbx**\nExperiment finished.")
end


#########
#########
#########

