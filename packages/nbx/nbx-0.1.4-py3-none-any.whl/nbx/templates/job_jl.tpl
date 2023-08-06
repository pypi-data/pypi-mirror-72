#!/bin/sh

{% for k,v in job_header %}#SBATCH {{k}}={{v}}
{% endfor %}

source /etc/profile.d/modules.sh
module add openmind/singularity
export SINGULARITY_CACHEDIR=/om5/user/`whoami`/.singularity
singularity exec -B /om:/om,/om5:/om5,/om2:/om2, {{nbx_folder}}:/omx \
                                {{simg}} \
                                julia wrapper.jl \
                                --job-id   $SLURM_ARRAY_JOB_ID \
                                --task-id  $SLURM_ARRAY_TASK_ID \
                                --results-dir {{results_dir}}