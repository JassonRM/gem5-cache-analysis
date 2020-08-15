from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import re
import threading
import time
from GUI_Results import init_interface

# Variables globales
BenchList = ['bzip2', 'mcf', 'hmmer', 'sjeng', 'lbm', 'blackscholes', 'canneal', 'streamcluster']
ReplacementList = ["LRURP", "FIFORP", "SecondChanceRP", "LFURP", "BIPRP", "LIPRP", "MRURP",
                   "RandomRP", "BRRIPRP", "RRIPRP", "NRURP", "TreePLRURP", "WeightedLRURP"]
PrefetcherList = ["NULL", "MultiPrefetcher", "QueuedPrefetcher", "StridePrefetcher", "TaggedPrefethcer",
                  "IndirectMemoryPrefetcher", "SignaturePathPrefetcher", "SignaturePathPrefetcherV2", "AMPMPrefetcher",
                  "DCPTPrefetcher", "IrregularStreamBufferPrefetcher", "SlimAMPMPrefetcher", "BOPPrefetcher",
                  "SBOOEprefetcher", "STeMSPrefetcher", "PIFPrefetcher"]
BranchList = ["NULL", "LocalBP", "BiModeBP", "TournamentBP"]
# -------------Configuraciones generales--------------------
CLK = "1GHz"
MEM_RANGE = "512MB"
BENCH_PATH = "/home/marco/Documents/Projects/gem5-analysis-with-parsec/benchmarks"
GEM_PATH = "/home/marco/Documents/Projects/gem5"
PY_PATH = "/home/marco/Documents/Projects/gem5-analysis-with-parsec/processor.py"
BENCHMARK = "bzip2"
BENCH_SIZE = "simsmall"
THREADS = "1"
PROCESSORS = "6"
INSTRUCTIONS = "10000000"
# ----------------------------------------------------------
# -------------Configuraciones Caches-----------------------
L1_INST_SIZE = "16kB"
L1_DAT_SIZE = "64kB"
L1_ASSOC = "2"
L1_TAG_LAT = "2"
L1_DAT_LAT = "2"
L1_RESP_LAT = "2"
L1_REPL_POL = "LRURP"
L1_PREFETCH = "NULL"
# ----------------------------------------------------------
L2_SIZE = "256kB"
L2_ASSOC = "8"
L2_TAG_LAT = "20"
L2_DAT_LAT = "20"
L2_RESP_LAT = "20"
L2_REPL_POL = "LRURP"
L2_PREFETCH = "NULL"

# ----------------------------------------------------------
BRANCH_PREDICTOR = "NULL"
BTB_ENTRIES = "4096"
LOCAL_PREDICTOR_SIZE = "1024"
GLOBAL_PREDICTOR_SIZE = "8192"
CHOICE_PREDICTOR_SIZE = "8192"


# ----------------------------------------------------------

def consultaPathBENCH():
    global BENCH_PATH
    try:
        # root.filename = filedialog.askopenfilename(initialdir="/home", title="Seleccione el Benchmark",filetypes=(("txt", "*txt"),("all files", "*.*")))
        root.filename = filedialog.askdirectory(initialdir="/home", title="Seleccione la carpeta del Benchmark")
    except:
        messagebox.showwarning("Alto! No ha elegido una carpeta.")

    BENCH_PATH = str(root.filename)


def consultaPathGEM():
    global GEM_PATH
    try:
        # root.filename = filedialog.askopenfilename(initialdir="/home", title="Seleccione gem5",filetypes=(("txt", "*txt"), ("all files", "*.*")))
        root.filename = filedialog.askdirectory(initialdir="/home",
                                                title="Seleccione la carpeta de instalacion de Gem5")
    except:
        messagebox.showwarning("Alto! No ha elegido una carpeta.")
    GEM_PATH = str(root.filename)


def consultaPy():
    global PY_PATH
    try:
        root.filename = filedialog.askopenfilename(initialdir="/home", title="Seleccione el .py",
                                                   filetypes=(("py", "*py"), ("txt", "*txt"), ("all files", "*.*")))
    except:
        messagebox.showwarning("Alto! No ha elegido un un archivo.")
    PY_PATH = str(root.filename)


