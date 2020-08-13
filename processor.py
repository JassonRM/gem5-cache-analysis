import m5
from m5.objects import *
from benchmark_selector import *
from caches import *
import argparse


# Construct the argument parser
ap = argparse.ArgumentParser(prefix_chars='-')
# Add the arguments to the parser
ap.add_argument("-clk", "--clk", required=False)
ap.add_argument("-mem_range", "-mem_range", required=False)
ap.add_argument("-bench_path", "-bench_path", required=False)
ap.add_argument("-gem_path", "--gem_path", required=False)
ap.add_argument("-benchmark", "--benchmark", required=False)
ap.add_argument("-bench_size", "--bench_size", required=False)
ap.add_argument("-threads", "--threads", required=False)

ap.add_argument("-l1_assoc", "--l1_assoc", required=False)
ap.add_argument("-l1_tag_lat", "--l1_tag_lat", required=False)
ap.add_argument("-l1_dat_lat", "--l1_dat_lat", required=False)
ap.add_argument("-l1_resp_lat", "--l1_resp_lat", required=False)
ap.add_argument("-l1_repl_pol", "--l1_repl_pol", required=False)
ap.add_argument("-l1_prefetch", "--l1_prefetch", required=False)
ap.add_argument("-l1_inst_size", "--l1_inst_size", required=False)
ap.add_argument("-l1_dat_size", "--l1_dat_size", required=False)

ap.add_argument("-l2_assoc", "--l2_assoc", required=False)
ap.add_argument("-l2_tag_lat", "--l2_tag_lat", required=False)
ap.add_argument("-l2_dat_lat", "--l2_dat_lat", required=False)
ap.add_argument("-l2_resp_lat", "--l2_resp_lat", required=False)
ap.add_argument("-l2_repl_pol", "--l2_repl_pol", required=False)
ap.add_argument("-l2_prefetch", "--l2_prefetch", required=False)
ap.add_argument("-l2_size", "--l2_size", required=False)

args = vars(ap.parse_args())

# processor.py -clk=1GHz -mem_range=512MB -bench_path=/home/marco/Documents/Projects/gem5-analysis-with-parsec/benchmarks -benchmark=canneal -bench_size=test -threads=1 -l1_assoc=2 -l1_tag_lat=2 -l1_dat_lat=2 -l1_resp_lat=2 -l1_inst_size=16kB -l1_dat_size=64kB -l2_assoc=8 -l2_tag_lat=20 -l2_dat_lat=20 -l2_resp_lat=20 -l2_size=256kB


CLK_FREQ = args["clk"]
MEM_RANGE = args["mem_range"]
BENCHMARKS_PATH = args["bench_path"]
BENCHMARK = Benchmark[args["benchmark"]]
BENCHMARK_SIZE = Size[args["bench_size"]]
THREADS = int(args["threads"])

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
system.cpu.icache = L1ICache(args["l1_assoc"], args["l1_tag_lat"], args["l1_dat_lat"], args["l1_resp_lat"],
                             args["l1_inst_size"])


system.cpu.dcache = L1DCache(args["l1_assoc"], args["l1_tag_lat"], args["l1_dat_lat"], args["l1_resp_lat"],
                             args["l1_dat_size"])

# Connect caches to CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

system.l2cache = L2Cache(args["l2_assoc"], args["l2_tag_lat"], args["l2_dat_lat"], args["l2_resp_lat"],
                         args["l2_size"])

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
