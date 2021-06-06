# OUTD 2 ACLOG
# ------------
# By: N6ARA

# Converts OutD ADIF log files to ACLOG (N3FJP) ADIF parseable log files

from argparse import ArgumentParser
from tkinter import (Tk, PhotoImage, StringVar, Label, Button, Entry, OptionMenu, E, W)
from tkinter import filedialog

from .static import static_file
from .version import __version__

import re

def browse_files(local):
    filename = filedialog.askopenfilename(initialdir="/",
                                          filetypes=[("ADIF files", "*.adif")],
                                          title="Select a File",
                                          )

    local['filename'] = filename

    local['label_file_explorer'].configure(text=".." + filename[-25:])


def open_file(local, input_filename):
    fin = open(input_filename, 'rt')

    try:
        input_filename.index("OutdLog-")
    except ValueError:
        local['label_file_explorer'].configure(text="  Invalid File!        ")
    else:
        output_filename = input_filename.replace("OutdLog-", "ACLOG-")
        output_filename = output_filename[:len(output_filename)-1]    # Make the .adif into .adi
        fout = open(output_filename, 'w+')

        for line in fin:

            if len(local['comment'].get()) == 0:
                new_line = line.replace('QSPMSG', 'COMMENT')

                # If left blank, auto-comment "SOTA [summit]" for regular chasers and "SOTA [summit] - S2S - [summit]" for S2S

                # Read My SOTA Reference
                msr = re.compile(r'<MY_SOTA_REF:\d+>([^<>]*?)<')
                msr_match = msr.search(new_line)

                if msr_match is None:
                    my_sota_ref = ""
                else:
                    my_sota_ref = msr_match.group(1)

                # Read Other SOTA Reference if S2S
                sr = re.compile(r'<SOTA_REF:\d+>([^<>]*?)<')
                sr_match = sr.search(new_line)

                if sr_match is None:
                    sota_ref = ""
                else:
                    sota_ref = sr_match.group(1)

                # Generate auto-comment
                if len(sota_ref) == 0:
                    # Regular SOTA contact
                    autocomment = "SOTA " + my_sota_ref
                else:
                    # S2S
                    autocomment = "SOTA " + my_sota_ref + " - S2S - " + sota_ref

                new_line = new_line.replace('<EOR>',
                                            '<OTHER:4>' + local['other'].get() + '<MY_GRIDSQUARE:4>' +
                                            local['grid'].get() + 
                                            '<COMMENT:' + str(len(autocomment)) + '>' + autocomment +
                                            '<EOR>')
            else:
                new_line = line.replace('<EOR>',
                                        '<OTHER:4>' + local['other'].get() + '<MY_GRIDSQUARE:4>' + local['grid'].get() +
                                        '<COMMENT:' + str(len(local['comment'].get())) + '>' + local['comment'].get() +
                                        '<EOR>')

            fout.write(new_line)

        fout.close()

        local['label_file_explorer'].configure(text="  Converted successfully!        ")

    fin.close()


def main():
    parser = ArgumentParser(description='Converts OutD ADIF log files to ACLOG (N3FJP) ADIF parsable log files')
    parser.add_argument('--version',
                        help='Print version and exit.',
                        action='version',
                        version=__version__)
    _ = parser.parse_args()  # This could have more args in the future

    window = Tk()
    window.title('OUTD 2 ACLOG')
    window.resizable(0, 0)

    #icon = PhotoImage(file=static_file('outd2aclogicon.png'))
    #window.iconphoto(False, icon)

    # local stores mutable data that is used by different parts of the GUI
    local = {
        'filename': "",
        'grid': StringVar(),
        'other': StringVar(),
        'comment': StringVar(),
        'label_file_explorer': Label(window, text="Select OutD ADIF file:"),
    }

    local['other'].set("SOTA")

    button_explore = Button(window,
                            text="Browse Files",
                            command=lambda: browse_files(local))

    grid_label = Label(window, text='My 4-Digit Gridsqure: ')
    grid_entry = Entry(window, textvariable=local['grid'])

    otherfield_label = Label(window, text='Type: ', )
    otherfield_drop = OptionMenu(window, local['other'], "SOTA", "CHASE")

    comment_label = Label(window, text='Comment: ')
    comment_entry = Entry(window, textvariable=local['comment'])

    button_convert = Button(window,
                            text="Convert",
                            command=lambda: open_file(local, local['filename']))

    local['label_file_explorer'].grid(row=1, column=0, sticky=E)

    button_explore.grid(row=1, column=1, sticky=W)

    grid_label.grid(row=3, column=0, sticky=E)
    grid_entry.grid(row=3, column=1, sticky=W)

    otherfield_label.grid(row=4, column=0, sticky=E)
    otherfield_drop.grid(row=4, column=1, sticky=W)

    comment_label.grid(row=5, column=0, sticky=E)
    comment_entry.grid(row=5, column=1, sticky=W)

    button_convert.grid(row=6, column=1)

    window.mainloop()