def setConfigGenerales(clock, mem_range, benchOption, bench_size, threads, processors, instructions):
    global CLK, MEM_RANGE, BENCHMARK, BENCH_SIZE, THREADS, PROCESSORS, INSTRUCTIONS
    CLK = clock
    MEM_RANGE = mem_range
    BENCHMARK = benchOption

    # if (benchOption == "bzip2"):
    #     BENCHMARK = "1"
    # elif (benchOption == "mcf"):
    #     BENCHMARK = "2"
    # elif (benchOption == "hmmer"):
    #     BENCHMARK = "3"
    # elif (benchOption == "sjeng"):
    #     BENCHMARK = "4"
    # elif (benchOption == "lbm"):
    #     BENCHMARK = "5"
    # elif (benchOption == "blackscholes"):
    #     BENCHMARK = "6"
    # elif (benchOption == "canneal"):
    #     BENCHMARK = "7"
    # else:
    #     BENCHMARK = "8"

    BENCH_SIZE = bench_size
    THREADS = threads
    PROCESSORS = processors
    INSTRUCTIONS = instructions

    print("CLK " + CLK)
    print("MEM_RANGE " + MEM_RANGE)
    print("BENCH_PATH " + BENCH_PATH)
    print("GEM_PATH " + GEM_PATH)
    print("PY_PATH " + PY_PATH)
    print("BENCHMARK " + BENCHMARK)
    print("BENCH_SIZE " + BENCH_SIZE)
    print("THREADS " + THREADS)
    print("PROCESSORS " + PROCESSORS)
    print("INSTRUCTIONS " + INSTRUCTIONS)
    table()
    ventanaConfig.destroy()


ventanaConfig = None


def ventanaConfiguracionesGenrales():
    global ventanaConfig
    ventanaConfig = Toplevel(root)
    ventanaConfig.title("Configuraciones del Sistema")
    ventanaConfig.geometry("400x480")
    etiquetaExplicativa = Label(ventanaConfig, text="Ingrese las configuraciones generales del sistema:").place(x=10,
                                                                                                                y=10)
    try:
        clock = StringVar(ventanaConfig, value=CLK)
        CLOCKEtiqueta = Label(ventanaConfig, text="Frecuencia del clock: ").place(x=10, y=40)
        CLOCKCaja = Entry(ventanaConfig, textvariable=clock).place(x=185, y=40)

        mem_range = StringVar(ventanaConfig, value=MEM_RANGE)
        MEMetiqueta = Label(ventanaConfig, text="Rango de memoria:").place(x=10, y=80)
        MEMcaja = Entry(ventanaConfig, textvariable=mem_range).place(x=185, y=80)

        BENCHetiquta = Label(ventanaConfig, text="Ruta de los Benchmark:").place(x=10, y=120)
        botonBenchPath = Button(ventanaConfig, text="Abrir Benchmark", command=lambda: consultaPathBENCH()).place(x=185,
                                                                                                                  y=120)

        GEMetiqueta = Label(ventanaConfig, text="Ruta de Instalacion GEM:").place(x=10, y=160)
        botonGEMPath = Button(ventanaConfig, text="Abrir GEM", command=lambda: consultaPathGEM()).place(x=185, y=160)

        PuntoPy = Label(ventanaConfig, text="Ruta .py a ejecutar:").place(x=10, y=200)
        botonPyPath = Button(ventanaConfig, text="Abrir .py", command=lambda: consultaPy()).place(x=185, y=200)

        BENCHetiqueta = Label(ventanaConfig, text="Tipo de Benchmark:").place(x=10, y=240)
        var = StringVar(ventanaConfig)
        var.set(BenchList[0])
        BENCHoption = OptionMenu(ventanaConfig, var, *BenchList).place(x=185, y=240)

        bench_size = StringVar(ventanaConfig, value=BENCH_SIZE)
        SIZEetiqueta = Label(ventanaConfig, text="Tamano del Benchmark:").place(x=10, y=280)
        SIZEcaja = Entry(ventanaConfig, textvariable=bench_size).place(x=185, y=280)

        threads = StringVar(ventanaConfig, value=THREADS)
        THREADSetiqueta = Label(ventanaConfig, text="Cantidad de hilos:").place(x=10, y=320)
        THREADScaja = Entry(ventanaConfig, textvariable=threads).place(x=185, y=320)

        processors = StringVar(ventanaConfig, value=PROCESSORS)
        PROCESSORSetiqueta = Label(ventanaConfig, text="Cantidad de procesadores:").place(x=10, y=360)
        PROCESSORScaja = Entry(ventanaConfig, textvariable=processors).place(x=185, y=360)

        instructions = StringVar(ventanaConfig, value=INSTRUCTIONS)
        INSTRetiqueta = Label(ventanaConfig, text="Cantidad de instrucciones:").place(x=10, y=400)
        INSTRcaja = Entry(ventanaConfig, textvariable=instructions).place(x=185, y=400)


    except ValueError:
        messagebox.showwarning("Cuidado", "No puede dejar valores en blanco")

    botonObtieneRuta = Button(ventanaConfig, text="Guardar",
                              command=lambda: setConfigGenerales(clock.get(), mem_range.get(), var.get(),
                                                                 bench_size.get(), threads.get(),
                                                                 processors.get(), instructions.get())).place(x=10,
                                                                                                              y=440)


