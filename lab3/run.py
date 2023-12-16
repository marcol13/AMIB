import itertools
import os

from multiprocessing.pool import Pool

directory = "lab3"
hof_name = f"{directory}/HoF"
iters = 10


def generate(item):
    n, params = item

    cmd_command = f"python FramsticksEvolution.py -path %DIR_WITH_FRAMS_LIBRARY%  -sim \"eval-allcriteria.sim;deterministic.sim;sample-period-longest.sim;wlasne-prawd-{params['method']}.sim\" -opt velocity -max_numparts 15 -max_numjoints 30 -max_numneurons 20 -max_numconnections 30 -genformat 1 -pxov 0 -popsize 50 -generations 90 -hof_size 1 -method {params['method']} -hof_savefile {get_file_name(params, n)}.gen"

    os.system(cmd_command)


def params_to_string(params):
    str_list = [f"{value}" for _, value in params.items()]

    return "-".join(str_list)


def get_file_name(params, n):
    return f"{hof_name}-{params_to_string(params)}-{n}"


def main():
    n = range(iters)
    params = {"genformat": (1,), "method": (3,)}

    param_list = [
        list(itertools.product((key,), value)) for key, value in params.items()
    ]
    param_list = list(itertools.product(*param_list))
    param_list = [dict(value) for value in param_list]
    items = itertools.product(n, param_list)

    with Pool() as pool:
        pool.imap_unordered(generate, items)
        pool.close()
        pool.join()


if __name__ == "__main__":
    main()
