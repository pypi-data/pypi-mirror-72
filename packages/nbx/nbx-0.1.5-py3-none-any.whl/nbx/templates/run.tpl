#!/bin/sh

#SBATCH --job-name={{job_name}}
#SBATCH -t {{hours}}:{{mins}}:00
#SBATCH --ntasks={{ntasks}}
#SBATCH --array={{array_start}}-{{array_end}}%{{array_step}}
#SBATCH --mem-per-cpu {{mem_per_cpu}}
#SBATCH --mail-type=END
#SBATCH --mail-user={{mail_user}}
#SBATCH --out=io/out_%a
#SBATCH --error=io/err_%a
#SBATCH --exclude=node030,node016

source /etc/profile.d/modules.sh
module add openmind/singularity
export SINGULARITY_CACHEDIR=/om2/user/`whoami`/.singularity
singularity exec --nv -B /om:/om,/om2:/om2,{{nbx_folder}}:/omx {{simg}} \
                                python {{script}} \
                                --job-id   $SLURM_ARRAY_JOB_ID \
                                --task-id  $SLURM_ARRAY_TASK_ID \
                                --results-dir {{results_dir}}