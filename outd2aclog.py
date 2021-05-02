# OUTD 2 ACLOG
# ------------
# By: N6ARA

# Converts OutD ADIF log files to ACLOG (N3FJP) ADIF parseable log files

from tkinter import *
from tkinter import filedialog

filename_var = ""

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          filetypes=[("ADIF files", "*.adif")],
                                          title = "Select a File",
                                          )
    
    global filename_var         # Don't judge globals. The quick and dirty hack always works.
    filename_var = filename

    label_file_explorer.configure(text=".."+filename[-25:])

def openFile(input_filename):
    fin = open(input_filename, 'rt')

    try:
        input_filename.index("OutdLog-")
    except ValueError:
        label_file_explorer.configure(text="  Invalid File!        ")
    else:
        output_filename = input_filename.replace("OutdLog-", "ACLOG-")
        fout = open(output_filename, 'w+')

        for line in fin:

            if len(comment_var.get()) == 0:
                new_line = line.replace('QSPMSG', 'COMMENT')
                new_line = line.replace('<EOR>', '<OTHER:4>' + other_var.get() + '<MY_GRIDSQUARE:4>' + grid_var.get() + '<EOR>')
            else:
                new_line = line.replace('<EOR>', '<OTHER:4>' + other_var.get() + '<MY_GRIDSQUARE:4>' + grid_var.get() + '<COMMENT:' + str(len(comment_var.get())) + '>' + comment_var.get() + '<EOR>')

            fout.write(new_line)
        
        fout.close()

        label_file_explorer.configure(text="  Converted successfully!        ")

    fin.close()

window = Tk()
window.resizable(0, 0)

## If you wish to build an executable with the OUTD-2-ACLOG icon, uncomment and modify the following two lines:
# icon = PhotoImage(file = r"[absolute file path here]\outd2aclogicon.png")
# window.iconphoto(False, icon)

grid_var = StringVar()
other_var = StringVar()
other_var.set( "SOTA" )
comment_var = StringVar()

window.title('OUTD 2 ACLOG')

label_file_explorer = Label(window,
                            text = "Select OutD ADIF file:")

button_explore = Button(window,
                        text = "Browse Files",
                        command = browseFiles)

grid_label = Label(window, text = 'My 4-Digit Gridsqure: ')
grid_entry = Entry(window, textvariable = grid_var)
      
otherfield_label = Label(window, text = 'Type: ',)
otherfield_drop = OptionMenu( window , other_var, "SOTA", "CHASE")

comment_label = Label(window, text = 'Comment: ')
comment_entry = Entry(window, textvariable = comment_var)

button_convert = Button(window,
                     text = "Convert",
                     command = lambda: openFile(filename_var))
  
label_file_explorer.grid(row = 1, column = 0, sticky=E)

button_explore.grid(row = 1, column = 1, sticky=W)

grid_label.grid(row=3,column= 0, sticky=E)
grid_entry.grid(row=3, column=1, sticky=W)

otherfield_label.grid(row = 4, column = 0, sticky=E)
otherfield_drop.grid(row = 4, column = 1, sticky=W)

comment_label.grid(row=5,column= 0, sticky=E)
comment_entry.grid(row=5, column=1, sticky=W)

button_convert.grid(row = 6, column = 1)

window.mainloop()