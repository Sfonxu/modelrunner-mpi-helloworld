from modelrunner import ModelBase
import numpy as np

class TestClass(ModelBase):
    parameters_default = {"a": 1}

    def __call__(self):
        for _ in np.arange(a):
            print("Hello World!")

model = TestClass()
