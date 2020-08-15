from m5.objects import Cache
from m5.params import *
from m5.objects.ReplacementPolicies import *
from m5.objects.Prefetcher import *

L1_REPLACEMENT_POLICY = MRURP()
L1_PREFETCHER = NULL
L2_REPLACEMENT_POLICY = LRURP()
L2_PREFETCHER = NULL


class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    replacement_policy = Param.BaseReplacementPolicy(L1_REPLACEMENT_POLICY, "Replacement policy")
    prefetcher = Param.BasePrefetcher(L1_PREFETCHER, "Prefetcher attached to cache")

    def __init__(self, assoc, tag_latency, data_latency, response_latency):
        self.assoc = assoc
        self.tag_latency = tag_latency
        self.data_latency = data_latency
        self.response_latency = response_latency
        super().__init__()

    def connectCPU(self, cpu):
        # need to define this in a base class!
        raise NotImplementedError

    def connectBus(self, bus):
        self.mem_side = bus.slave


class L1ICache(L1Cache):
    size = '16kB'

    def __init__(self, assoc, tag_latency, data_latency, response_latency, size):
        self.size = size
        super().__init__(assoc, tag_latency, data_latency, response_latency)

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port


class L1DCache(L1Cache):
    size = '64kB'

    def __init__(self, assoc, tag_latency, data_latency, response_latency, size):
        self.size = size
        super().__init__(assoc, tag_latency, data_latency, response_latency)

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port


class L2Cache(Cache):
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    replacement_policy = Param.BaseReplacementPolicy(L2_REPLACEMENT_POLICY, "Replacement policy")
    prefetcher = Param.BasePrefetcher(L2_PREFETCHER, "Prefetcher attached to cache")

    def __init__(self, assoc, tag_latency, data_latency, response_latency, size):
        self.assoc = assoc
        self.tag_latency = tag_latency
        self.data_latency = data_latency
        self.response_latency = response_latency
        self.size = size
        super().__init__()

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.master

    def connectMemSideBus(self, bus):
        self.mem_side = bus.slave


