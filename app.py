#import required library
from tkinter import *
from tkinter import messagebox, ttk
import requests
import json
from PIL import ImageTk, Image

#function to switch between frames
def switch_to_frame(frame):
    frame.tkraise()

#function to switch instructions frame
def instructions():
     switch_to_frame(frame2) 
     
#function to switch entries frame
def entries():
    switch_to_frame(frame3)
    
#function to switch to questions frame
def questions():
    switch_to_frame(frame4)

#root window configuration
root = Tk()
root.title('Triviality')
root.geometry('500x600')

# Frame 1: Start Screen
frame1 = Frame(root)

# Load background image
image = Image.open("bgt.png")
resize_image = image.resize((500,600))
img1 = ImageTk.PhotoImage(resize_image)
img_label = Label(frame1,image=img1)
img_label.place(x=0,y=0)
# Start button
start_btn = Button(frame1, text="let's start",
                   font=('Verdana',12),bg="black",
                   fg="white",command=instructions)
start_btn.place(x=200,y=460)
frame1.place(x=0,y=0, width=500,height=600)

# Frame 2: Instructions
frame2 = Frame(root)
frame2.place(x=0,y=0, width=500,height=600)

# Load background image for instructions frame
image = Image.open("inst.png")
resize_image = image.resize((500,600))
img = ImageTk.PhotoImage(resize_image)
img_label = Label(frame2,image=img)
img_label.place(x=0,y=0)

#load image for logo
image = Image.open("img.png")
resize_image = image.resize((400,80))
img3 = ImageTk.PhotoImage(resize_image)
img_label = Label(frame2,image=img3,bg='#4C2B2A')
img_label.place(x=50,y=420)

# Back button 
button = Button(frame2,text="<",
                command=lambda:switch_to_frame(frame1),
                bg='#A87C7C', fg='white')
button.place(x=20,y=20)

#frame for instructions
inst_frame = Frame(frame2,bg='black')
inst_frame.place(x=70,y=170,width=350,height=200)
in1 = Label(frame2, 
            text="1. First, the user has to enter their name.",
            font=('Roboto',13),bg='black',fg='white')
in1.place(x=100,y=180)
in2 = Label(frame2, text="2. User has to shoose the category. ",
            font=('Roboto',13),bg='black',fg='white')
in2.place(x=100,y=215)
in3 = Label(frame2, text="3. A set of questions appears ",
            font=('Roboto',13),bg='black',fg='white')
in3.place(x=100,y=250)
in4 = Label(frame2, text="4. Read the questions carefully .",
            font=('Roboto',13),bg='black',fg='white')
in4.place(x=100,y=285)
in5 = Label(frame2, text="5. Last but not least, the results appear",
            font=('Roboto',13),bg='black',fg='white')
in5.place(x=100,y=320)

#instruction next button
nxt_btn = Button(frame2, text='NEXT',
                 command=entries,bg='#A87C7C',fg='white')
nxt_btn.place(x=420,y=550)

#switch to frame2
switch_to_frame(frame2)

current_question = 0
score = 0
user_name = ""
selected_category = ""

#requests to fetch categoies 
def fetch_categories():
    api_url = "https://opentdb.com/api_category.php"
    response = requests.get(api_url)
    data = response.json()

    if response.status_code == 200 and data["trivia_categories"]:
        return [category["name"] for category in data["trivia_categories"]]
    else:
        return []

#start quiz
def start_quiz():
    global user_name, selected_category
    user_name = entry_name.get()
    selected_category = category_var.get()

if __name__ == "__main__":
    
    #frame3: entries
    frame3 = Frame(root)
    frame3.place(x=0,y=0,width=500,height=600)
    
    #load background image
    image = Image.open("entry.png")
    resize_image = image.resize((500,600))
    img4 = ImageTk.PhotoImage(resize_image)
    img_label = Label(frame3,image=img4)
    img_label.place(x=0,y=0)
    
    #Back button
    button = Button(frame3,text="<",
                    command=lambda:switch_to_frame(frame2),
                    bg='#A87C7C', fg='white')
    button.place(x=20,y=20)
    
    # User Name Entry
    label_name = Label(frame3, 
                       text="Enter Your Name:",
                       font=('Verdana',12),
                       bg='#3E3232',fg='white')
    label_name.place(x=170,y=150)
    entry_name = Entry(frame3)
    entry_name.place(x=180,y=190)

    # Category Selection
    label_category = Label(frame3,
                           text="Select a Category:",
                           font=('Verdana',12),
                           bg='#3E3232',fg='white')
    label_category.place(x=160,y=240)
    categories = fetch_categories()
    category_var = StringVar(value=categories[0] if categories else "")
    category_combobox = ttk.Combobox(frame3, 
                                     textvariable=category_var, 
                                     values=categories, state="readonly")
    category_combobox.place(x=170,y=280)

    # Start Quiz Button
    start_button = Button(frame3, text="Start Quiz", 
                          command=questions,font=('Verdana',11),
                          fg='white',bg='#503C3C')
    start_button.place(x=200,y=340,width=90,height=30)
    
    #load image for logo
    image = Image.open("img.png")
    resize_image = image.resize((400,80))
    img5 = ImageTk.PhotoImage(resize_image)
    img_label = Label(frame3,image=img5,bg='#4C2B2A')
    img_label.place(x=50,y=500)

    #switch to frame3
    switch_to_frame(frame3)


