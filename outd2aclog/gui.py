# OUTD 2 ACLOG
# ------------
# By: N6ARA

# Converts OutD ADIF log files to ACLOG (N3FJP) ADIF parseable log files

from argparse import ArgumentParser
from tkinter import (Tk, PhotoImage, StringVar, Label, Button, Entry, OptionMenu, E, W)
from tkinter import filedialog
from sys import platform

if platform == "darwin":
    from tkmacosx import *

from .static import static_file
from .version import __version__

import re

def browse_files(local):
    filename = filedialog.askopenfilename(initialdir="/",
                                          filetypes=[("ADIF files", "*.adif"), ("ADI files", "*.adi")],
                                          title="Select a File",
                                          )

    local['filename'] = filename
    local['label_file_explorer'].configure(text=".." + filename[-25:])  # Show preview of filename


def open_file(local, input_filename):
    fin = open(input_filename, 'rt')

    if "OutdLog-" in input_filename:                                    # Check to see if file is an OutD log by filename
        output_filename = input_filename.replace("OutdLog-", "ACLOG-")  #     Note: Checking programid for "Portable Logger" may cause parsing issues
        output_filename = output_filename[:len(output_filename)-1]      # Change the .adif into .adi
        local['filetype'] = "OUTD"
        
        fout = open(output_filename, 'w+')
    else:
        for line in fin:                                                # Check to see if the file is a HAMRS log file by programid
            if '<programid:5>HAMRS' in line:
                local['filetype'] = "HAMRS"
                output_filename = input_filename.replace(".adi", "-ACLOG.adi")
                fout = open(output_filename, 'w+')

                fin.seek(0)                                     # Reset file line pointer
                fin.readline()                                  # Skip the first line of the HAMRS header (unused info)

                header_line = fin.readline()                    
                fout.write(header_line[1:len(header_line)])     # Write "adif_ver"

                header_line = fin.readline()                    
                fout.write(header_line[1:len(header_line)])     # Write "programid"

                header_line = fin.readline()                    
                fout.write(header_line[1:len(header_line)])     # Write "programversion"

                header_line = fin.readline()                    
                fout.write(header_line[1:len(header_line)])     # Write "EOH"

                break
        
        if local['filetype'] == "Invalid":                              # Invalid File. Abort file parsing and conversion
            local['label_file_explorer'].configure(text="  Invalid File!        ")
            return
    
    # Prepare MY_GRIDSQUARE field
    if local['filetype'] == "OUTD":
        # Add the MY_GRIDSQAURE field if the input file is an OutD Log
        if len(local['grid'].get()) != 0:
            mygridsquare_field = '<MY_GRIDSQUARE:' + str(len(local['grid'].get())) + '>' + local['grid'].get()
        else:
            mygridsquare_field = ''
    else:
        # Don't add the MY_GRIDSQUARE field otherwise (HAMRS does this automatically)
        mygridsquare_field = ''


    # Variables used for HAMRS Parsing
    line = ""
    line_ready = False
    hamrs_combine_state = False

    # Loop through the log file and parse lines depending on filetype, then convert them to the appropriate formatting 
    for readline in fin:

        # HAMRS log records are multi-line, so we need to combine them into one line, uppercase the field names then parse them
        if local['filetype'] == "HAMRS":    

            if hamrs_combine_state == True: # If we are currently combining lines, grab the current line and add it to the line to-be-parsed
                
                # Uppercase the field names
                fieldname = re.search('<(.*):', readline)
                if fieldname is not None:
                    readline_uppercased = readline.replace(fieldname.group(1), fieldname.group(1).upper())

                # Combine to current line minus the line return
                line = line + readline_uppercased[:len(readline_uppercased)-1]

            if readline == '\n':             # Start of record
                hamrs_combine_state = True
            elif readline == '<eor>\n':      # End of record
                hamrs_combine_state = False
                line = line + '<EOR>\n'
                line_ready = True            # Combined HAMRS log record line is ready for parsing

        # OutD log records are one line, so the line is always ready for parsing
        elif local['filetype'] == "OUTD":
            line = readline
            line_ready = True               

        # Convert line when the current line is ready
        if line_ready == True:

            # Read My SOTA Reference
            msr = re.compile(r'<MY_SOTA_REF:\d+>([^<>]*?)<')
            msr_match = msr.search(line)

            if msr_match is None:
                my_sota_ref = ""
            else:
                my_sota_ref = msr_match.group(1)

            # Read Contact SOTA Reference
            sr = re.compile(r'<SOTA_REF:\d+>([^<>]*?)<')
            sr_match = sr.search(line)

            if sr_match is None:
                sota_ref = ""
            else:
                sota_ref = sr_match.group(1)

            # Check for QSPMSG
            qm = re.compile(r'QSPMSG')
            qm_match = qm.search(line)

            if qm_match is None:
                qm_override = False
            else:
                qm_override = True

            # Determine if SOTA, S2S, or Chase
            if (len(my_sota_ref) == 0) and (len(sota_ref) > 0):
                # SOTA Chaser log entry
                sota_type = "CHASE"
            elif (len(my_sota_ref) > 0) and (len(sota_ref) == 0):
                # SOTA Activator log entry
                sota_type = "SOTA"
            else:
                # Summit to Summit
                sota_type = "S2S"

            # If the comment field is not populated
            if len(local['comment'].get()) == 0:

                # Check for OutD QSPMSG field and change to COMMENT field
                if qm_override == True:
                    new_line = line.replace('QSPMSG', 'COMMENT')
                    if sota_type == "CHASE":
                        new_line = new_line.replace('<EOR>',
                                            '<OTHER:5>CHASE' + mygridsquare_field +
                                            '<EOR>')
                    else:
                        new_line = new_line.replace('<EOR>',
                                            '<OTHER:4>SOTA' + mygridsquare_field +
                                            '<EOR>')

                # If QSPMSG is not provided, generate auto-comment
                else:
                    # Generate auto-comment
                    if sota_type == "CHASE":
                        # SOTA CHASE
                        autocomment = "SOTA CHASE " + sota_ref
                        new_line = line.replace('<EOR>',
                                                    '<OTHER:5>CHASE' + mygridsquare_field + 
                                                    '<COMMENT:' + str(len(autocomment)) + '>' + autocomment +
                                                    '<EOR>')
                    elif sota_type == "SOTA":
                        # SOTA
                        autocomment = "SOTA " + my_sota_ref
                        new_line = line.replace('<EOR>',
                                                    '<OTHER:4>SOTA' + mygridsquare_field + 
                                                    '<COMMENT:' + str(len(autocomment)) + '>' + autocomment +
                                                    '<EOR>')
                    elif sota_type == "S2S":
                        # S2S
                        autocomment = "SOTA " + my_sota_ref + " - S2S - " + sota_ref
                        new_line = line.replace('<EOR>',
                                                    '<OTHER:4>SOTA' + mygridsquare_field + 
                                                    '<COMMENT:' + str(len(autocomment)) + '>' + autocomment +
                                                    '<EOR>')
                    else:
                        # Error
                        autocomment = "Unreachable Error!"
                        new_line = line.replace('<EOR>',
                                                    '<OTHER:4>SOTA' + mygridsquare_field + 
                                                    '<COMMENT:' + str(len(autocomment)) + '>' + autocomment +
                                                    '<EOR>')

            # If the GUI Comment field is populated, overwrite all the ADI COMMENT fields with the value
            else:
                if sota_type == "CHASE":
                    new_line = line.replace('<EOR>',
                                            '<OTHER:5>CHASE' + mygridsquare_field +
                                            '<COMMENT:' + str(len(local['comment'].get())) + '>' + local['comment'].get() +
                                            '<EOR>')
                else:
                    new_line = line.replace('<EOR>',
                                            '<OTHER:4>SOTA' + mygridsquare_field +
                                            '<COMMENT:' + str(len(local['comment'].get())) + '>' + local['comment'].get() +
                                            '<EOR>')

            fout.write(new_line)
            line_ready = False
            line = ""

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
        'comment': StringVar(),
        'label_file_explorer': Label(window, text="Select ADIF/ADI file:"),
        'filetype': "Invalid",
    }

    button_explore = Button(window,
                            text="Browse Files",
                            command=lambda: browse_files(local))

    grid_label = Label(window, text='My Gridsquare: ')
    grid_entry = Entry(window, textvariable=local['grid'])

    comment_label = Label(window, text='Comment: ')
    comment_entry = Entry(window, textvariable=local['comment'])

    button_convert = Button(window,
                            text="Convert",
                            command=lambda: open_file(local, local['filename']))

    local['label_file_explorer'].grid(row=1, column=0, sticky=E)

    button_explore.grid(row=1, column=1, sticky=W)

    grid_label.grid(row=3, column=0, sticky=E)
    grid_entry.grid(row=3, column=1, sticky=W)

    comment_label.grid(row=5, column=0, sticky=E)
    comment_entry.grid(row=5, column=1, sticky=W)

    button_convert.grid(row=6, column=1)

    window.mainloop()