def setConfigurarcionL1(l1_inst_size, l1_dat_size, l1_assoc, l1_tag_latency, l1_data_latency, l1_resp_lat, l1_repl_pol,
                        l1_prefetch):
    global L1_INST_SIZE, L1_DAT_SIZE, L1_ASSOC, L1_TAG_LAT, L1_DAT_LAT, L1_RESP_LAT, L1_REPL_POL, L1_PREFETCH
    L1_INST_SIZE = l1_inst_size
    L1_DAT_SIZE = l1_dat_size
    L1_ASSOC = l1_assoc
    L1_TAG_LAT = l1_tag_latency
    L1_DAT_LAT = l1_data_latency
    L1_RESP_LAT = l1_resp_lat
    L1_REPL_POL = l1_repl_pol
    L1_PREFETCH = l1_prefetch

    print("L1_INST_SIZE " + L1_INST_SIZE)
    print("L1_DAT_SIZE " + L1_DAT_SIZE)
    print("L1_ASSOC " + L1_ASSOC)
    print("L1_TAG_LAT " + L1_TAG_LAT)
    print("L1_DAT_LAT " + L1_DAT_LAT)
    print("L1_RESP_LAT " + L1_RESP_LAT)
    print("L1_REPL_POL " + L1_REPL_POL)
    print("L1_PREFETCH " + L1_PREFETCH)
    table()
    ventanaCacheL1.destroy()


ventanaCacheL1 = None


def configuracionCacheL1():
    global ventanaCacheL1
    ventanaCacheL1 = Toplevel(root)
    ventanaCacheL1.title("Configuraciones de la Cahce L1(Datos e Instrucciones)")
    ventanaCacheL1.geometry("400x400")
    etiquetaExplicativa = Label(ventanaCacheL1, text="Ingrese las configuraciones de la Cache L1:").place(x=10, y=10)

    try:

        l1_inst_size = StringVar(ventanaCacheL1, value=L1_INST_SIZE)
        SIZEIetiqueta = Label(ventanaCacheL1, text="Tamano cache instr:").place(x=10, y=40)
        SIZEICaja = Entry(ventanaCacheL1, textvariable=l1_inst_size).place(x=185, y=40)

        l1_dat_size = StringVar(ventanaCacheL1, value=L1_DAT_SIZE)
        SIZEDetiqueta = Label(ventanaCacheL1, text="Tamano cache datos:").place(x=10, y=80)
        SIZEDcaja = Entry(ventanaCacheL1, textvariable=l1_dat_size).place(x=185, y=80)

        l1_assoc = StringVar(ventanaCacheL1, value=L1_ASSOC)
        ASSOCetiqueta = Label(ventanaCacheL1, text="Associatividad:").place(x=10, y=120)
        ASSOCcaja = Entry(ventanaCacheL1, textvariable=l1_assoc).place(x=185, y=120)

        l1_tag_latency = StringVar(ventanaCacheL1, value=L1_TAG_LAT)
        TAGetiqueta = Label(ventanaCacheL1, text="Latencia de la etiqueta:").place(x=10, y=160)
        TAGcaja = Entry(ventanaCacheL1, textvariable=l1_tag_latency).place(x=185, y=160)

        l1_data_latency = StringVar(ventanaCacheL1, value=L1_DAT_LAT)
        DATAetiqueta = Label(ventanaCacheL1, text="Latencia de los datos:").place(x=10, y=200)
        DATAcaja = Entry(ventanaCacheL1, textvariable=l1_data_latency).place(x=185, y=200)

        l1_resp_lat = StringVar(ventanaCacheL1, value=L1_RESP_LAT)
        RESPetiqueta = Label(ventanaCacheL1, text="Latencia de respuesta:").place(x=10, y=240)
        RESPcaja = Entry(ventanaCacheL1, textvariable=l1_resp_lat).place(x=185, y=240)

        REPLetiqueta = Label(ventanaCacheL1, text="Politica de reemplazo:").place(x=10, y=280)
        var = StringVar(ventanaCacheL1)
        var.set(ReplacementList[0])
        REPLACEMENToption = OptionMenu(ventanaCacheL1, var, *ReplacementList).place(x=185, y=280)

        PREFETCHetiqueta = Label(ventanaCacheL1, text="Prefetcher:").place(x=10, y=320)
        var1 = StringVar(ventanaCacheL1)
        var1.set(PrefetcherList[0])
        PREFETCHoption = OptionMenu(ventanaCacheL1, var1, *PrefetcherList).place(x=185, y=320)

    except ValueError:
        messagebox.showwarning("Cuidado", "No puede dejar valores en blanco")
    botonGuardar = Button(ventanaCacheL1, text="Confirmar",
                          command=lambda: setConfigurarcionL1(l1_inst_size.get(), l1_dat_size.get(), l1_assoc.get(),
                                                              l1_tag_latency.get(), l1_data_latency.get(),
                                                              l1_resp_lat.get(), var.get(), var1.get())).place(x=10,
                                                                                                               y=360)


