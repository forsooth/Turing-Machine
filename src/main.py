import argparse
import tm
import colors
import signal

print(colors.default, end='')

def catch_ctrl_c(signal, frame):
    print("Keyboard interrupt caught. Exiting.")
    exit(130)

signal.signal(signal.SIGINT, catch_ctrl_c)

parser = argparse.ArgumentParser(description="COMP-170 Turing Machine Interpreter.", add_help=False)

# Setting up command line flags and options. 
parser.add_argument('-m', '--machine', type=str, help="Required argument, followed by the path to the file specifying the machine.")
parser.add_argument('-t', '--tape', type=str, help="Optional argument, followed by the path to the file specifying the tape. If this option is not present, tape is instead read from stdin.")
parser.add_argument('-d', '--debug', type=int, default=0, help="Debugging level. Takes an integer, default is 0 (no debugging). Maxmimum is 2.")
parser.add_argument('-w', '--time', type=float, default=0.0, help="Time to wait between animation frames. Default is 0, meaning no animation.")
parser.add_argument('-l', '--haltafter', type=int, default=0.0, help="Number of steps to run the computation before halting.")
parser.add_argument('-s', '--haltat', type=str, help="State at which to halt the machine.")
parser.add_argument('-i', '--step', action="store_true", help="Run animation mode, but wait for input between each frame.")
parser.add_argument('-a', '--ascii', action="store_true", help="Strictly enforce the 170 standard that only ASCII characters are allowed in alphabets and states.")
parser.add_argument('-n', '--dark', action="store_true", help="Prints output in a 'dark mode', with black text. Default is light gray.")
parser.add_argument('-h', '--help', action="store_true", help="Shows this help message and exit.")

try:
    args = parser.parse_args()
except SystemExit:
    print("Invalid arguments given to program.")
    exit(9)

if args.help:
    parser.print_help()
    exit(3)

machine_file = args.machine

if args.dark:
    colors.default = colors.black_16
    colors.state_text = colors.dark_blue_16
    colors.changed_bit = colors.dark_dark_green
    colors.tape_box_2 = colors.dark_blue_16
    colors.tape_head_2 = colors.dark_red_16
    colors.tape_box_1 = colors.dark_red_16
    colors.tape_1 = colors.grey
    colors.accept = colors.dark_dark_green
    colors.reject = colors.dark_red_16
    colors.abort = colors.dark_red_16
    colors.hlighted = colors.dark_red_16
    colors.selected = colors.dark_dark_green

print(colors.default, end='')

debug = args.debug
if debug < 0 or debug > 2:
    debug = 0

tflag = args.time
if tflag < 0:
    tflag = 0

haltafter = args.haltafter
if haltafter < 0:
    haltafter = 0

haltat = args.haltat

# Initialize turing machine structure. Q, Σ, and Γ are Python lists. δ is
# a dictionary indexed by the string "state current_bit", i.e. the name of
# the state, a single space, and the current bit the tape head is reading.
B = 'B'
tape = ""
name = ""
Q = []
Σ = []
Γ = []
q_0 = ""
q_a = ""
q_r = ""
δ = {}

# Keep track of which of the keywords (GAMMA, SIGMA, etc.) we have encountered 
encountered = []

# Open the machine file. We have not yet begun reading in the delta states,
# so we wish to keep track of that.
if args.machine is None:
    print(colors.default + "No Turing machine file specified (-m option). Exiting.")
    exit(10)
try:
    f = open(args.machine, 'r')
except FileNotFoundError:
    print(colors.default + "Machine file at {} not found. Exiting.".format(args.machine))
    exit(11)

