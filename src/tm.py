from tape import Tape
import colors
import time
import shutil

class TM:

    # Our core turing machine structure is essentially the classic
    # 7-tuple with some fluff: the debug level, the time step between
    # animation steps, the name of the machine, and the blank character.
    def __init__(self, debug, tflag, haltafter, haltat, step, name, B, Q, Σ, Γ, q_0, q_a, q_r, δ):
        self.debug = debug
        self.tflag = tflag
        self.haltafter = haltafter
        self.haltat = haltat
        self.lastexit = 0
        self.step = step

        self.accstr = (colors.accept + "┌────────────────────┐" + '\n' +
                                       "│ ┌─┐┌─┐┌─┐┌─┐┌─┐┌┬┐ │" + '\n' +
                                       "│ ├─┤│  │  ├┤ ├─┘ │  │" + '\n' +
                                       "│ ┴ ┴└─┘└─┘└─┘┴   ┴  │" + '\n' +
                                       "└────────────────────┘" + '\n'
                                       + colors.default)

        self.rejstr = (colors.reject + "┌────────────────────┐" + '\n' +
                                       "│  ┬─┐┌─┐ ┬┌─┐┌─┐┌┬┐ │" + '\n' +
                                       "│  ├┬┘├┤  │├┤ │   │  │" + '\n' +
                                       "│  ┴└─└─┘└┘└─┘└─┘ ┴  │" + '\n' +
                                       "└────────────────────┘" + '\n'
                                       + colors.default)

        self.halstr = (colors.abort  + "┌────────────────────┐" + '\n' +
                                       "│   ┌─┐┌┐ ┌─┐┬─┐┌┬┐  │" + '\n' +
                                       "│   ├─┤├┴┐│ │├┬┘ │   │" + '\n' +
                                       "│   ┴ ┴└─┘└─┘┴└─ ┴   │" + '\n' +
                                       "└────────────────────┘" + '\n'
                                       + colors.default)

        if debug != 2:
            self.accstr = colors.accept + "Accept" + colors.default
            self.rejstr = colors.reject + "Reject" + colors.default
            self.halstr = colors.abort + "Abort" + colors.default

        # Store the number of characters in the longest state, for formatting.
        self.maxlen = max([len(q) for q in Q])
        self.langlen = max([len(g) for g in Γ])

        self.numsteps = 0
        self.name = name
        self.B = B
        self.Q = Q
        # Fun fact: unicode has been supported in Python identifiers since 
        # PEP 3131 in 2007 (Python 3.0).
        self.Σ = Σ
        self.Γ = Γ
        self.ΓsubΣ = [s for s in Γ if s not in Σ and s != B]
        self.q_0 = q_0
        self.q_a = q_a
        self.q_r = q_r
        self.δ = δ
        self.curr_tape = None
        self.curr_state = q_0
        self.R = 'R'
        self.L = 'L'

    # Run the gen_tape function on the string tape to create our
    # tape data structure.
    def add_tape(self, tape):
        self.curr_tape = Tape.gen_tape(tape, self.Σ, self.B)

    def remove_tape(self):
        self.curr_tape = None

    # This is the core of the machine. Here we run through 
    # each state of the Turing machine.
    def run_tape(self):
        # Until the machine explicitly halts or aborts, run.
        termw, termh = shutil.get_terminal_size()

        while True:

            if self.haltafter > 0 and self.numsteps == self.haltafter:
                break

            if self.curr_state == self.haltat:
                break

            bit = self.curr_tape.read()
            # attempt to extract a transition corresponding to this current bit on
            # the tape and current state. If we cannot, then we have reached an 
            # implicit rejection.
            try:
                newstate, newbit, direction = self.δ[self.curr_state + ' ' + bit]
            except KeyError:
                if self.debug > 0:
                    print("No valid transition function found from state {} on input {}".format(self.curr_state, bit))
                self.lastexit = 1
                return self.rejstr

            # Store a copy of the bit-to-write so we can add color codes to it.
            printbit = newbit

            # Print out the state and turing machine tape.
            if self.debug == 2:
                # Create a 5-character word for the direction we're moving.
                move = 'RIGHT'
                if direction == 'L':
                    move = 'LEFT '
                if newstate == self.q_a:
                    move = '     '
                    printbit = ' '
                
                # Store the raw length of every string we're going to print, as
                # adding color codes changes the length.
                writelen = len('│ WRITE: {} '.format(printbit))
                statelen = len('│ STATE: {} '.format(self.curr_state) + ' ' * (self.maxlen - len(self.curr_state)))
                readlen = len('│ READ: {} '.format(bit))
                gotolen = len('│ GO TO: {} '.format(newstate) + ' ' * (self.maxlen - len(newstate)))
                movelen = len('│ MOVE: {} │'.format(move))

                # Format the box for printing the state. Looks like this:
                #┌─────────────┬─────────┬──────────┬─────────────┬─────────────┐
                #│ STATE: q0   │ READ: 0 │ WRITE: 1 │ GO TO: q1   │ MOVE: LEFT  │
                #└─────────────┴─────────┴──────────┴─────────────┴─────────────┘
                state = '│ ' + colors.state_text + 'STATE: ' + colors.default + '{} '.format(self.curr_state) + ' ' * (self.maxlen - len(self.curr_state))
                read = '│ ' + colors.state_text + 'READ: ' + colors.default + '{} '.format(bit)
                if bit == printbit:
                    write = '│ ' + colors.state_text + 'WRITE: {} '.format(colors.default + printbit)
                else:
                    write = '│ ' + colors.state_text + 'WRITE: {} '.format(colors.changed_bit + printbit + colors.default)
                if newstate == self.q_a:
                    goto = '│ ' + colors.state_text + 'GO TO: ' + colors.default + '{} '.format(colors.accept + newstate + colors.default) + ' ' * (self.maxlen - len(newstate))
                elif newstate == self.q_r:
                    goto = '│ ' + colors.state_text + 'GO TO: ' + colors.default + '{} '.format(colors.reject + newstate + colors.default) + ' ' * (self.maxlen - len(newstate))
                else:
                    goto = '│ ' + colors.state_text + 'GO TO: ' + colors.default + '{} '.format(newstate) + ' ' * (self.maxlen - len(newstate))
                move = '│ ' + colors.state_text + 'MOVE: {} │     '.format(colors.default + move)

                top = '┌' + (statelen - 1) * '─' + '┬' + (readlen - 1) * '─' + '┬' + (writelen - 1) * '─' + '┬' + (gotolen - 1) * '─' + '┬' + (movelen - 2) * '─' + '┐     '
                mid = state + read + write + goto + move
                bottom = '└' + (statelen - 1) * '─' + '┴' + (readlen - 1) * '─' + '┴' + (writelen - 1) * '─' + '┴' + (gotolen - 1) * '─' + '┴' + (movelen - 2) * '─' + '┘     '
                print(top)
                print(mid)
                print(bottom)
                
            # If our debug level is 1 or 2, print the tape. The print function
            # handles the difference between debug level 1 and 2.
            # We print a newline after, to separate states.
            if self.debug > 0:
                self.curr_tape.print_tape(self.ΓsubΣ, direction, self.debug, self.langlen)
                print("")

            # If tflag is nonzero, then the user has requested an animated
            # output and we need to deal with that. If debug level is 2, then
            # we have six lines of input.
            if self.debug == 2 and (self.step == True or self.tflag > 0):
                # first, sleep after we have printed out the step for the desired time.
                if self.tflag > 0:
                    time.sleep(self.tflag)
                if self.step == True:
                    input("")
                # Bring the terminal output cursor up six lines.
                for i in range(0, 7):
                    print('\033[F', end = '')
                # store the length of the biggest line of output in tapecs.
                spaces = ' ' * termw
                # flush the output clear, by printing out that many spaces.
                for i in range(0, 6):
                    print(spaces)
                if self.tflag > 0:
                    print(spaces)
                # After flushing, go back up six lines again, in preparation for
                # printing out the next frame of our output.
                for i in range(0, 7):
                    print('\033[F', end = '')
                
            # If we have debug == 1, we do the same thing, except we only
            # have one line of output.
            elif self.debug == 1 and (self.step == True or self.tflag > 0):
                if self.tflag > 0:
                    time.sleep(self.tflag)
                if self.step == True:
                    input("")

                time.sleep(self.tflag)
                print('\033[F', end = '')
                if self.step == True:
                    print('\033[F', end = '')
                spaces = ' ' * termw
                print(spaces)
                if self.step == True:
                    print(spaces)
                print('\033[F', end = '')
                if self.step == True:
                    print('\033[F', end = '')
    
            # Check that the bits we're dealing with, and the state
            # we are being sent to, are in their respective sets.
            if newbit not in self.Γ:
                print("Symbol '{}' on tape not recognized. Exiting.".format(newbit))
                exit(34)
                
            # Send the machine to the next state
            self.curr_state = newstate

            # If we have reached an accept or reject state, end the machine.
            if self.debug == 2 and (newstate == self.q_a or newstate == self.q_r):
                spaces = ' ' * termw
                print(spaces)
            if newstate == self.q_a:
                self.lastexit = 0
                return self.accstr
            elif newstate == self.q_r:
                self.lastexit = 1
                return self.rejstr

            # Write to the tape in accordance with the state we were at.
            self.curr_tape.write(newbit)
            
            # Move the tape head depending on the direction specified by the
            # transition function.
            if direction == self.L:
                self.curr_tape = self.curr_tape.l()
            elif direction == self.R:
                self.curr_tape = self.curr_tape.r()
            else:
                print("Direction specified in δ not equal to L or R. Exiting.")
                exit(36)

            self.numsteps += 1

        self.lastexit = 2
        print()
        return self.halstr

    def get_last_exit(self):
        return self.lastexit