def setConfigurarcionL2(l2_size, l2_assoc, l2_tag_latency, l2_data_latency, l2_resp_lat, l2_repl_pol, l2_prefetch):
    global L2_SIZE, L2_ASSOC, L2_TAG_LAT, L2_DAT_LAT, L2_RESP_LAT, L2_REPL_POL, L2_PREFETCH
    L2_SIZE = l2_size
    L2_ASSOC = l2_assoc
    L2_TAG_LAT = l2_tag_latency
    L2_DAT_LAT = l2_data_latency
    L2_RESP_LAT = l2_resp_lat
    L2_REPL_POL = l2_repl_pol
    L2_PREFETCH = l2_prefetch

    print("L2_SIZE " + L2_SIZE)

    print("L2_ASSOC " + L2_ASSOC)
    print("L2_TAG_LAT " + L2_TAG_LAT)
    print("L2_DAT_LAT " + L2_DAT_LAT)
    print("L2_RESP_LAT " + L2_RESP_LAT)
    print("L2_REPL_POL " + L2_REPL_POL)
    print("L2_PREFETCH " + L2_PREFETCH)
    table()
    ventanaCacheL2.destroy()

    ventanaCacheL2 = None


def configuracionCacheL2():
    global ventanaCacheL2
    ventanaCacheL2 = Toplevel(root)
    ventanaCacheL2.title("Configuraciones de la Cahce L2")
    ventanaCacheL2.geometry("400x400")
    etiquetaExplicativa = Label(ventanaCacheL2, text="Ingrese las configuraciones de la Cache L2:").place(x=10, y=10)

    try:
        l2_size = StringVar(ventanaCacheL2, value=L2_SIZE)
        SIZEetiqueta = Label(ventanaCacheL2, text="Tamano de la cache:").place(x=10, y=40)
        SIZECaja = Entry(ventanaCacheL2, textvariable=l2_size).place(x=185, y=40)

        l2_assoc = StringVar(ventanaCacheL2, value=L2_ASSOC)
        ASSOCetiqueta = Label(ventanaCacheL2, text="Associatividad:").place(x=10, y=80)
        ASSOCcaja = Entry(ventanaCacheL2, textvariable=l2_assoc).place(x=185, y=80)

        l2_tag_latency = StringVar(ventanaCacheL2, value=L2_TAG_LAT)
        TAGetiqueta = Label(ventanaCacheL2, text="Latencia de la etiqueta:").place(x=10, y=120)
        TAGcaja = Entry(ventanaCacheL2, textvariable=l2_tag_latency).place(x=185, y=120)

        l2_data_latency = StringVar(ventanaCacheL2, value=L2_DAT_LAT)
        DATAetiqueta = Label(ventanaCacheL2, text="Latencia de los datos:").place(x=10, y=160)
        DATAcaja = Entry(ventanaCacheL2, textvariable=l2_data_latency).place(x=185, y=160)

        l2_resp_lat = StringVar(ventanaCacheL2, value=L2_RESP_LAT)
        RESPetiqueta = Label(ventanaCacheL2, text="Latencia de respuesta:").place(x=10, y=200)
        RESPcaja = Entry(ventanaCacheL2, textvariable=l2_resp_lat).place(x=185, y=200)

        REPLetiqueta = Label(ventanaCacheL2, text="Politica de reemplazo:").place(x=10, y=240)
        var = StringVar(ventanaCacheL2)
        var.set(ReplacementList[0])
        REPLACEMENToption = OptionMenu(ventanaCacheL2, var, *ReplacementList).place(x=185, y=240)

        PREFETCHetiqueta = Label(ventanaCacheL2, text="Prefetcher:").place(x=10, y=280)
        var1 = StringVar(ventanaCacheL2)
        var1.set(PrefetcherList[0])
        PREFETCHoption = OptionMenu(ventanaCacheL2, var1, *PrefetcherList).place(x=185, y=280)

    except ValueError:
        messagebox.showwarning("Cuidado", "No puede dejar valores en blanco")
    botonGuardar = Button(ventanaCacheL2, text="Confirmar",
                          command=lambda: setConfigurarcionL2(l2_size.get(), l2_assoc.get(), l2_tag_latency.get(),
                                                              l2_data_latency.get(), l2_resp_lat.get(), var.get(),
                                                              var1.get())).place(x=10, y=320)


