from tkinter import *
from PIL import ImageTk, Image
import sqlite3 
import textwrap
from tkinter import ttk # for scroll bar

root = Tk()
root.title("Movie Reviews Database")
root.geometry ("500x900")
# root.configure(background='white')
# Create database
connect1 = sqlite3.connect('jullya_reviews.db')

# Create cursor
c1 = connect1.cursor()

# Create database table to store reviews
c1.execute(""" CREATE TABLE IF NOT EXISTS reviews (
           oid INTEGER PRIMARY KEY AUTOINCREMENT,
           author_full_name text,
           movie_name text,
           rating int,
           essay text
           )""")

def update():
        
    connect1 = sqlite3.connect('jullya_reviews.db')
    c1 = connect1.cursor()
    record_id = delete_box.get() # ID to be updated is the one that was entered in the delete box. 
    c1.execute(""" UPDATE reviews SET
            author_full_name = :name,
            movie_name = :movie,
            rating = :rating,
            essay = :essay
            WHERE oid = :oid""",
                {
                'name' : author_full_name_editor.get(),
                 'movie' : movie_name_editor.get(),
                 'rating': rating_editor.get(),
                 'essay' : essay_editor.get("1.0", END).strip(),
                 'oid' : record_id
                 }) # python dictionary that designate the key value pairs using the new data name (:first) and its new content(value) which will be f_name_editor.
               
                # The record pulled up has a specific ID key, se we are saying update
                #  these columns (first_name) with this info = :name where our ID is equal 
                # to the designated ID (the one chosen for update)              
                # update sql = update table and set columns where certain things equal certain things

    connect1.commit()
    connect1.close()
    editor.destroy()
    root.deiconify()

def edit(): # This section creates a whole new window. That is why we need new buttons and labes :)
    root.withdraw()
    global editor 
    editor = Tk()
    editor.title("Update review")
    editor.geometry("600x500")
    connect1 = sqlite3.connect('jullya_reviews.db')
    c1 = connect1.cursor()
    record_id = delete_box.get()
    # Query database
    c1.execute("SELECT * FROM reviews WHERE oid = " + record_id) # This is getting all info in addresses for the matching OID in the box. All entries have ids in them. So oid must be included. They make it easier to delete records because each will have an unique ID! 
    records = c1.fetchall()
    # Create global vals for text box names so it can be used in update function
    global author_full_name_editor 
    global movie_name_editor
    global rating_editor
    global essay_editor
    # Copy all the boxes created into the edit function so you'll be able to edit them. Add _editor to the text boxes names so you can see the difference. No need to change the label names cause those won't be changed. 
    # These are NOT in the root window, they are in editor! 

    # Create the text boxes the info is written in for the editor
    author_full_name_editor = Entry (editor, width = 30)
    author_full_name_editor.grid(row=0, column=1, padx=20, pady=(10,0)) 

    movie_name_editor = Entry (editor, width = 30)
    movie_name_editor.grid(row = 1, column = 1)

    rating_editor = Entry (editor, width = 30)
    rating_editor.grid(row = 2, column = 1)

    essay_editor = Text (editor, width = 40, height = 10)
    essay_editor.grid(row = 3, column = 1, pady = 10)

    # delete_box_editor = Entry (editor, width = 30)
    # delete_box_editor.grid (row= 8, column=1, pady=5)

    # Labels for the text boxes in editor
    author_full_name_label = Label (editor, text = "Your full name", font =("Times"))
    author_full_name_label.grid(row=0,column=0, pady=(10,0))

    movie_name_label = Label (editor, text="Movie name", font =("Times"))
    movie_name_label.grid(row=1, column=0)

    rating_label = Label (editor, text="Rating", font =("Times"))
    rating_label.grid(row=2,column=0)

    essay_label = Label (editor, text = "Insert review ", font =("Times"))
    essay_label.grid(row=3, column=0)

    # put info in each box. Loop through results. Each item is in a list, so begin placing them with the oth item. 0th item is f_name, 1th item is l_name, 2nd item is address...
    for record in records:
        author_full_name_editor.insert(0,record[0])
        movie_name_editor.insert(0,record[1])
        rating_editor.insert(0,record[2])
        essay_editor.insert("1.0", record[3])  # Insert the essay text at the beginning of the Text widget
    # Create a save button
    edit_button = Button (editor, text= "Update", command= update)
    edit_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=145)

def delete():
    connect1 = sqlite3.connect('jullya_reviews.db')
    c1 = connect1.cursor()
    c1.execute("DELETE from reviews WHERE oid = " + delete_box.get()) # This is getting what is typed in the delete box.
    connect1.commit()
    connect1.close()

