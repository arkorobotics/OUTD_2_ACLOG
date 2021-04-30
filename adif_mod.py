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
        print("Invalid file!")
    else:
        output_filename = input_filename.replace("OutdLog-", "ACLOG-")
        fout = open(output_filename, 'w+')

        replace_string = '<OTHER:4>' + other_var.get() + '<MY_GRIDSQUARE:4>' + grid_var.get() + '<EOR>'

        for line in fin:
            new_line = line.replace('QSPMSG', 'COMMENT')
            new_line = line.replace('<EOR>', replace_string)

            fout.write(new_line)
        
        fout.close()

    fin.close()

    label_file_explorer.configure(text="  Converted successfully!        ")

window = Tk()
window.resizable(0, 0)

grid_var = StringVar()
other_var = StringVar()
other_var.set( "SOTA" )

window.title('OUTD 2 ACLOG')
  
window.config(background='#3E4149')

label_file_explorer = Label(window,
                            text = "Select OutD ADIF file:           ",
                            fg = "white",
                            background='#3E4149')

button_explore = Button(window,
                        text = "Browse Files", highlightbackground='#3E4149',
                        command = browseFiles)

grid_label = Label(window, text = 'My 4-Digit Gridsqure: ', fg = "white", background='#3E4149')
grid_entry = Entry(window, textvariable = grid_var, highlightbackground='#3E4149')
      
otherfield_label = Label(window, text = 'Type: ', fg = "white", background='#3E4149')
otherfield_drop = OptionMenu( window , other_var, "SOTA", "CHASE")
otherfield_drop.config(background='#3E4149')
otherfield_drop.pack()

button_convert = Button(window,
                     text = "Convert", highlightbackground='#3E4149',
                     command = lambda: openFile(filename_var))

button_exit = Button(window,
                     text = "Exit", highlightbackground='#3E4149',
                     command = exit)
  
label_file_explorer.grid(row = 1, column = 0, sticky=E)

button_explore.grid(row = 1, column = 1, sticky=W)

grid_label.grid(row=3,column= 0, sticky=E)
grid_entry.grid(row=3, column=1, sticky=W)

otherfield_label.grid(row = 4, column = 0, sticky=E)
otherfield_drop.grid(row = 4, column = 1, sticky=W)

button_convert.grid(row = 5, column = 1)
button_exit.grid(row = 5, column = 0)

window.mainloop()