import colors
import shutil

# The tape structure is a doubly-linked list with no access to
# its head or tail. Each space contains a character 'bit', and
# we store a blank character. 'None' is used for blank nodes.
class Tape:
    
    def __init__(self, blank, bit, prev=None, after=None):
        self.bit = bit
        self.blank = blank
        self.prev = prev
        self.after = after

    # This method creates a tape from a string. It also checks
    # that the characters in the tape input are valid in the 
    # input alphabet.
    @staticmethod
    def gen_tape(tapestr, alphabet, blank):
        t = Tape(blank, blank, None, None)
        # reverse the string
        s = tapestr[::-1]
        for i in range(0, len(s)):
            if s[i] not in alphabet and s[i] != blank:
                print("Symbol on initial tape not in input alphabet. Exiting.")
                exit(32)
            # add each character's node to the left of the previous one.
            t.add_l(s[i])
            t = t.l()
        return t

    def r(self):
        if self.after is None:
            newr = Tape(self.blank, self.blank, self, None)
            self.after = newr
        return self.after

    def l(self):
        if self.prev is None:
            return self
        return self.prev

    def read(self):
        return self.bit

    def write(self, bit):
        old = self.bit
        self.bit = bit
        return old

    def add_l(self, newbit):
        # if self has no left, None is passed as the
        # second parameter; if it does, that data persists
        # by being passed in as the second parameter. Either
        # way, expected behavior is established.
        newl = Tape(self.blank, newbit, self.prev, self)
        self.prev = newl

    def add_r(self, newbit):
        newr = Tape(self.blank, newbit, self, self.after)
        self.after = newr

    # Print the tape, depending on the current debug settings.
    # Debug = 0 means no printing occurs. Debug = 1 prints a 
    # minimal array representation on a single line. Debug = 2
    # prints a full, ASCII art tape with pretty colors.
    def print_tape(self, highlighted, direction, debug=2, langlen=1):

        # Make a copy of our linked list, go all the way to the
        # left, and then walk it to build up an array containing
        # all of the elements of the tape for easy formatting.
        arr = []
        index = 0
        head = self.l()
        prevhead = self
        # Go as far left as possible.
        while prevhead != head:
            temp = head.l()
            prevhead = head
            head = temp
            index += 1
        curr = head
        # Walk the list and add to array.
        while curr is not None and curr.read() != self.blank:
            arr.append(curr.read())
            curr = curr.r()
        
        # Full, pretty tape printing. Looks like this:
        #┌───┬───┬───┬───┬───┬───┬───┬───╔═▼═╗────
        #│ 0 │ 0 │ 1 │ 1 │ 0 │ 1 │ 0 │ 1 ║ B ║ ···
        #└───┴───┴───┴───┴───┴───┴───┴───╚═▲═╝────
        if debug == 2:
            termw, termh = shutil.get_terminal_size()
            ll = langlen - langlen % 2
            # Between middle boxes, we use the character '┬', but at the
            # beginning we need '┌'.
            openboxt = '┌───' + '─' * ll
            openboxb = '└───' + '─' * ll
            if index == 0:
                openboxt = ''
                openboxb = ''
                index = 0

            # create a line looking like this: ┌───┬───┬───┬───┬───┬───┬───┬───╔═▼═╗────
            overlines = (openboxt 
                        + (('┬───' + '─' * ll) * (index - 1)) 
                        + (colors.tape_box_2 + '╔═' + '═' * (ll // 2) 
                        + colors.tape_head_2 + '▼' + colors.tape_box_2
                        + '═' * (ll // 2) + '═╗' + colors.default)
                        + (('─' * ll + '───┬') * (len(arr) - index)) 
                        + '────')
            
            toomanychars = False
            if len(overlines) > termw:
                toomanychars = True
                difflen = len(overlines) - termw
                csperelem = len(overlines) / len(arr)
                overby = int(difflen / (csperelem))
                arr = arr[:len(arr) - overby]
                index = min(index, len(arr))
                if index >= len(arr):
                    overlines = (openboxt 
                                + (('┬───' + '─' * ll) * (index - 1)) 
                                + colors.tape_box_2 + '╔═' + '═' * (ll // 2) 
                                + '═' 
                                + '═' * (ll // 2) 
                                + '══' + colors.default)
                else:
                    overlines = (openboxt 
                                + (('┬───' + '─' * ll) * (index - 1)) 
                                + (colors.tape_box_2 + '╔═' + '═' * (ll // 2) 
                                + colors.tape_head_2 + '▼' + colors.tape_box_2 
                                + '═' * (ll // 2) + '═╗' + colors.default) 
                                + ('─' * ll + '───┬') * (len(arr) - index - 1) 
                                + '────')

            # create a line looking like this: └───┴───┴───┴───┴───┴───┴───┴───╚═▲═╝────
            if toomanychars:
                if index >= len(arr):
                    underlines = (openboxb 
                                 + (('┴───' + '─' * ll) * (index - 1)) 
                                 + colors.tape_box_2 + '╚═' + '═' * (ll // 2) 
                                 + '═' 
                                 + '═' * (ll // 2) 
                                 + '══' + colors.default)
                else:
                    underlines = (openboxb 
                                 + (('┴───' + '─' * ll) * (index - 1)) 
                                 + (colors.tape_box_2 + '╚═' + '═' * (ll // 2)
                                 + colors.tape_head_2 + '▲' + colors.tape_box_2
                                 + '═' * (ll // 2) + '═╝' + colors.default) 
                                 + ('─' * ll + '───┴') * (len(arr) - index - 1)
                                 + '────')
            else:
                underlines = (openboxb 
                             + (('┴───' + '─' * ll) * (index - 1)) 
                             + (colors.tape_box_2 + '╚═' + '═' * (ll // 2) 
                             + colors.tape_head_2 + '▲' + colors.tape_box_2 
                             + '═' * (ll // 2) + '═╝' + colors.default) 
                             + (('─' * ll + '───┴') * (len(arr) - index)) 
                             + '────')
            print(overlines)
            
            # If we are at the tape head, before even starting, i.e. the head is at
            # the beginning of the tape, the left pillar has to be highlighted.
            if index == 0:
                print(colors.tape_box_2 + '║' + colors.default, end='')
            else:
                print('│', end='')

            # Looping through the elements in the array, we want to print out vertical
            # bars between the characters on the tape, with the tape head highlighted
            # with thicker vertical bars. We keep track of how far away from the tape
            # head we are in 'index'
            for elem in arr:
                lenbox = 1 + ll
                spaces = lenbox - len(elem)
                exsp = spaces % 2
                halfsp = spaces // 2
                pelem = elem
                if index == 0:
                    pelem = colors.selected + elem + colors.default
                elif elem in highlighted:
                    pelem = colors.hlighted + elem + colors.default
                
                print(' ' + ' ' * (halfsp + exsp) 
                      + pelem 
                      + ' ' * (halfsp), end='')
                
                if index == 1 or index == 0:
                    print(' ' + colors.tape_box_2 
                          + '║' + colors.default, end='')
                else:
                    print(' │', end='')
                index -= 1
            # If the tape head is on the blank space, we want to highlight the blank
            # manually.
            if not toomanychars:
                if index == 0:
                    print(' ' + ' ' * (ll // 2) 
                          + colors.selected + self.blank + colors.default 
                          + ' ' + ' ' * (ll // 2) 
                          + colors.tape_box_2 + '║' + colors.default + ' ···')
                else:
                    print(' ' + ' ' * (ll // 2) 
                          + self.blank 
                          + ' ' + ' ' * (ll // 2) + '│ ···')
            else:
                if index == 0 and direction == 'R':
                    #➤
                    print(colors.tape_head_2 + ' ⮞⮞⮞' + colors.default)
                elif index == 0 and direction == 'L':
                    print(colors.tape_head_2 + ' ⮜⮜⮜' + colors.default)
                else:
                    print(' ···')
            print(underlines)

        # If debug is 1, we instead want to print out each line looking like this:
        # [o][o][1][1][0][1][0][1][B][···
        # coloring is done using index, as above.
        elif debug == 1:
            for elem in arr:
                if index == 0:
                    print(colors.tape_box_1 + '[' + colors.default, end='')
                    print(colors.selected + elem + colors.default, end='')
                else:
                    print(colors.tape_1 + '[' + colors.default, end='')
                    if elem in highlighted:
                        print(colors.hlighted + elem + colors.default, end='')
                    else:
                        print(elem, end='')
                if index == 0:
                    print(colors.tape_box_1 + ']' + colors.default, end='')
                else:
                    print(colors.tape_1 + ']' + colors.default, end='')
                index -= 1

            if index == 0:
                print(colors.tape_box_1 + '[' + colors.default 
                      + self.blank 
                      + colors.tape_box_1 + ']' + colors.default 
                      + colors.tape_1 + '[' + colors.default + '···', end='')
            else:
                print(colors.tape_1 + '[' + colors.default 
                      + self.blank 
                      + colors.tape_1 + ']' + colors.default 
                      + colors.tape_1 + '[' + colors.default + '···', end='')

