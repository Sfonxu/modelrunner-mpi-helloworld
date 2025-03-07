print: print.py
	mpirun -np 2 --tag-output python -m modelrunner print.py
	mpirun -np 2 --tag-output python -m modelrunner print.py --a=2
	mpirun -np 2 --tag-output python -m modelrunner print.py --a=4