def setBranchPredictor(tipo, btbentries, localPsize, globalPsize, choicePsize):
    global BRANCH_PREDICTOR, BTB_ENTRIES, LOCAL_PREDICTOR_SIZE, GLOBAL_PREDICTOR_SIZE, CHOICE_PREDICTOR_SIZE

    BRANCH_PREDICTOR = tipo
    BTB_ENTRIES = btbentries
    LOCAL_PREDICTOR_SIZE = localPsize
    GLOBAL_PREDICTOR_SIZE = globalPsize
    CHOICE_PREDICTOR_SIZE = choicePsize

    editCPU()
    table()
    ventanBranchpredictor.destroy()


ventanBranchpredictor = None


def branchPredictor():
    global ventanBranchpredictor
    ventanBranchpredictor = Toplevel(root)
    ventanBranchpredictor.title("Configuraciones del Branch Predictor")
    ventanBranchpredictor.geometry("400x280")
    Branch = Label(ventanBranchpredictor, text="Ingrese la configuracion del Branch Predictor").place(x=10, y=10)

    try:

        BRANCHetiqueta = Label(ventanBranchpredictor, text="Tipo de branch predictor:").place(x=10, y=40)
        var = StringVar(ventanBranchpredictor)
        var.set(BranchList[0])
        BRANCHoption = OptionMenu(ventanBranchpredictor, var, *BranchList).place(x=200, y=40)

        btbentries = StringVar(ventanBranchpredictor, value=BTB_ENTRIES)
        BTBentryetiqueta = Label(ventanBranchpredictor, text="Numero de BTBentries:").place(x=10, y=80)
        BTBcaja = Entry(ventanBranchpredictor, textvariable=btbentries).place(x=200, y=80)

        localPsize = StringVar(ventanBranchpredictor, value=LOCAL_PREDICTOR_SIZE)
        LOCALetiqueta = Label(ventanBranchpredictor, text="Tamano de Local Predictor:").place(x=10, y=120)
        LOCALcaja = Entry(ventanBranchpredictor, text=localPsize).place(x=200, y=120)

        globalPsize = StringVar(ventanBranchpredictor, value=GLOBAL_PREDICTOR_SIZE)
        GLOBALetiqueta = Label(ventanBranchpredictor, text="Tamano de Global Predictor:").place(x=10, y=160)
        GLOBALcaja = Entry(ventanBranchpredictor, text=globalPsize).place(x=200, y=160)

        choicePsize = StringVar(ventanBranchpredictor, value=CHOICE_PREDICTOR_SIZE)
        CHOICEetiqueta = Label(ventanBranchpredictor, text="Tamano de Choice Predictor:").place(x=10, y=200)
        CHOICEcaja = Entry(ventanBranchpredictor, text=choicePsize).place(x=200, y=200)
    except ValueError:
        messagebox.showwarning("Cuidado", "No puede dejar valores en blanco")

    botonBranch = Button(ventanBranchpredictor, text="Confirmar",
                         command=lambda: setBranchPredictor(var.get(), btbentries.get(), localPsize.get(),
                                                            globalPsize.get(), choicePsize.get())).place(x=10, y=240)


