class Instance:
    """Class representing an instance of the JSP."""
    def __init__(self, jobs, m, machineCapability):
        self.jobs = jobs
        self.machineCapability = machineCapability
        self.dur = [[d[0]/cap for d in self.jobs] for cap in machineCapability]
        self.n = len(jobs) # number of jobs
        self.m = m         # number of machines

    # I[0] => I.jobs[0]
    def __getitem__(self, i):
        return self.jobs[i]

    def getDuration(self, jobMachine):
        return self.dur[jobMachine[1]][jobMachine[0]]

    # len(I) => len(I.jobs)
    def __len__(self):
        return len(self.jobs)