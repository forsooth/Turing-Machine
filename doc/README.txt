Matt Asnes
Turing Machine Interpreter & Debugger

===============================================================================
ABOUT
===============================================================================

This is an interpreter for the Turing machine syntax defined in a particular problem set given to me in class.

===============================================================================
REPRESENTATION
===============================================================================

The machine, internally is essentially the formally defined 7-tuple (with some
additional fluff for convenience). The tape is represented as a doubly-linked
list so that the internal representation is no more knowledgable about the 
state than the abstract turing machine it is representing and simulating. The
transition function is a dictionary mapping some state and bit to some new 
state, new bit, and direction. 

===============================================================================
USAGE
===============================================================================

This Turing machine interpreter runs in Python 3. The program can be 
executed in its most basic form as follows in its simplest variety:
        $> python3 main.py -m ../path/to/turing_machine

for class TAs, a suggested usage would be:
        $> python3 main.py -m ./machine -t ./tape -d 2 -i -a

or, if the terminal background is white / a light color:
        $> python3 main.py -m ./machine -t ./tape -d 2 -i -a -n

If the machine runs until it reaches its accept state, the exit code is 0. 
If it rejects, the exit code is 1. 
If it halts after running for a period and aborting, it exits 2.
If the help page is displayed (-h OR --help) it exits 3.
If CTRL+C (SIGINT) is sent, it safely exits Python with code 130.
In error cases, the program exits with a code higher than 2.

The command line options & flags are as follows:

-------------------------------------------------------------------------------
COMMAND LINE OPTIONS
-------------------------------------------------------------------------------

OPTION: -m OR --machine
HUMAN-READABLE NAME: machine
TYPE: STRING
REQUIREMENTS: must be a valid path
DESCRIPTION:
Required option, specifies the Turing machine file as specified
in the class course page and homework. File type does not matter. The
argument following this option should be the path to the file.

OPTION: -t OR --tape
HUMAN-READABLE NAME: tape
TYPE: STRING
REQUIREMENTS: must be a valid path
DESCRIPTION:
Optional, followed by the path to the file containing input. Input should be a
file which contains a series of characters specified in the input alphabet of
the machine file. Whitespace characters are ignored, as only non-whitespace
characters are valid input symbols. As such, the file need not end in a
newline. If no file is specified (i.e. the --t option is not present) input
is instead read from stdin.

OPTION: -d OR --debug
HUMAN-READABLE NAME: debug level
TYPE: INTEGER
REQUIREMENTS: must be 0, 1, or 2
DESCRIPTION: 
Sets the debug level of the program. Valid levels are 0, 1, and 2. Negative
integers and integers greater than 2 will default to debug level 0. Fractional
debug levels will return an error. The descriptions of debug levels are
as follows:
    Level 0:
        Prints only the word 'Accept' or 'Reject', and
        the word "Input:", depending on whether input
        was provided on the command line or through stdin.
    Level 1:
        Prints a single-line representation of the Turing
        machine tape at every stage, but no information on
        state is provided.
    Level 2:
        Prints a full ASCII description of the Turing 
        machine, including state and tape information.

OPTION: -w OR --time
HUMAN-READABLE NAME: time to wait between frames
TYPE: FLOAT
REQUIREMENTS: must be > 0
DESCRIPTION:
For debug levels 1 and 2, rather than printing every step of the Turing machine
computation at once, an animation mode is supported. If the --time option is
present and followed by a floating point number strictly greater than zero,
that number of seconds will be slept before the next frame of output is
provided. Previous framesare overwritten such that at the end of output,
nothing is present except for the accept or reject stamp. A value
of 0 (default) turns off animation entirely.

OPTION: -l OR --haltafter
HUMAN-READABLE NAME: number of steps after which the Turing machine should halt
TYPE: INTEGER
REQUIREMENTS: must be >= 0
DESCRIPTION:
Number of steps to execute the machine for before computation is stopped and
an "Abort" keyword is returned. This is useful if a non-halting Turing machine
needs to be simulated.

FLAG: -s OR --haltat
HUMAN-READABLE NAME: state which, once reached, causes the machine to halt
DESCRIPTION:
Specifies the state which, if reached, the machine halts before computing.
If the specified state is the accept or reject state, the machine will 
accept or reject respectively instead of aborting.

FLAG: -i OR --step
HUMAN-READABLE NAME: interactive mode to step through animation
DESCRIPTION:
Specifies that rather than running in animation mode with a fixed time to
pause each frame before continuing, the program waits for user input
between each frame. If any key is pressed it will execute the next state.
If both -i and -w are present, the machine waits the set frame pause time,
and then waits for user input.

FLAG: -a OR --ascii
HUMAN-READABLE NAME: disallow non-ASCII characters. 
DESCRIPTION:
Turns on checking for non-ASCII characters. If any character in a state name,
or in SIGMA or DELTA is outside of the ASCII range, the program terminates
with an error.

FLAG: -n OR --dark
HUMAN-READABLE NAME: dark, or night, color mode for output
Changes the color scheme to a built in dark mode, made for light terminal
backgrounds, rather than the default color scheme which assumes a dark
terminal background color.

