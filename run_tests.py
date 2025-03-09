from modelrunner import make_model, submit_job


@make_model
def multiply(a: float = 1, b: float = 2):
    """Multiply two numbers."""
    return a * b


if __name__ == "__main__":
    submit_job(__file__,  method="srun")
