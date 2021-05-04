# OUTD 2 ACLOG
# ------------
# By: N6ARA

# Converts OutD ADIF log files to ACLOG (N3FJP) ADIF parseable log files

from argparse import ArgumentParser
from tkinter import (Tk, PhotoImage, StringVar, Label, Button, Entry, OptionMenu, E, W)
from tkinter import filedialog

from .version import __version__


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
        fout = open(output_filename, 'w+')

        for line in fin:

            if len(local['comment'].get()) == 0:
                new_line = line.replace('QSPMSG', 'COMMENT')
                new_line = new_line.replace('<EOR>',
                                        '<OTHER:4>' + local['other'].get() + '<MY_GRIDSQUARE:4>' +
                                        local['grid'].get() + '<EOR>')
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

    # If you wish to build an executable with the OUTD-2-ACLOG icon, uncomment and modify the following two lines:
    #icon = PhotoImage(file = r"C:\Users\[userpath]\OUTD_2_ACLOG\outd2aclogicon.png")
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