def submit():

    connect1 = sqlite3.connect('jullya_reviews.db')
    c1 = connect1.cursor()

    c1.execute ("INSERT INTO reviews VALUES (:author_full_name, :movie_name, :rating, :essay)",
                { 
                    'author_full_name': author_full_name.get(), # The second "author_full_name" refers to the text box info that's entered under that variable.
                    'movie_name': movie_name.get(),
                    'rating': rating.get(),
                    #'essay': essay.get()
                    'essay': essay.get("1.0", END).strip()  # Retrieve and clean all text from the Text widget, removing extra whitespace. This is different because it is Text and not Entry. It is multiple lines. 
                    # This dictionary stores the info from the text boxes into the table areas under that same name :)
                } )

    connect1.commit()
    connect1.close()
    # Clear text boxes
    author_full_name.delete(0, END)
    movie_name.delete(0, END)
    rating.delete(0, END)
    essay.delete (1.0, END) # This is different because it is Text and not Entry. It is multiple lines. 


def query(): 
    # Connect to the SQLite database
    connect1 = sqlite3.connect('jullya_reviews.db')
    c1 = connect1.cursor()  # Create a cursor object to execute SQL commands

    # Execute a SQL query to select all records from the 'reviews' table
    c1.execute("SELECT *, oid FROM reviews") 
    records = c1.fetchall()  # Fetch all the records from the executed query
    
    # Initialize an empty string to accumulate the review records for display
    print_records = '' 
    for record in records:
        # Format each record as a string and append it to print_records
        print_records += "Author: "+ str(record[0]) +"\n"
        print_records += "Movie: " + str(record[1]) +"\n" 
        print_records += "Rating out of 10: " + str(record[2]) +"\n" 
        print_records += "Review: " + str(record[3]) +"\n" 
        print_records += "\n"

    # Create a LabelFrame to contain the output area for displaying reviews
    output_frame = LabelFrame(root, text="Previous Reviews", font=("Times", 16), padx=10, pady=10)
    output_frame.grid(row=12, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Create a Canvas widget inside the output frame for scrolling content
    canvas = Canvas(output_frame)
    
    # Create a vertical scrollbar for the canvas
    scrollbar = ttk.Scrollbar(output_frame, orient=VERTICAL, command=canvas.yview)
    
    # Create a Frame widget inside the canvas to contain the actual content
    scrollable_frame = Frame(canvas)

    # Bind the <Configure> event to update the canvas scroll region based on the size of the scrollable_frame
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")  # Update the scroll region to cover the entire content
        )
    )

    # Create a window inside the canvas that will hold the scrollable_frame
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
   
    # Configure the canvas to update the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
   
    # Add a Label inside the scrollable frame to display the formatted reviews
    # Set wraplength to ensure text wraps within the width of the frame
    Label(scrollable_frame, text=print_records, font=("Times", 14), fg = "white", anchor="w", justify=LEFT, wraplength=300).pack(fill=BOTH, expand=True)

    # Pack the canvas to fill the output frame and allow it to expand
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    
    # Pack the scrollbar to the right side of the output frame
    scrollbar.pack(side=RIGHT, fill=Y)

    # Commit changes to the database (no changes are made here, but good practice to include)
    connect1.commit()
    
    # Close the connection to the database
    connect1.close()


# Adjust the grid to center the frame
root.grid_rowconfigure(12, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create the text boxes the info is written in 
author_full_name = Entry (root, width = 30)
author_full_name.grid(row=0, column=1, padx=20, pady=(10,0)) 

movie_name = Entry (root, width = 30)
movie_name.grid(row = 1, column = 1)

rating = Entry (root, width = 30)
rating.grid(row = 2, column = 1)

essay = Text (root, width = 40, height = 10)
essay.grid(row = 3, column = 1, pady = 10, sticky="n")

# Prevent the root window from resizing based on widget size
root.grid_propagate(False)

delete_box = Entry (root, width = 30)
delete_box.grid (row= 8, column=1, pady=5)

# Labels for the text boxes
author_full_name_label = Label (root, text = "Your full name", font = ("Times" , 15, "bold"))
author_full_name_label.grid(row=0,column=0, pady=(10,0))

movie_name_label = Label (root, text="Movie name", font =("Times", 15, "bold"))
movie_name_label.grid(row=1, column=0)

rating_label = Label (root, text="Rating", font =("Times", 15, "bold"))
rating_label.grid(row=2,column=0)

essay_label = Label (root, text = "Insert review ", font =("Times", 15, "bold"))
essay_label.grid(row=3, column=0)

delete_box_label = Label(root, text= "Select review ID", font =("Times", 15, "bold"))
delete_box_label.grid(row=8, column = 0, pady=5)

# Buttons to submit info, query, delete and edit.

submit_button = Button (root, text = "Add review to database",  font =("Times", 15, "bold") , command=submit)
submit_button.grid(row=6, column=0, columnspan=2,pady=10,padx=10,ipadx=100)

query_button = Button (root, text="Show previous reviews", font =("Times", 15, "bold"), command=query)
query_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=105)

delete_button = Button (root, text="Delete review",  font =("Times", 15, "bold"), command=delete)
delete_button.grid (row=10, column=0, columnspan=2,padx=10,pady=10,ipadx=125)

edit_button = Button (root, text="Update review",  font =("Times", 15, "bold"), command= edit)
edit_button.grid(row=11, column=0, columnspan=2, padx=10,pady=10,ipadx=125)

# Commit changes to database and close it
connect1.commit()
connect1.close()

root.mainloop()