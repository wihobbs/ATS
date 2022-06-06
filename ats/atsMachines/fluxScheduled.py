#ATS:slurm56 SELF FluxScheduled 3
#ATS:toss_4_x86_64_ib SELF FluxScheduled 16

from ats.atsMachines import lcMachines
import time
from math import ceil

## Must be on a Flux machine or with Flux broker running in Slurm allocation for these imports to work.

import flux
import flux.job
f = flux.Flux() ## defines a persistent handle to use to connect to the broker

## Do we need to request an allocation? On fluke if you issue Flux mini run it sends to a compute node automatically
## but there's no assurances it will be to the _same_ compute nodes for each of ats's "tests" or whatever
## answer: YES for now

## Should start its own Flux session!! TODO

class FluxScheduled(lcMachines.LCMachineCore):
    def init(self):
        ## anything to initialize here?
        ## set ceiling on number of nodes and cores in the allocation.
        self.maxNodes = int(flux.resource.list.resource_list(f).get().free.nnodes)
        self.maxCores = int(flux.resource.list.resource_list(f).get().free.ncores)
        self.coresPerNode = int(self.maxCores // self.maxNodes)

        ## overwritten machine things I don't understand.
        self.numberTestsRunningMax = self.maxCores
        import pdb 
        pdb.set_trace()
        ## set number of nodes

    def examineOptions(self, options):
        ## Option values for Flux 
        self.exclusive = options.exclusive

    def calculateCommandList(self, test):
        ## flux mini run commands will go here
        ret = "flux mini run".split()
        np = test.options.get('np', 1)
        nn = test.options.get('nn', 1)
        if np > self.coresPerNode:
            nn = ceil(np / self.coresPerNode)
        # import pdb 
        # print("np trace")
        # pdb.set_trace()
        
        # set number of nodes and cores
        ret.append(f"-N {nn}")
        ret.append(f"-n {np}")

        ## TODO: MPI job connection. Needs to be able to see how many cores it needs.

        # exclusivity set by default changed by shared ATS argument
        # requires: NN
        ## change to test exclusivity TODO
        if self.exclusive:
            ret.append("--exclusive")
        
        ## verbose mode, outputs to log file, could be useful
        ret.append("-vvv")

        # set job name
        test.jobname = f"{np}_{test.serialNumber}{test.namebase[0:50]}{time.strftime('%H%M%S',time.localtime())}"
        ret.append("--job-name")
        ret.append(test.jobname)

        return ret + self.calculateBasicCommandList(test)
    
    def canRun(self, test):
        ## get rid of this logic of "only if the resources are free can we submit the job"
        """
        if test.np > self.maxCores: 
            return f"Too many processors needed ({test.np} needed, {self.maxCores} available)"
        return ''
        """
        return ''
    
    def canRunNow(self, test):
        ## This should always be true in a flux instance. If it can't run now,
        ## submitting it to the queue will not affect it in the way it will Slurm.
        return True

    def periodicReport(self):
        ## Copied from SlurmProcessorScheduled lines 650-654
        "Report on current status of tasks"
        if len(self.running):
            terminal("CURRENTLY RUNNING %d tests:" % len(self.running),
                     " ".join([t.name for t in self.running]) )
        terminal("-"*80)

        ## Flux specific accessors for number of nodes
        
        procs = flux.resource.list.resource_list(f).get().allocated.nnodes
        total = flux.resource.list.resource_list(f).get().free.nnodes
        terminal(f"CURRENTLY UTILIZING {procs} of {total} processors.")
        terminal("-"*80)
        
    def remainingCapacity(self):
        return flux.resource.list.resource_list(f).get().free.ncores