#function request to fetch question
def fetch_questions():
    global questions, options, correct_answers

    api_url = "https://opentdb.com/api.php"
    params = {
        "amount": 5,  # Adjust the number of questions as needed
        "type": "multiple",  # Multiple-choice questions
    }

    response = requests.get(api_url, params=params)
    data = response.json()
    
    #open a file for dumping the api into file using json
    with open('Ex1.json', 'w') as file:
        json.dump(data,file,indent=6)

    if response.status_code == 200 and data["response_code"] == 0:
        questions = [question["question"] for question in data["results"]]
        options = [question["incorrect_answers"] + [question["correct_answer"]] for question in data["results"]]
        correct_answers = [len(question["incorrect_answers"]) for question in data["results"]]
        load_question()
    else:
        messagebox.showerror("Error", "Failed to fetch questions. Check your internet connection.")

# Function to load the current question
def load_question():
    question_label.config(text=questions[current_question])
    for i in range(4):
        option_buttons[i].config(text=options[current_question][i])

# Function to check the selected answer
def check_answer(selected_option):
    global current_question, score

    # Check if the selected option is the correct answer
    if selected_option == correct_answers[current_question]:
        score += 1
        result_message = f"Correct! Your Score: {score}/{len(questions)}"
    else:
        correct_option = correct_answers[current_question]
        result_message = f"Wrong! The correct answer is option {correct_option + 1}. Your Score: {score}/{len(questions)}"

    messagebox.showinfo("Result", result_message)

    if current_question < len(questions) - 1:
        next_question()
    else:
        show_result()


# Function to move to the next question
def next_question():
    global current_question
    current_question += 1
    load_question()

# Function to reset the game
def reset_game():
    global current_question, score
    current_question = 0
    score = 0
    fetch_questions()
    switch_to_frame(frame3)

# Function to show the result and ask to play again
def show_result():
    result_message = f"Your Score: {score}/{len(questions)}"
    messagebox.showinfo("Quiz Completed", result_message)
    play_again = messagebox.askyesno("Quiz Completed", result_message + "\nDo you want to play again?")
    
    if play_again:
        reset_game()
    else:
        root.destroy()

if __name__ == "__main__":
    
    #frame4: questions
    frame4 = Frame(root)
    frame4.place(x=0,y=0,width=500,height=600)
    
    # Load background image for questions frame
    image = Image.open("quest.png")
    resize_image = image.resize((500,600))
    img2 = ImageTk.PhotoImage(resize_image)
    img_label = Label(frame4,image=img2)
    img_label.place(x=0,y=0)
    
    #going back to entries
    button = Button(frame4,text="<",
                    command=lambda:switch_to_frame(frame3),
                    bg='#A87C7C', fg='white')
    button.place(x=20,y=20)
    # UI Components
    question_label = Label(frame4, text="", wraplength=400,
                           bg="#C3946B",font=('Roboto',12))
    question_label.place(x=60,y=150)
    
    #option answers button
    option_buttons = []
    for i in range(4):
        button = Button(frame4, text="", 
                        command=lambda i=i: check_answer(i),
                        fg='white',bg='black')
        button.place(x=100, y=260 + i * 40)
        option_buttons.append(button)
    
    #next question button
    next_question_button = Button(frame4,
                                  text="Next Question",
                                  command=next_question,
                                  bg='brown',fg='white')
    next_question_button.place(x=200,y=450)

    # Fetch questions from Open Trivia Database
    fetch_questions()
    
    #switch to frame1
    switch_to_frame(frame1)
    
    #start main loop event
    root.mainloop()