

class Clock:
    def load(self, filename=None):
        if filename:
            self.clock_filename = filename
        self.categories = {}
        with open(self.clock_filename, "r") as infile:
            for line in infile:
                tokens = line.split()
                if not tokens:
                    continue
                if tokens[0][0] == '#':
                    continue
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
            from timeclock import get_timestamp

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

    def print_times(self, query=None, alphabetic=False, name_map=None, payrate=None):
        if alphabetic:
            categories = sorted(self.categories)
        else:
            categories = self.categories
        elapsed_time = self.total_time()
        named_categories = {}
        missing_names = []
        for cat in categories:
            if query and cat != query:
                continue

            total_time = self.total_time(cat)
            if name_map:
                if cat in name_map:
                    alias = name_map[cat]
                    if alias in named_categories:
                        named_categories[alias] += total_time
                    else:
                        named_categories[alias] = total_time
                else:
                    missing_names.append(cat)

            suffix = str(total_time)
            if len(self.categories[cat]) % 2 != 0:
                suffix = "+ seconds\t{0:.2f} hrs".format(total_time / 3600.)
            else:
                suffix = " seconds\t{0:.2f} hrs".format(total_time / 3600.)
            if payrate is not None:
                suffix += " ${0:.2f}".format(payrate * (total_time / 3600.))
            print("{0}: {1}{2}\t{3:0.2f}%"
                  .format(cat,
                          total_time,
                          suffix,
                          100. * total_time / elapsed_time))

        if named_categories:
            print("")
            print("Effort Categories:")

            for effort in named_categories:
                print("{}: {:0.2f} hours"
                      .format(effort, named_categories[effort] / 3600.))

            if missing_names:
                print("")
                print("Missing categories in name list: {}"
                      .format(", ".join(missing_names)))

    def punch(self, category, timestamp=None):
        from timeclock import get_timestamp
        if not timestamp:
            _timestamp = get_timestamp()
        else:
            _timestamp = timestamp
        with open(self.clock_filename, "a") as outfile:
            outfile.write("{0}\t{1}\n".format(category, _timestamp))

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

    def last_punch(self):
        last = None
        for (category, last_punch) in self.running_tasks():
            if last is None or last_punch > last[1]:
                last = (category, last_punch)

        return last

    def largest_running_time(self, category):
        from timeclock import get_timestamp
        if not category in self.categories:
            raise Exception("{0} is not a known category".format(category))

        largest = None
        times = self.categories[category]

        idx = 0
        len(times)
        num_times = len(times)
        while idx < num_times:
            start = times[idx]
            idx += 1
            if idx >= num_times:
                stop = get_timestamp()
            else:
                stop = times[idx]
            idx += 1

            thetime = stop - start

            if largest is None:
                largest = (thetime, start, stop)
            else:
                if thetime > largest[0]:
                    largest = (thetime, start, stop)

        return largest
