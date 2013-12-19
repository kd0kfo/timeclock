def test_function(function):
    def tester():
        retval = function()
        if not retval:
                print("FAILED")
                exit(1)
        else:
            print("Success!")
        return retval

    return tester


def run_command(cmd):
    import shlex
    import subprocess
    return subprocess.check_output(shlex.split(cmd))

@test_function
def date2unix():
    import time
    from datetime import datetime as DT

    # Get current time data
    currunixtime = int(time.time())
    currdatetime = DT.fromtimestamp(currunixtime).strftime('%Y%m%d %H:%M')
    secoffset = DT.fromtimestamp(currunixtime).strftime('%S')
    currunixtime -= int(secoffset)
    print("Current Unix Time: %d" % currunixtime)
    print("Current Date Time: %s" % currdatetime)

    # Run script
    unixtime = run_command("date2unix %s" % currdatetime)
    unixtime = unixtime.strip()
    unixtime = int(unixtime)

    # Compare
    retval = (unixtime == currunixtime)
    print("Calculated Unix Time: %d" % unixtime)
    return retval


