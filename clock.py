

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

    def total_time(self, category=None):
        def get_total_time(category):
            punches = self.categories[category]
            elapsed_time = 0
            length = len(punches)
            if length % 2 != 0:
                length -= 1
            idx = 0
            while idx < length:
                start = punches[idx]
                stop = punches[idx + 1]
                elapsed_time += stop - start
                idx += 2

            if len(punches) % 2 != 0:
                elapsed_time += get_timestamp() - punches[-1]

            return elapsed_time

        if not category:
            elapsed_time = 0
            for cat in self.categories:
                elapsed_time += get_total_time(cat)
            return elapsed_time
        return get_total_time(category)


    def print_times(self, query=None):
        for cat in self.categories:
            if query and cat != query:
                continue

            total_time = self.total_time(cat)
            suffix = str(total_time)
            if len(self.categories[cat]) % 2 != 0:
                suffix = "+ seconds ({0:.2f} hrs)".format(total_time/3600.)
            else:
                suffix = " seconds ({0:.2f} hrs)".format(total_time/3600.)
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

    def get_categories(self):
        return self.categories.keys()

    def get_timestamps(self):
        all_timestamps = []
        for times in self.categories.itervalues():
            all_timestamps.extend(times)
        return all_timestamps