isdelta = False
for line in f:
    # Remove newlines so we don't confuse our Turing machine.
    line = line.replace('\n', '')
    # Ignore comments and die when 'END' is found.
    if line.startswith(';') or line == "":
        continue
    if line.startswith("END"):
        break
    # If we are reading lines in delta, split the line on whitespace. If we have five elements,
    # assume they are formatted correctly and put them into delta.
    elif isdelta:
        splitline = line.split()
        if len(splitline) == 5:
            state = splitline[0]
            if state not in Q:
                print("State '{}' read in DELTA not found in Q.".format(state))
                exit(12)
            curbit = splitline[1]
            nextstate = splitline[2]
            writebit = splitline[3]
            direction = splitline[4]
            δ[state + ' ' + curbit] = (nextstate, writebit, direction)
        elif len(splitline) == 3 or len(splitline) == 4:
            state = splitline[0]
            curbit = splitline[1]
            nextstate = splitline[2]
            if nextstate != q_a and nextstate != q_r:
                print("In the following line of DELTA:")
                print(splitline[0] + ' ' + splitline[1] + ' ' + splitline[2])
                print("state with a destination that was not the accept ({}) or reject ({}) state gave no symbol to write or direction to move. Exiting.".format(q_a, q_r))
                exit(13)
            # When we don't have a supplied write bit or direction, just use B and L,
            # for the sake of having a consistent tuple.
            else:
                δ[state + ' ' + curbit] = (nextstate, B, 'L')
        else:
            continue
    elif line.startswith("NAME"):
        name = line.replace("NAME:", "").strip()
        encountered.append("NAME:")

    elif line.startswith("STATE:"):
        s = line.replace("STATE:", "")
        encountered.append("STATE:")
        Q = s.split()
        for state in Q:
            for char in state:
                if args.ascii and ord(char) >= 128:
                    print("State '{}' read in DELTA contains non-ASCII character.".format(state))
                    exit(23)

    elif line.startswith("SIGMA:"):
        s = line.replace("SIGMA:", "")
        encountered.append("SIGMA:")
        Σ = s.split()
        for sym in Σ:
            for char in sym:
                if args.ascii and ord(char) >= 128:
                    print("Symbol '{}' read in SIGMA contains non-ASCII character.".format(sym))
                    exit(24)


    elif line.startswith("GAMMA:"):
        s = line.replace("GAMMA:", "")
        encountered.append("GAMMA:")
        Γ = s.split()
        for sym in Γ:
            for char in sym:
                if args.ascii and ord(char) >= 128:
                    print("Symbol '{}' read in GAMMA contains non-ASCII character.".format(sym))
                    exit(25)

    elif line.startswith("START:"):
        q_0 = line.replace("START:", "").strip()
        encountered.append("START:")

    elif line.startswith("ACCEPT:"):
        q_a = line.replace("ACCEPT:", "").strip()
        encountered.append("ACCEPT:")

    elif line.startswith("REJECT:"):
        q_r = line.replace("REJECT:", "").strip()
        encountered.append("REJECT:")

    elif line.startswith("DELTA:"):
        encountered.append("DELTA:")
        if not "NAME:" in encountered:
            print("Field 'NAME:' not found in Turing machine. Exiting.")
            exit(14)
        if not "STATE:" in encountered:
            print("Field 'STATE:' not found in Turing machine. Exiting.")
            exit(15)    
        if not "SIGMA:" in encountered:
            print("Field 'SIGMA:' not found in Turing machine. Exiting.")
            exit(16)    
        if not "GAMMA:" in encountered:
            print("Field 'GAMMA:' not found in Turing machine. Exiting.")
            exit(17)    
        if not "START:" in encountered:
            print("Field 'START:' not found in Turing machine. Exiting.")
            exit(18)    
        if not "ACCEPT:" in encountered:
            print("Field 'ACCEPT:' not found in Turing machine. Exiting.")
            exit(19)    
        if not "REJECT:" in encountered:
            print("Field 'REJECT:' not found in Turing machine. Exiting.")
            exit(20)        
        isdelta = True
f.close()

# If we specify a file name for the tape, read from that file. Otherwise
# read from stdin.
if args.tape is not None:
    tape_file = args.tape
    try:
        tf = open(tape_file, 'r')
        tape = tf.read()
        tf.close()
        tape = tape.replace('\n', '')
    except FileNotFoundError:
        print(colors.default + "Tape file at {} not found. Exiting.".format(tape_file))
        exit(21)
else:
    tape = input(colors.default + "Input: ")
    tape = ''.join(tape.split())

if haltat not in Q and haltat != None:
    print("State to halt at '{}' not found in Q.".format(haltat))
    exit(22)

# Create our turing machine, add our tape to it, and run the tape.
machine = tm.TM(debug, tflag, haltafter, haltat, args.step, name, B, Q, Σ, Γ, q_0, q_a, q_r, δ)
machine.add_tape(tape)
out = machine.run_tape()
print(out)
exit(machine.get_last_exit())