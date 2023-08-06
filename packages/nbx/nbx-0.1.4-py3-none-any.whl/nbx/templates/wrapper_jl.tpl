#!/usr/bin/env julia

using ArgParse
include("./experiment.jl")

settings = ArgParseSettings()
@add_arg_table settings begin
    "--job-id"
        help = "Job-id provided by job manager"
    "--task-id", 
        help = "Task-id provided by job manager"
    "--results-dir", 
        help = "Directory where results are stored"
end

parsed_args = parse_args(ARGS, settings)
println("Parsed args:")
for (arg,val) in parsed_args
    println("  $arg  =>  $val")
end


t  = parsed_args["task-id"]
rd = joinpath(parsed_args["results-dir"],"$t")

xargs = sweep_params[t-1]
mkdir(rd)
run_nb_experiment(xargs...; task_id=t, results_dir=rd)




