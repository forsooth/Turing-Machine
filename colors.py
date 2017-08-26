# Escape codes for various colors
white = '\033[38;5;15m'
green = '\033[38;5;10m'
red = '\033[38;5;09m'
cyan = '\033[38;5;14m'
yellow = '\033[38;5;228m'
grey = '\033[38;5;08m'
dark_cyan = '\033[38;5;06m'

# default 16-color terminal codes:
dark_red_16 = '\033[38;5;01m'
dark_green_16 = '\033[38;5;02m'
dark_yellow_16 = '\033[38;5;03m'
dark_blue_16 = '\033[38;5;04m'
dark_purple_16 = '\033[38;5;05m'
dark_cyan_16 = '\033[38;5;06m' # note: same as above
dark_white_16 = '\033[38;5;07m'
dark_grey_16 = '\033[38;5;08m' # note: same as above
red_16 = '\033[38;5;09m' # note: same as above
green_16 = '\033[38;5;10m' # note: same as above
yellow_16 = '\033[38;5;11m'
blue_16 = '\033[38;5;12m'
purple_16 = '\033[38;5;13m'
cyan_16 = '\033[38;5;14m' # note: same as above
white_16 = '\033[38;5;15m' #note: same as above
black_16 = '\033[38;5;16m'

# for Adam
dark_dark_green = '\033[38;5;34m'

# The externally accessed variables for these colors.

# Text for fields in the box for debug level 2's state print box.
state_text = dark_cyan
# The color of a bit in debug level 2's when the bit being written
# is different than the one which was read.
changed_bit = green
# The color of the box around the tape head, in debug level 2.
tape_box_2 = cyan
# The color of the arrows on the tape head in debug level 2.
tape_head_2 = yellow
# The color of the box around the tape head in debug level 1.
tape_box_1 = yellow
# The color of other boxes on the tape in debug level 1.
tape_1 = grey
# The color of the stamp / text for the accept text.
accept = green
# The color of the stamp / text for the reject text.
reject = red
# The color of the stamp / text for a halted and aborted machine.
abort = yellow
# The color of other text in the program.
default = white
# The color of highlighted elements on the tape
hlighted = yellow
# The color of the character currently under the tape head
selected = green