def simular():
    editCaches()
    print("------------------------------Parametros de configuracion---------------------------------------")
    print("CLK " + CLK)
    print("MEM_RANGE " + MEM_RANGE)
    print("BENCH_PATH " + BENCH_PATH)
    print("GEM_PATH " + GEM_PATH)
    print("PY_PATH " + PY_PATH)
    print("BENCHMARK " + BENCHMARK)
    print("BENCH_SIZE " + BENCH_SIZE)
    print("THREADS " + THREADS)
    print("PROCESSORS " + PROCESSORS)
    print("L1_SIZE " + L1_INST_SIZE)
    print("L1_SIZE " + L1_DAT_SIZE)
    print("L1_ASSOC " + L1_ASSOC)
    print("L1_TAG_LAT " + L1_TAG_LAT)
    print("L1_DAT_LAT " + L1_DAT_LAT)
    print("L1_RESP_LAT " + L1_RESP_LAT)
    print("L1_REPL_POL " + L1_REPL_POL)
    print("L1_PREFETCH " + L1_PREFETCH)
    print("L2_SIZE " + L2_SIZE)
    print("L2_ASSOC " + L2_ASSOC)
    print("L2_TAG_LAT " + L2_TAG_LAT)
    print("L2_DAT_LAT " + L2_DAT_LAT)
    print("L2_RESP_LAT " + L2_RESP_LAT)
    print("L2_REPL_POL " + L2_REPL_POL)
    print("L2_PREFETCH " + L2_PREFETCH)

    print(PY_PATH)
    print(GEM_PATH)
    print(BENCH_PATH)

    print(INSTRUCTIONS)
    comando = GEM_PATH + "/build/X86/gem5.opt " + PY_PATH + " -I " + INSTRUCTIONS + " -clk=" + CLK + " -mem_range=" + MEM_RANGE + " -bench_path=" + BENCH_PATH + " -benchmark=" + BENCHMARK + " -bench_size=" + BENCH_SIZE + " -threads=" + THREADS + " -l1_inst_size=" + L1_INST_SIZE + " -l1_dat_size=" + L1_DAT_SIZE + " -l1_assoc=" + L1_ASSOC + " -l1_tag_lat=" + L1_TAG_LAT + " -l1_dat_lat=" + L1_DAT_LAT + " -l1_resp_lat=" + L1_RESP_LAT + " -l2_size=" + L2_SIZE + " -l2_assoc=" + L2_ASSOC + " -l2_tag_lat=" + L2_TAG_LAT + " -l2_dat_lat=" + L2_DAT_LAT + " -l2_resp_lat=" + L2_RESP_LAT
    os.system(comando)


