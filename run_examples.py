import os
from modelrunner import submit_jobs

files = []
path = os.getcwd()

if "output_files" not in os.listdir(path):
    os.mkdir("output_files")
inpath = path+"/input_files"
outpath = path+"/output_files"
params1 = {"a": [1,2,3,4,5]}
                   
params2 = {"N": [50,100,150,2137],
          "maxprocs": [2,5,10]
           }

params3 = {#"options": {"n_iters": 1},
          "courant_field_multiplier": [(0.25,0.5),(-0.25,0.5)],
          "output_steps": [24,48,64]
          }


for fn in os.listdir(f"{path}/test_files"):
    if "child" not in fn and fn.endswith(".py"):
        files.append(fn)

if __name__ == "__main__":
        submit_jobs(f"{inpath}/{files[0]}",
                    name_base=f"{files[0][:-3]_out}",
                    parameters=params1,
                    output_folder="output_files",
                    output_format="hdf5",
                    method="srun"
                    )

        # submit_jobs(f"{inpath}/{files[1]}",
        #             parameters=params2,
        #             name_base=f"{files[1][:-3]}_out",
        #             output_folder=outpath,
        #             output_format="hdf5",
        #             method="srun"
        #             )
        
        # submit_jobs(f"{inpath}/{files[2]}",
        #             parameters=params3,
        #             name_base=f"{files[2][:-3]}_out",
        #             output_folder=outpath,
        #             output_format="hdf5",
        #             method="srun"
        #             )
