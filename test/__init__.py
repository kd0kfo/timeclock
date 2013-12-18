def test_date2unix(datetime):
    import subprocess
    import shlex

    cmd = "date2unix %s" % datetime
    output = subprocess.check_output(shlex.split(cmd))
    output = output.strip()
    retval = (output == "1387384320")
    if not retval:
        print("OUTPUT: %s" % output)
    return retval