def table():
    Label(root, borderwidth=2, relief='ridge').place(x=3, y=175, width=693, height=500)
    Label(root, text="CLK:", anchor="w", width=18).place(x=10, y=190)
    Label(root, text="MEM_RANGE:", anchor="w", width=18).place(x=10, y=210)
    Label(root, text="BENCH_PATH:", anchor="w", width=18).place(x=10, y=230)
    Label(root, text="GEM_PATH:", anchor="w", width=18).place(x=10, y=250)
    Label(root, text="PY_PATH:", anchor="w", width=18).place(x=10, y=270)
    Label(root, text="BENCHMARK:", anchor="w", width=18).place(x=10, y=290)
    Label(root, text="BENCH_SIZE:", anchor="w", width=18).place(x=10, y=310)
    Label(root, text="THREADS:", anchor="w", width=18).place(x=10, y=330)
    Label(root, text="INSTRUCTIONS:", anchor="w", width=18).place(x=10, y=350)  # a partir de aca cambiar y
    Label(root, text="L1_INST_SIZE:", anchor="w", width=18).place(x=10, y=370)
    Label(root, text="L1_DAT_SIZE:", anchor="w", width=18).place(x=10, y=390)
    Label(root, text="L1_ASSOC:", anchor="w", width=18).place(x=10, y=410)
    Label(root, text="L1_TAG_LAT:", anchor="w", width=18).place(x=10, y=430)
    Label(root, text="L1_DAT_LAT:", anchor="w", width=18).place(x=10, y=450)
    Label(root, text="L1_REPL_POL:", anchor="w", width=18).place(x=10, y=470)
    Label(root, text="L1_PREFETCH:", anchor="w", width=18).place(x=10, y=490)
    Label(root, text="L2_SIZE:", anchor="w", width=18).place(x=10, y=510)
    Label(root, text="L2_ASSOC:", anchor="w", width=18).place(x=10, y=530)
    Label(root, text="L2_TAG_LAT:", anchor="w", width=18).place(x=10, y=550)
    Label(root, text="L2_DAT_LAT:", anchor="w", width=18).place(x=10, y=570)
    Label(root, text="L2_RESP_LAT:", anchor="w", width=18).place(x=10, y=590)
    Label(root, text="L2_REPL_POL:", anchor="w", width=18).place(x=10, y=610)
    Label(root, text="L2_PREFETCH:", anchor="w", width=18).place(x=10, y=630)
    Label(root, text="BRANCH_PREDICTOR:", anchor="w", width=18).place(x=10, y=650)

    Label(root, text=CLK).place(x=160, y=190)
    Label(root, text=MEM_RANGE).place(x=160, y=210)
    Label(root, text=BENCH_PATH).place(x=160, y=230)
    Label(root, text=GEM_PATH).place(x=160, y=250)
    Label(root, text=PY_PATH).place(x=160, y=270)
    Label(root, text=BENCHMARK).place(x=160, y=290)
    Label(root, text=BENCH_SIZE).place(x=160, y=310)
    Label(root, text=THREADS).place(x=160, y=330)
    Label(root, text=INSTRUCTIONS).place(x=160, y=350)  # a partir de aca cambiar y
    Label(root, text=L1_INST_SIZE).place(x=160, y=370)
    Label(root, text=L1_DAT_SIZE).place(x=160, y=390)
    Label(root, text=L1_ASSOC).place(x=160, y=410)
    Label(root, text=L1_TAG_LAT).place(x=160, y=430)
    Label(root, text=L1_DAT_LAT).place(x=160, y=450)
    Label(root, text=L1_REPL_POL).place(x=160, y=470)
    Label(root, text=L1_PREFETCH).place(x=160, y=490)
    Label(root, text=L2_SIZE).place(x=160, y=510)
    Label(root, text=L2_ASSOC).place(x=160, y=530)
    Label(root, text=L2_TAG_LAT).place(x=160, y=550)
    Label(root, text=L2_DAT_LAT).place(x=160, y=570)
    Label(root, text=L2_RESP_LAT).place(x=160, y=590)
    Label(root, text=L2_REPL_POL).place(x=160, y=610)
    Label(root, text=L2_PREFETCH).place(x=160, y=630)
    Label(root, text=BRANCH_PREDICTOR).place(x=160, y=650)


def editCaches():
    caches = open("../caches.py", "r+")
    data = caches.read()
    caches.close()
    open("../caches.py", "w").close()
    caches = open("../caches.py", "r+")
    data = re.sub("L1_REPLACEMENT_POLICY = .+\n", "L1_REPLACEMENT_POLICY = " + L1_REPL_POL + "()\n", data)
    if L1_PREFETCH == "NULL":
        data = re.sub("L1_PREFETCHER = .+\n", "L1_PREFETCHER = " + L1_PREFETCH + "\n", data)
    else:
        data = re.sub("L1_PREFETCHER = .+\n", "L1_PREFETCHER = " + L1_PREFETCH + "()\n", data)
    data = re.sub("L2_REPLACEMENT_POLICY = .+\n", "L2_REPLACEMENT_POLICY = " + L2_REPL_POL + "()\n", data)
    if L2_PREFETCH == "NULL":
        data = re.sub("L2_PREFETCHER = .+\n", "L2_PREFETCHER = " + L2_PREFETCH + "\n", data)
    else:
        data = re.sub("L2_PREFETCHER = .+\n", "L2_PREFETCHER = " + L2_PREFETCH + "()\n", data)
    caches.seek(0)
    caches.write(data)
    caches.close()


