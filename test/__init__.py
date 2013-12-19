TEST_CLOCK_FILE = "clock.test.dat"


def test_function(function):
    def tester():
        print("Testing %s" % getattr(function, "__name__"))
        retval = function()
        if not retval:
                print("FAILED")
                exit(1)
        else:
            print("Success!")
            print("")
        return retval

    return tester


def run_command(cmd):
    import shlex
    import subprocess
    return subprocess.check_output(shlex.split(cmd))


@test_function
def date2unix():
    import time
    from timeclock import get_timestamp
    from datetime import datetime as DT

    # Get current time data
    currunixtime = get_timestamp()
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


@test_function
def punchin():
    print(run_command("punch -f %s test" % TEST_CLOCK_FILE))
    return True


@test_function
def switch_punch():
    print(run_command("punch -f %s -s test2" % TEST_CLOCK_FILE))
    return True


@test_function
def punchout():
    print(run_command("punch -f %s stop" % TEST_CLOCK_FILE))
    return True


@test_function
def summary():
    output = run_command("punch -f %s" % TEST_CLOCK_FILE)
    print(output)
    expected = "Total counted time: 4 seconds (0.00 hrs)"

    return (expected in output)