FLAG: -h OR --help
HUMAN-READABLE NAME: help page
DESCRIPTION:
Displays a summary of this information.

===============================================================================
COMPATIBILITY
===============================================================================

This program is meant to be run in the Python 3 interpreter. Testing has only
been carried out on Python 3.4.5 on Windows. Output is printed using high-ASCII
and unicode characters, and support for these features is anticipated. Output
is colorized using ANSI escape codes, and animation relies on the ANSI terminal
traversal codes to rewrite the screen; as such, support for this feature is
expected for full functionality. 

Behavior in an environment which does not meet these criteria is undefined, as
no attempt is made to recover from errors pertaining to these things.

===============================================================================
ERRORS
===============================================================================

Each error has its own exit code, which are present in parentheses before their
description.

-------------------------------------------------------------------------------
Errors which are checked by the program are as follows:
-------------------------------------------------------------------------------

MAIN (main.py) ----------------------------------------------------------------

(9) Bad arguments caught by the argument parser (floats for --debug, 
nonexistent options passed, etc.).

(10) -m option not passed to program at all.

(11) Nonexistent path specified for machine file.

(12) A state in the input machine's transition function was not found in Q.

(13) A state in the input machine's transition function was not transitioning 
to the accept or reject state and also did not specify a bit to write or
direction to move.

(14) NAME field not found

(15) STATE field not found

(16) SIGMA field not found

(17) GAMMA field not found

(18) START field not found

(19) ACCEPT field not found

(20) REJECT field not found

(21) Nonexistent path specified for tape file.

(22) A state to explicitly halt at was specified, but not found in Q.

(23) State in DELTA contained a non-ASCII character.

(24) A symbol in SIGMA contained a non-ASCII character.

(25) A symbol in GAMMA contained a non-ASCII character.

(130) SIGINT sent by user.

TAPE (tape.py): ---------------------------------------------------------------

(32) A symbol on the input tape was not found in the input alphabet.

TURING MACHINE (tm.py): -------------------------------------------------------

(34) A symbol to be written was not in the tape alphabet.

(36) A state in the input machine's transition function specified a direction, 
but it was a character other than 'L' or 'R'.

-------------------------------------------------------------------------------
Errors which are specified by the class Turing machine spec, but are not
treated as such by this program:
-------------------------------------------------------------------------------

Uncommented lines containing random words are allowed throughout the file, and
have no effect on the program unless they can be confused for states. 
Explicitly, lines in the DELTA section which are not comprised of 3, 4, or 5 
whitespace-delimited fields are ignored in input, and fields before the DELTA
section are ignored if they do not begin with one of the keywords (STATE,
GAMMA, SIGMA, etc).

Comments and other lines in the file are not checked for non-ASCII characters.

===============================================================================
DEPENDENCIES
===============================================================================

From the core python libraries, this program depends on:
argparse // parse command line arguments
time     // sleep between frames when animating the machine
signal   // catch Ctrl+C exit so the Python interpreter doesn't spit garbage
shutil   // get dimensions of terminal so we never have ugly output

There are no external dependencies.

===============================================================================
FILES
===============================================================================

The following modules are included in this program:
main.py       Parses command line arguments and initializes data structures.
tape.py       Represents a Turing machine tape as a doubly linked list.
tm.py         Creates and runs a Turing machine.
colors.py     Contains single-point of truth colors for customization.
README        This README file

===============================================================================
EXAMPLE
===============================================================================

$> python3 main.py -m ./machine --debug 2
Input:
01
┌─────────────┬─────────┬──────────┬─────────────┬─────────────┐
│ STATE: q0   │ READ: 0 │ WRITE: o │ GO TO: qo1  │ MOVE: RIGHT │
└─────────────┴─────────┴──────────┴─────────────┴─────────────┘
╔═▼═╗───┬───┬────
║ 0 ║ 1 │ B │ ···
╚═▲═╝───┴───┴────

┌─────────────┬─────────┬──────────┬─────────────┬─────────────┐
│ STATE: qo1  │ READ: 1 │ WRITE: i │ GO TO: qrb  │ MOVE: RIGHT │
└─────────────┴─────────┴──────────┴─────────────┴─────────────┘
┌───╔═▼═╗───┬────
│ o ║ 1 ║ B │ ···
└───╚═▲═╝───┴────

┌─────────────┬─────────┬──────────┬─────────────┬─────────────┐
│ STATE: qrb  │ READ: B │ WRITE:   │ GO TO: qa   │ MOVE:       │
└─────────────┴─────────┴──────────┴─────────────┴─────────────┘
┌───┬───╔═▼═╗────
│ o │ i ║ B ║ ···
└───┴───╚═▲═╝────

┌────────────────────┐
│ ┌─┐┌─┐┌─┐┌─┐┌─┐┌┬┐ │
│ ├─┤│  │  ├┤ ├─┘ │  │
│ ┴ ┴└─┘└─┘└─┘┴   ┴  │
└────────────────────┘

===============================================================================
TODO
===============================================================================

print comments above state
left and right arrow keys step through (allow backwards stepping)
pretty-print table of states
generate diagram of transition function representation of machine
scroll tape when tape is too long for terminal, rather than truncating
