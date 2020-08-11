import enum


class Benchmark(enum.Enum):
    bzip2 = 1;
    mcf = 2;
    hmmer = 3;
    sjeng = 4;
    lbm = 5;
    blackscholes = 6;
    canneal = 7;
    streamcluster = 8;


class Size(enum.Enum):
    test = 1;
    simdev = 2;
    simsmall = 3;
    simmedium = 4;
    simlarge = 5;
    native = 6;

def bzip2(benchmarks_folder):
    binary = benchmarks_folder + "/401.bzip2/src/benchmark"
    parameters = [benchmarks_folder + "/401.bzip2/data/input.program", 10]
    return [binary] + parameters


def mcf(benchmarks_folder):
    binary = benchmarks_folder + "/429.mcf/src/benchmark"
    parameters = [benchmarks_folder + "/429.mcf/data/inp.in"]
    return [binary] + parameters


def hmmer(benchmarks_folder):
    binary = benchmarks_folder + "/456.hmmer/src/benchmark"
    parameters = ['--fixed', 0, '--mean', 325, '--num', 45000, '--sd', 200, '--seed', 0, benchmarks_folder + '/456.hmmer/data/bombesin.hmm']
    return [binary] + parameters


def sjeng(benchmarks_folder):
    binary = benchmarks_folder + "/458.sjeng/src/benchmark"
    parameters = [benchmarks_folder + '/458.sjeng/data/test.txt']
    return [binary] + parameters


def lbm(benchmarks_folder):
    binary = benchmarks_folder + "/470.lbm/src/benchmark"
    parameters = [20, benchmarks_folder + '/470.lbm/data/reference.dat', 0, 1, benchmarks_folder + '/470.lbm/data/100_100_130_cf_a.of']
    return [binary] + parameters


def blackscholes(size, benchmarks_folder, threads):
    binary = benchmarks_folder + "/blackscholes/blackscholes"
    test = {
        Size.test: 'test.txt',
        Size.simdev: 'simdev.txt',
        Size.simsmall: 'simsmall.txt',
        Size.simmedium: 'simmedium.txt',
        Size.simlarge: 'simlarge.txt',
        Size.native: 'native.txt'
    }
    parameters = [
        benchmarks_folder + "/blackscholes/inputs/input_" + test.get(size, "size debe ser un elemento del enum Size"),
        benchmarks_folder + "/blackscholes/outputs/output_" + test.get(size, "size debe ser un elemento del enum Size")]
    return [binary, threads] + parameters


def canneal(size, benchmarks_folder, threads):
    binary = benchmarks_folder + "/canneal/canneal"
    test = {
        Size.test: [5, 100, 'test.nets', 1],
        Size.simdev: [100, 300, 'simdev.nets', 2],
        Size.simsmall: [10000, 2000, 'simsmall.nets', 32],
        Size.simmedium: [15000, 2000, 'simmedium.nets', 64],
        Size.simlarge: [15000, 2000, 'simlarge.nets', 128],
        Size.native: [15000, 2000, 'simnative.nets', 6000]
    }
    parameters = test.get(size, "size debe ser un elemento del enum Size")
    if isinstance(parameters, list):
        parameters[2] = benchmarks_folder + "/canneal/inputs/input_" + parameters[2]
    return [binary, threads] + parameters


def streamcluster(size, benchmarks_folder, threads):
    binary = benchmarks_folder + "/streamcluster/streamcluster"
    test = {
        Size.test: [2, 5, 1, 10, 10, 5, 'none', 'test.txt'],
        Size.simdev: [3, 10, 3, 16, 16, 10, 'none', 'simdev.txt'],
        Size.simsmall: [10, 20, 32, 4096, 4096, 1000, 'none', 'simsmall.txt'],
        Size.simmedium: [10, 20, 64, 8192, 8192, 1000, 'none', 'simmedium.txt'],
        Size.simlarge: [10, 20, 128, 16384, 16384, 1000, 'none', 'simlarge.txt'],
        Size.native: [10, 20, 128, 1000000, 200000, 5000, 'none', 'native.txt']
    }
    parameters = test.get(size, "size debe ser un elemento del enum Size")
    if isinstance(parameters, list):
        parameters[7] = benchmarks_folder + "/streamcluster/outputs/output_" + parameters[7]
    return [binary] + parameters + [threads]


def benchmark_selector(benchmark, size, benchmarks_folder, threads):
    suite = {
        Benchmark.bzip2: bzip2(benchmarks_folder),
        Benchmark.mcf: mcf(benchmarks_folder),
        Benchmark.hmmer: hmmer(benchmarks_folder),
        Benchmark.sjeng: sjeng(benchmarks_folder),
        Benchmark.lbm: lbm(benchmarks_folder),
        Benchmark.blackscholes: blackscholes(size, benchmarks_folder, threads),
        Benchmark.canneal: canneal(size, benchmarks_folder, threads),
        Benchmark.streamcluster: streamcluster(size, benchmarks_folder, threads)
    }
    parameters = suite.get(benchmark, "benchmark debe ser algun elemento del enum Benchmark")
    return parameters


def test():
    path = '/mnt/a/gem5-analysis-with-parsec'
    print(benchmark_selector(Benchmark.blackscholes, Size.test, path))
    print(benchmark_selector(Benchmark.canneal, Size.native, path))


if __name__ == "__main__":
    test()