def editCPU():
    cpu = open(GEM_PATH + "/src/cpu/simple/BaseSimpleCPU.py", "r+")
    data = cpu.read()
    cpu.close()
    open(GEM_PATH + "/src/cpu/simple/BaseSimpleCPU.py", "w").close()
    cpu = open(GEM_PATH + "/src/cpu/simple/BaseSimpleCPU.py", "r+")
    if BRANCH_PREDICTOR != "NULL":
        data = re.sub("Param.BranchPredictor(.+, \"Branch Predictor\").*",
                      "Param.BranchPredictor(" + BRANCH_PREDICTOR + "(), \"Branch Predictor\")", data)
    else:
        data = re.sub("Param.BranchPredictor(.+, \"Branch Predictor\").*",
                      "Param.BranchPredictor(" + BRANCH_PREDICTOR + ", \"Branch Predictor\")", data)
    cpu.seek(0)
    cpu.write(data)
    cpu.close()

    cpu = open(GEM_PATH + "/src/cpu/pred/BranchPredictor.py", "r+")
    data = cpu.read()
    cpu.close()
    open(GEM_PATH + "/src/cpu/pred/BranchPredictor.py", "w").close()
    cpu = open(GEM_PATH + "/src/cpu/pred/BranchPredictor.py", "r+")

    data = re.sub("BTBEntries = .+\n", "BTBEntries = Param.Unsigned(" + BTB_ENTRIES + ", \"Number of BTB entries\")\n",
                  data)

    data = re.sub("localPredictorSize = .+\n",
                  "localPredictorSize = Param.Unsigned(" + LOCAL_PREDICTOR_SIZE + ", \"Size of local predictor)\")\n",
                  data)

    data = re.sub("globalPredictorSize = .+\n",
                  "globalPredictorSize = Param.Unsigned(" + GLOBAL_PREDICTOR_SIZE + ", \"Size of global predictor)\")\n",
                  data)

    data = re.sub("choicePredictorSize = .+\n",
                  "choicePredictorSize = Param.Unsigned(" + CHOICE_PREDICTOR_SIZE + ", \"Size of choice predictor)\")\n",
                  data)

    cpu.seek(0)
    cpu.write(data)
    cpu.close()
    cmd = "cd " + GEM_PATH + " && scons build/X86/gem5.opt -j " + PROCESSORS
    print(cmd)
    os.system(cmd)


def execute_result_interface():
    x = threading.Thread(target=init_interface, args=())
    x.start()


# Configuracion general para la ventana principal.
root = Tk()
root.title("Herramienta de configuracion para el Simulador gem5")
root.geometry("700x730")
root.resizable(False, False)
etiqueta = Label(root, borderwidth=2, relief='solid').place(x=-10, y=3, width=900, height=135)
etiquetaConfiguracionGeneral = Label(root, text="Configuraciones generales del sistema.").place(x=25, y=10)
botonConfiguracionGeneral = Button(root, text="Configuracion General", command=ventanaConfiguracionesGenrales).place(
    x=40, y=50, width=225)
botonBranchPredictor = Button(root, text="Configuracion BranchPredictor", command=branchPredictor).place(x=40, y=90,
                                                                                                         width=225)
etiquetaDecodificarImagen = Label(root, text="Configuraciones para las cache L1 y L2").place(x=400, y=10)
botonL1 = Button(root, text="Configuracion de Cache L1", command=configuracionCacheL1).place(x=430, y=50)
botonL2 = Button(root, text="Configuracion de Cache L2", command=configuracionCacheL2).place(x=430, y=90)
etiquetaMostrarInfo = Label(root, text="Informacion de la configuracion:").place(x=40, y=150)
botonMostrarInfo = Button(root, text="Actualizar", command=table).place(x=480, y=142
                                                                        )
botonRun = Button(root, text="Simular", command=simular).place(x=40, y=685)
botonresultados = Button(root, text="Resultados", command=execute_result_interface).place(x=530, y=685)

table()
root.mainloop()
