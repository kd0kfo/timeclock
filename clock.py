

def get_timestamp():
    import time
    return int(time.time())

class Clock:
    def load(self, filename=None):
        if filename:
            self.clock_filename = filename
        self.categories = {}
        with open(self.clock_filename, "r") as infile:
            for line in infile:
                tokens = line.split()
                if len(tokens) != 2:
                    raise Exception("Broken line: {0}".format(line))
                cat = tokens[0]
                timestamp = int(tokens[1])
                if not tokens[0] in self.categories:
                    self.categories[cat] = [timestamp]
                else:
                    self.categories[cat].append(timestamp)

    def __init__(self, filename):
        from os.path import isfile

        self.categories = {}
        self.clock_filename = filename
        if isfile(self.clock_filename):
            self.load(self.clock_filename)

    def print_times(self):
        for cat in self.categories:
            punches = self.categories[cat]
            total_time = 0
            length = len(punches)
            if length  % 2 != 0:
                length -= 1
            idx = 0
            while idx < length:
                start = punches[idx]
                stop = punches[idx + 1]
                total_time += stop - start
                idx += 2

            if len(punches) % 2 != 0:
                total_time += get_timestamp() - punches[-1]
                suffix = "+ seconds"
            else:
                suffix = " seconds"
            print("{0}: {1}{2}".format(cat, total_time, suffix))

    def punch(self, category):
        with open(self.clock_filename, "a") as outfile:
            outfile.write("{0}\t{1}\n".format(category, get_timestamp()))

    def running_tasks(self):
        running = []
        
        for category in self.categories:
            if len(self.categories[category]) % 2 == 1:
                running.append((category, self.categories[category][-1]))
        return running
