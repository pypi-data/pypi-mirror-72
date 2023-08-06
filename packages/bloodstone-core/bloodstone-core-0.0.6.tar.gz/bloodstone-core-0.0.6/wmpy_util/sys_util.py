import subprocess


def excute(cmd, cwd=None, verbose=False):
    if isinstance(cmd, str):
        if verbose:
            print(cmd)
        run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    elif isinstance(cmd, list):
        cmd = [str(unit) for unit in cmd]
        if verbose:
            print(" ".join(cmd))
        run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    else:
        return None
    out = get_output_1(run, verbose)
    return out


def get_output(run, verbose):
    """ Display the output/error of a subprocess.Popen object
        if 'verbose' is True.
    """
    out = list()
    # 重定向标准输出
    while run.poll() == None:  # None表示正在执行中
        line = run.stdout.readline().decode("UTF-8", "ignore").strip()
        error_line = run.stderr.readline().decode("UTF-8", "ignore").strip()
        if line:
            out.append(line)
            if verbose:
                print(line)
        if error_line and verbose:
            print(error_line)

    if run.returncode == 0:
        print('Subprogram success')
    else:
        print('Subprogram failed')
    return "".join(out)


def get_output_1(run, verbose):
    out, err = run.communicate()
    out = out.decode("utf8", "ignore")
    if verbose:
        print(out)
        if err:
            print(err.decode("utf8", "ignore"))
    return out
