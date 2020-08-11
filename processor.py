import m5
from m5.objects import *
from benchmark_selector import *
from caches import *

CLK_FREQ = '1GHz'
MEM_RANGE = '512MB'
BENCHMARKS_PATH = "/home/marco/Documents/Projects/gem5-analysis-with-parsec/benchmarks"
BENCHMARK = Benchmark.canneal
BENCHMARK_SIZE = Size.test
THREADS = 1

# Create system
system = System()

# Start of system configuration ---

# Set clock and voltage
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = CLK_FREQ
system.clk_domain.voltage_domain = VoltageDomain()

# Set memory mode and range
system.mem_mode = 'atomic'
system.mem_ranges = [AddrRange(MEM_RANGE)]

# Create CPU
system.cpu = AtomicSimpleCPU()

# Create Caches
system.cpu.icache = L1ICache(2, 2, 2, 2, '16kB')
system.cpu.dcache = L1DCache(2, 2, 2, 2, '64kB')

# Connect caches to CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

system.l2cache = L2Cache(8, 20, 20, 20, '256kB')
system.l2cache.connectCPUSideBus(system.l2bus)

# Create memory bus
system.membus = SystemXBar()

system.l2cache.connectMemSideBus(system.membus)

# Connect PIO and interrupt ports (x86-specific)
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave

isa = str(m5.defines.buildEnv['TARGET_ISA']).lower()

# Set memory controller
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# End of system configuration ---

# Create process
process = Process()
process.cmd = benchmark_selector(BENCHMARK, BENCHMARK_SIZE, BENCHMARKS_PATH, THREADS)
system.cpu.workload = process
system.cpu.createThreads()

# Instantiate system and begin execution
root = Root(full_system=False, system=system)
m5.instantiate()

# Begin simulation
print('Beginning simulation of benchmark ', BENCHMARK.name)
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
