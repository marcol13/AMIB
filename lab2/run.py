import itertools
import os

from multiprocessing.pool import Pool

directory = "lab2"
hof_name = f"{directory}/HoF"
iters = 3

def generate(item):
    n, params = item
    f = params["genformat"]
    method = params["new_method"]

    cmd_command = f"python FramsticksEvolution.py -path %DIR_WITH_FRAMS_LIBRARY%  -sim \"eval-allcriteria.sim;deterministic.sim;sample-period-2.sim;only-body.sim\"  -opt vertpos -max_numparts 30   -genformat {f}   -popsize 50    -generations 90 -hof_size 1 -hof_savefile {get_file_name(params, n)}.gen -new_method {method}"

    os.system(cmd_command)

def params_to_string(params):
    str_list = [f"{value}" for _, value in params.items()]

    return "-".join(str_list)

def get_file_name(params, n):
    return f"{hof_name}-{params_to_string(params)}-{n}"

def main():
    n = range(iters)
    params = {
        "genformat": (0, 1, 4, 9),
        "new_method": (0, 1)
    }

    param_list = [list(itertools.product((key, ), value)) for key, value in params.items()]
    param_list = list(itertools.product(*param_list))
    param_list = [dict(value) for value in param_list]
    items = itertools.product(n, param_list)
    # print(list(items))

    with Pool() as pool:
        pool.imap_unordered(generate, items)
        pool.close()
        pool.join()


if __name__ == "__main__":
    main()

