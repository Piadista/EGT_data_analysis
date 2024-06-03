import originpro as op
import numpy as np
import pandas as pd


# Very useful, especially during development, when you are
# liable to have a few uncaught exceptions.
# Ensures that the Origin instance gets shut down properly.
# Note: only applicable to external Python.
import sys
def origin_shutdown_exception_hook(exctype, value, traceback):
    '''Ensures Origin gets shut down if an uncaught exception'''
    op.exit()
    sys.__excepthook__(exctype, value, traceback)
if op and op.oext:
    sys.excepthook = origin_shutdown_exception_hook


# Set Origin instance visibility.
# Important for only external Python.
# Should not be used with embedded Python. 
if op.oext:
    op.set_show(True)


# Example of opening a project and reading data.

# We'll open the Tutorial Data.opju project that ships with Origin.
src_opju = op.path('e')+ r'Samples\Tutorial Data.opju'
op.open(file = src_opju, readonly = True)

# Simple syntax to find a worksheet.
src_wks = op.find_sheet('w', 'Book1A')

# Pull first column data into a list and dump to screen.
lst = src_wks.to_list(0)
print(*lst, sep = ", ")

# Pull entire worksheet into a pandas DataFrame and partially dump to screen.
# Column long name will be columns name.
df = src_wks.to_df()
print(df.head())


# Start a new project which closes the previous one.
op.new()


#Examples of writing data to a project and saving it.

# We'll reuse the data objects we previously created.

# Simple syntax to create a new workbook with one sheet
dest_wks = op.new_sheet('w')

# Insert list data into columns 1
dest_wks.from_list(0, lst)

# Add another sheet top above workbook and add the DataFrame data.
# DataFrame column names with be Origin column Long Names.
dest_wks.get_book().add_sheet().from_df(df)

# Save the opju to your UFF.
op.save(op.path('u')+ 'Ext Python Example 1.opju')


# Exit running instance of Origin.
# Required for external Python but don't use with embedded Python.
if op.oext:
    op.exit()
op.save('C:\\Users\\Edu\\Desktop\\Test\\Ext_Python_3.opju')