from tkinter import *
import tkinter.messagebox
from random import *
from matplotlib import pyplot as plt
import matplotlib
import pymongo
import os

global root1
global top
global quit1
global update_data

class Marquee(Canvas):
    def __init__(self, parent, text, margin=2, borderwidth=1, relief='flat', fps=30):
        Canvas.__init__(self, parent, borderwidth=borderwidth, relief=relief)
        self.fps = fps

        # start by drawing the text off screen, then asking the canvas
        # how much space we need. Use that to compute the initial size
        # of the canvas.
        text = self.create_text(0, -1000, text=text, anchor="w", tags=("text",))
        (x0, y0, x1, y1) = self.bbox("text")
        width = 300
        height = 35
        self.configure(width=width, height=height)
        #(x1 - x0) + (2*margin) + (2*borderwidth)
        #(y1 - y0) + (2*margin) + (2*borderwidth)
        # start the animation
        self.animate()

    def animate(self):
        (x0, y0, x1, y1) = self.bbox("text")
        if x1 < 0 or y0 < 0:
            # everything is off the screen; reset the X
            # to be just past the right margin
            x0 = self.winfo_width()
            y0 = int(self.winfo_height()/2)
            self.coords("text", x0, y0)
        else:
            self.move("text", -1, 0)

        # do again in a few milliseconds
        self.after_id = self.after(int(1000/self.fps), self.animate)

'*******************************************************************************************************************************************'
'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++DataBase Section+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
'*******************************************************************************************************************************************'

def write_into_db(data):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["predictive_cricket"]
    mycol = mydb["users"]
    mycol.insert_one(data)
    tkinter.messagebox.showinfo("Predictive Cricket", "Data successfully stored in the database, Please login:)")

def read_from_db(data):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["predictive_cricket"]
    mycol = mydb["users"]
    temp = mycol.find(data)
    return temp[0]


def check_data(data):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["predictive_cricket"]
    mycol = mydb["users"]
    return mycol.count({'username' : data['username'], 'password' : data['password']})

def check_username(data):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["predictive_cricket"]
    mycol = mydb["users"]
    return mycol.count({'username' : data['username']})


def update_data(result):
    global game_status
    global username
    if result:
        game_status += '1'
    else:
        game_status += '0'
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["predictive_cricket"]
    mycol = mydb["users"]
    mycol.update({'username' : username}, {'$set' : {'game_status' : game_status}})
    tkinter.messagebox.showinfo("Predictive Cricket", "Database updated...")


'==========================================================================================================================================='
'==========================================================================================================================================='
''' Function for erasing the initial content of new game window'''
def destroy():
    #target.destroy()
    ball_label.destroy()
    run_label.destroy()
    wicket_label.destroy()
    difficulty.destroy()
    commentry.destroy()
    scored.destroy()
    next_ball.destroy()
    R1.destroy()
    R2.destroy()
    R3.destroy()

''' Function to erase the prediction elements
    for showing the results of the game'''
def destroy_prediction():
    prediction.destroy()
    prediction_data.destroy()
    ball_result.destroy()

'Function for computing the result of every single ball'
def current_result():
    destroy_prediction()
    global top
    global run
    global ball
    global wicket
    global commentry
    global scored
    global next_ball
    global level
    global target
    global target_label
    global ball_label
    global run_label
    global wicket_label
    global prediction
    global prediction_data
    global ball_result
    global result

    def end_match():
        global update_data
        target_label.destroy()
        ball_label.destroy()
        run_label.destroy()
        wicket_label.destroy()
        prediction.destroy()
        prediction_data.destroy()
        ball_result.destroy()
        commentry.destroy()
        scored.destroy()
        final.destroy()
        back.destroy()
        update_data(result)
        game_window()



    good_wishes=["Remarkable Shot!!","Oh my goodness that's really awesome shot",\
                 "There was no chance for any fielder","Classical shot",\
                 "Finds the boundary easily","Great playing:)"]
    try:
        my_run = int(prediction_data.get())
    except:
        if level == 1:
            my_run = randint(1,50)
        elif level == 2:
            my_run = randint(1,100)
        else:
            my_run = randint(1,200)

    if level == 1:
        comp_run = randint(1,50)
    elif level == 2:
        comp_run = randint(1,100)
    else:
        comp_run = randint(1,200)

    if abs(my_run-comp_run)<=5:
        run+=6
        ball-=1
        score_message="It's Maximum 6 !!!"
        comment=choice(good_wishes)
    if abs(my_run-comp_run)>5 and abs(my_run-comp_run)<=10:
        run+=4
        ball-=1
        score_message="It's boundary 4 ..."
        comment=choice(good_wishes)
    if abs(my_run-comp_run)>10 and abs(my_run-comp_run)<=15:
        run+=3
        ball-=1
        score_message="That's 3 runs"
        comment="## sparkle running ##"
    if abs(my_run-comp_run)>15 and abs(my_run-comp_run)<=20:
        run+=2
        ball-=1
        score_message="It's double 2 runs"
        comment="Good running between the wicket"
    if abs(my_run-comp_run)>20 and abs(my_run-comp_run)<=25:
        run+=1
        ball-=1
        score_message="It's single, 1 run"
        comment="@ quick run:)"
    if abs(my_run-comp_run)>25 and abs(my_run-comp_run)<=30:
        ball-=1
        score_message="Thats dot ball"
        comment="Be careful next time"
    if abs(my_run-comp_run)>30:
        wicket-=1
        ball-=1
        score_message="That's wicket, super bowling"
        comment="Very poor prediction"

    commentry = Label(top, text = comment,bg="green",fg="white",width=40, font=('bold', 12))
    commentry.place(x = 62,y = 250)

    scored = Label(top, text = score_message,bg="green",fg="white",width=30, font=('bold', 12))
    scored.place(x = 105,y = 280)

    if wicket <= 0:
        final = Label(top, text = "All Out, Defeated by {} runs".format(target-run),
                      bg="red",fg="white",width=30,font=("bold",12))
        final.place(x = 80,y = 310)

        back = Button(top, text = "Go Back",bg="black",fg="white", font=('bold', 12),
                      width=30,command=end_match)
        back.place(x = 110,y = 350)
    elif ball <= 0:
        if target <= run:
            result = True
            final = Label(top, text = "YES !!! You won by {} wickets".format(wicket),
                          bg="red",fg="white",width=30,font=("bold",12))
            final.place(x = 110,y = 310)
            back = Button(top, text = "Go Back",bg="black",fg="white",width=30,
                          command=end_match)
            back.place(x = 120,y = 350)
        else:
            final = Label(top, text = "No balls left, Defeated by {} runs".format(target-run),
                          bg="red",fg="white",width=30,font=("bold",12))
            final.place(x = 110,y = 310)
            back = Button(top, text = "Go Back",bg="black",fg="white",width=30, font=('bold', 12),command=end_match)
            back.place(x = 110,y = 350)

    elif target <= run:
        result = True
        final = Label(top, text = "YES !!! You won by {} wickets".format(wicket),
                      bg="red",fg="white",width=30,font=("bold",12))
        final.place(x = 100,y = 310)

        back = Button(top, text = "Go Back",bg="black",fg="white",font=('bold', 12),
                      width=30,command=end_match)
        back.place(x = 110,y = 350)

    else:
        next_ball = Button(top, text = "Press for next ball",bg="black",
                           fg="white",width=28,command=gameloop, font=('bold', 12))
        next_ball.place(x = 110,y = 310)

'Main game loop for playing the game'
def gameloop():
    global result
    global top
    global target_label
    global ball_label
    global run_label
    global wicket_label
    global prediction
    global prediction_data
    global flag
    global ball_result

    result = False #flag for tracking match result
    temp = {1:"1 - 50",2:"1 - 100",3:"1 - 200"}

    if flag == False:
        destroy()

    ball_label = Label(top, text = "Balls left : "+str(ball),
                       bg="red",fg="white",width=15,font=("bold",12))
    ball_label.place(x = 280,y = 150)

    wicket_label = Label(top, text = "Wicket : "+str(wicket),
                         bg="red",fg="white",width=15,font=("bold",12))
    wicket_label.place(x = 70,y = 180)

    run_label = Label(top, text = "Run : "+str(run),
                      bg="purple",fg="white",width=15,font=("bold",12))
    run_label.place(x = 280,y = 180)

    prediction = Label(top, text = "Predict between "+temp[level],
                       bg="#c9d91e",fg="black",width=25,font=("bold",12))
    prediction.place(x = 70,y = 210)

    prediction_data = Entry(top,width=10,font=("bold",12))
    prediction_data.place(x = 325,y = 210)

    ball_result = Button(top, text = "Check Result",bg="brown",fg="white",
                         font=("bold",12),width=12,command=current_result)
    ball_result.place(x = 190,y = 240)

    if flag:
        target_label = Label(top, text = "Target : "+str(target),
                             bg="purple",fg="white",width=15, font=("bold",12))
        target_label.place(x = 70,y = 150)
        flag=False

'Function to set up initial stuffs'
def start_game():
    global ball
    global run
    global wicket
    global flag

    run = 0
    wicket = 10
    ball = 6 * over
    flag = True

    gameloop()


'Function for destroying previous content of the window'
def destroy_data():
    global target
    global over
    global level
    try:
        if abs(int(over_entry.get()))!=0:
            over = abs(int(over_entry.get()))
        else:
            over = 1
    except:
        over = 1

    try:
        if abs(int(target_entry.get()))!=0:
            target = abs(int(target_entry.get()))
        else:
            if over == 1:
                target = 10
            elif ober < 5:
                target = 30
            else:
                target = 50
    except:
        target = 10

    level = radio.get()

    info.destroy()
    over_label.destroy()
    over_entry.destroy()
    target_label.destroy()
    target_entry.destroy()
    confirm.destroy()
    difficulty.destroy()
    R1.destroy()
    R2.destroy()
    R3.destroy()

    start_game()

'Function to create new game'
def new_game_func():
    global top

    # root1 = Toplevel()
    # root1.geometry("400x400+600+100")
    # root1.configure(bg="cyan")
    # root1.title("Game window")

    global new_game
    global performance
    global rule
    global back0
    global quit2

    global info
    global over_label
    global over_entry
    global target_label
    global target_entry
    global confirm
    global radio
    global difficulty
    global R1
    global R2
    global R3

    new_game.destroy()
    performance.destroy()
    rule.destroy()
    back0.destroy()
    quit2.destroy()

    # title = Label(top, text = "PREDICTIVE CRICKET",width=20,font=("bold",20),
    #               bg="yellow")
    # title.place(x = 35,y = 20)

    # message = Marquee(top, text = "(: Fill out the details for continue :)",
    #                   borderwidth=2, relief="sunken")
    # message.place(x = 85,y = 70)

    info = Label(top, text = "Enter target,number of overs and difficulty level",
                 bg="#5e3c05",font=("bold",14),fg="white", width=40)
    info.place(x = 25,y = 150)

    over_label = Label(top, text = "Overs",bg='#e3102c',fg="white",width=15,font=("bold",12))
    over_label.place(x = 85,y = 190)

    over_entry = Entry(top,font=("bold",12))
    over_entry.place(x = 230, y = 190)

    target_label = Label(top, text = "Target",bg="#e3102c",fg="white",width=15,font=("bold",12))
    target_label.place(x = 85,y = 220)

    target_entry = Entry(top,font=("bold",12))
    target_entry.place(x = 230, y = 220)

    difficulty = Label(top, text = "Difficulty level",bg="#2712e0",fg="white",width=20,font=("bold",12))
    difficulty.place(x = 145,y = 270)

    radio = IntVar()
    radio.set(1)

    R1 = Radiobutton(top, text="EASY", variable=radio, value=1,bg="#d6679a", width = 10, fg = '#f5f7f5')
    R1.place(x=70,y=310)

    R2 = Radiobutton(top, text="MEDIUM", variable=radio, value=2,bg="#992c5e",  width = 10, fg = '#f5f7f5')
    R2.place(x=190,y=310)

    R3 = Radiobutton(top, text="HARD", variable=radio, value=3,bg="#570a2d",  width = 10, fg = '#f5f7f5')
    R3.place(x=310,y=310)

    confirm = Button(top, text = "Continue",bg="black",fg="white",bd=5,width=15,
                     command=destroy_data)
    confirm.place(x = 175,y = 350)

'================================================================================================================================================='
'================================================================================================================================================='

'Function for showing game rules window'
def rule1():
    root3 = Toplevel()
    root3.geometry("500x500+530+150")
    root3.configure(bg="#613175")
    root3.title("Rule window")

    title = Label(root3, text = "PREDICTIVE CRICKET",width=25,
                  font=("bold",20),bg="#dea30d")
    title.place(x = 45,y = 20)

    message = Marquee(root3, text = "(: Game Rules      !!!      Game Rules      !!!        Game Rules  :)",borderwidth=2,
                      relief="sunken")
    message.place(x = 95,y = 75)

    rule1 = Label(root3, text = "1. You have predict a number within a range",
                  width=40,font=("bold",12),bg="#90f78b")
    rule1.place(x = 65,y = 140)

    rule2 = Label(root3, text = "2. Computer will also predict a number",
                  width=40,font=("bold",12),bg="#77e371")
    rule2.place(x = 65,y = 170)

    rule3 = Label(root3, text = "3. If the difference between 1 & 2 will be -",
                  width=40,font=("bold",12),bg="#63c75d")
    rule3.place(x = 65,y = 200)

    rule4 = Label(root3, text = "4. In between 0-5, then you hit 6",
                  width=40,font=("bold",12),bg="#49a644")
    rule4.place(x = 65,y = 230)

    rule5 = Label(root3, text = "5. In between 6-10, then you hit 4",
                  width=40,font=("bold",12),bg="#3f873b")
    rule5.place(x = 65,y = 260)

    rule6 = Label(root3, text = "6. In between 11-15, then you hit 3",
                  width=40,font=("bold",12),bg="#32692f")
    rule6.place(x = 65,y = 290)

    rule7 = Label(root3, text = "7. In between 16-20, then you hit 2",
                  width=40,font=("bold",12),bg="#224f20")
    rule7.place(x = 65,y = 320)

    rule8 = Label(root3, text = "8. In between 21-25, then you hit 1",
                  width=40,font=("bold",12),bg="#163b14")
    rule8.place(x = 65,y = 350)

    rule9 = Label(root3, text = "9. In between 26-30, then it's dot ball",
                  width=40,font=("bold",12),bg="#084704")
    rule9.place(x = 65,y = 380)

    rule10 = Label(root3, text = "10. more than 30, then it's your wicket",
                   width=40,font=("bold",12),bg="#10380c")
    rule10.place(x = 65,y = 410)

    back = Button(root3, text = "BACK",width=15,bd=5,font=("bold",10),
                  bg="black",fg="white",command=root3.destroy)
    back.place(x = 170,y = 450)

'================================================================================================================================================='
'================================================================================================================================================='

'Function to store the high score'
def graph():
    global game_status

    # Creating dataset
    Game_Performance = ['Winning', 'Loosing']
    data = [list(game_status).count('1'),list(game_status).count('0')]
    explode = [0.1,0]
    colors = ['#2cdb12', '#f5120a']

    def move_figure(f, x, y):
        """Move figure's upper left corner to pixel (x, y)"""
        backend = matplotlib.get_backend()
        if backend == 'TkAgg':
            f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
        elif backend == 'WXAgg':
            f.canvas.manager.window.SetPosition((x, y))
        else:
            # This works for QT and GTK
            # You can also use window.setGeometry
            f.canvas.manager.window.move(x, y)

    f, ax = plt.subplots()
    move_figure(f, 450, 150)

    plt.title('Game Playing Status')
    plt.pie(data, explode=explode, labels=Game_Performance, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.show()




'================================================================================================================================================='
'================================================================================================================================================='

global login_func
def login_func():
    root5 = Toplevel()
    root5.geometry("405x300+580+270")
    root5.configure(bg="#052b03")
    root5.title("Login Window")

    title = Label(root5, text = "!!!Login Page!!!",width=30,
                  font=("bold",15),bg="#e62542")
    title.place(x = 35,y = 20)

    message = Marquee(root5, text = "PLEASE ENTER YOUR USER NAME AND PASSWORD FOR REGISTRATION PURPOSE, THANK YOU:)",borderwidth=1,
                      relief="sunken")
    message.place(x = 50,y = 60)

    username_label = Label(root5, text = "Username",bg="#4a4f59",fg="white",width=15,font = ("italic",12))
    username_label.place(x = 30,y = 120)

    username_entry = Entry(root5,font=('bold',12),bg="#f7baef")
    username_entry.place(x = 180, y = 120)

    pass_label = Label(root5, text = "Password",bg="#4a4f59",fg="white",width=15,font = ("italic",12))
    pass_label.place(x = 30,y = 150)

    pass_entry = Entry(root5,font=('bold',12),show='*',bg="#f7baef")
    pass_entry.place(x = 180, y = 150)

    checkvar1 = IntVar()
    check = Checkbutton(root5, text = "I am not a robot *", variable = checkvar1, onvalue = 1, offvalue = 0, width = 20,bg="#78340c",font=('bold',12))
    check.place(x = 105, y = 180)

    def onLeave(event):
        submit.config(bg='#2767e6')

    def onEnter(event):
        submit.config(bg='#f06413')

    def login_verification():
        global game_status
        global username
        data ={}
        data['username'] = username_entry.get()
        data['password'] = pass_entry.get()
        if check_data(data):
            print("logged in succesfully:)")
            root5.destroy()
            game_status = read_from_db(data)['game_status']
            username = read_from_db(data)['username']
            game_window()
        else:
            tkinter.messagebox.showerror("Predictive Cricket", "User not registered yet:(")


    submit = Button(root5, text = "Login",width=20,bd=5,font=("bold",13),
                  bg="black",fg="white",command=login_verification)
    submit.place(x = 110,y = 220)
    submit.bind('<Leave>', onLeave)
    submit.bind('<Enter>', onEnter)

global register_func
def register_func():
    root4 = Toplevel()
    root4.geometry("405x300+580+270")
    root4.configure(bg="#1c2a40")
    root4.title("Register window")

    title = Label(root4, text = "!!!Register Page!!!",width=30,
                  font=("bold",15),bg="#7f8c07")
    title.place(x = 35,y = 20)

    message = Marquee(root4, text = "PLEASE ENTER YOUR USER NAME AND PASSWORD FOR REGISTRATION PURPOSE, THANK YOU:)",borderwidth=1,
                      relief="sunken")
    message.place(x = 50,y = 60)

    username_label = Label(root4, text = "Username",bg="brown",fg="white",width=15,font = ("italic",12))
    username_label.place(x = 30,y = 120)

    username_entry = Entry(root4,font=('bold',12),bg='#72ed8d')
    username_entry.place(x = 180, y = 120)

    pass_label = Label(root4, text = "Password",bg="brown",fg="white",width=15,font = ("italic",12))
    pass_label.place(x = 30,y = 150)

    pass_entry = Entry(root4,font=('bold',12),show='*',bg='#72ed8d')
    pass_entry.place(x = 180, y = 150)

    cpass_label = Label(root4, text = "Confirm Password",bg="brown",fg="white",width=15,font = ("italic",12))
    cpass_label.place(x = 30,y = 180)

    cpass_entry = Entry(root4,font=('bold',12), show='*',bg='#72ed8d')
    cpass_entry.place(x = 180, y = 180)

    def onLeave(event):
        submit.config(bg='#910fa8')

    def onEnter(event):
        submit.config(bg='#f06413')

    def register_verification():
        if pass_entry.get() != cpass_entry.get():
            tkinter.messagebox.showerror("Predictive Cricket", "Password didn't matched in confirm input, Please try again")
        elif check_username({'username' : username_entry.get()}):
            tkinter.messagebox.showwarning("Predictive Cricket", "Username already exist, Please try something else!!")
        else:
            data ={}
            data['username'] = username_entry.get()
            data['password'] = pass_entry.get()
            data['game_status'] = ''
            write_into_db(data)
            root4.destroy()

    submit = Button(root4, text = "Register",width=20,bd=5,font=("bold",13),
                  bg="black",fg="white",command=register_verification)
    submit.place(x = 110,y = 220)
    submit.bind('<Leave>', onLeave)
    submit.bind('<Enter>', onEnter)

global about_func
def about_func():
    def onLeavequit(event):
        back.config(bg='#910fa8')

    def onEnterquit(event):
        back.config(bg='#f06413')
    root6 = Toplevel()
    root6.geometry("400x400+582+210")
    root6.configure(bg="purple")
    root6.title("Rule window")

    temp = PhotoImage(file = "image//5.png")
    Label(root6, image = temp).place(x=0,y=0)

    title = Label(root6, text = "PREDICTIVE CRICKET",width=20,
                  font=("bold",20),bg="yellow")
    title.place(x = 35,y = 20)

    message = Marquee(root6, text = "(: About the core developer of Predictive Cricket :)",borderwidth=2,
                      relief="sunken")
    message.place(x = 45,y = 80)

    poonam = Label(root6, text = "1. Poonam Kumari : Frontend developer",
                  width=40,font=("bold",9),bg="#37ad4b", fg = 'yellow')
    poonam.place(x = 55,y = 150)

    rohit = Label(root6, text = "2. Rohit Prasad : Backend developer",
                  width=40,font=("bold",9),bg="#1bab34", fg = 'yellow')
    rohit.place(x = 55,y = 180)

    ritesh = Label(root6, text = "3. Ritesh Vohra : Database management",
                  width=40,font=("bold",9),bg="#208030", fg = 'yellow')
    ritesh.place(x = 55,y = 210)

    shrish = Label(root6, text = "4. Shrish : Testing and bug fixer",
                  width=40,font=("bold",9),bg="#094d14", fg = 'yellow')
    shrish.place(x = 55,y = 240)

    back = Button(root6, text = "Back",width=20,bd=8,font=("bold",12),
              bg="#0717f5",fg="white",command=root6.destroy)
    back.place(x = 95,y = 280)
    back.bind('<Leave>', onLeavequit)
    back.bind('<Enter>', onEnterquit)

'*************************************************************************************************************************************************'
'*********************************************************Game window after login*****************************************************************'
'*************************************************************************************************************************************************'
def game_window():
    global top
    global quit1
    global register
    global login
    global about
    global new_game
    global performance
    global rule
    global back0
    global quit2
    register.destroy()
    login.destroy()
    about.destroy()
    quit1.destroy()

    def onLeavenew_game1(event):
        new_game.config(bg='#910fa8')

    def onEnternew_game1(event):
        new_game.config(bg='#12eb07')

    def onLeaveperformance(event):
        performance.config(bg='#6e140f')

    def onEnterperformance(event):
        performance.config(bg='#bd6022')

    def onLeaverule(event):
        rule.config(bg='#034f37')

    def onEnterrule(event):
        rule.config(bg='#010008')

    def onLeavequit2(event):
        quit2.config(bg='#3e248f')

    def onEnterquit2(event):
        quit2.config(bg='#e09cf0')

    def onLeaveback0(event):
        back0.config(bg='#871248')

    def onEnterback0(event):
        back0.config(bg='#b5720e')

    def quit_window():
        l = tkinter.messagebox.askyesno("Predictive Cricket", "Do you really want to quit ?")
        if l > 0:
            top.destroy()
        else:
            pass

    def destroy_game_window():
        top.destroy()
        main()

    def quit_window():
        l = tkinter.messagebox.askyesno("Predictive Cricket", "Do you really want to quit ?")
        if l > 0:
            top.destroy()
        else:
            pass




    new_game = Button(top, text = "Start New Game!",width=20,bd=10,font=("bold",12),
                      bg="red",fg="white",command=new_game_func)
    new_game.place(x = 140,y = 150)
    new_game.bind('<Leave>', onLeavenew_game1)
    new_game.bind('<Enter>', onEnternew_game1)

    performance = Button(top, text = "Performance graph",width=20,bd=10,font=("bold",12),
                   bg="green",fg="white",command=graph)
    performance.place(x = 140,y = 210)
    performance.bind('<Leave>', onLeaveperformance)
    performance.bind('<Enter>', onEnterperformance)

    rule = Button(top, text = "Game Rules",width=20,bd=10,font=("bold",12),
                  bg="red",fg="white",command=rule1)
    rule.place(x = 140,y = 270)
    rule.bind('<Leave>', onLeaverule)
    rule.bind('<Enter>', onEnterrule)

    back0 = Button(top, text = "Back",width=20,bd=10,font=("bold",12),
                  bg='#07bade',fg="white",command=destroy_game_window)
    back0.place(x = 140,y = 330)
    back0.bind('<Leave>', onLeaveback0)
    back0.bind('<Enter>', onEnterback0)

    quit2 = Button(top, text = "Quit",width=20,bd=10,font=("bold",12),
                  bg="#034769",fg="white",command=quit_window)
    quit2.place(x = 140,y = 390)
    quit2.bind('<Leave>', onLeavequit2)
    quit2.bind('<Enter>', onEnterquit2)







'*************************************************************************************************************************************************'
'*********************************************************Driver Code starts here*****************************************************************'
'*************************************************************************************************************************************************'
def main():
    global top
    global login_func
    global register_func
    global about_func
    global about
    global register
    global login
    global quit1
    def onLeavequit(event):
        quit1.config(bg='#910fa8')

    def onEnterquit(event):
        quit1.config(bg='#12eb07')

    def onLeaveabout(event):
        about.config(bg='#6e140f')

    def onEnterabout(event):
        about.config(bg='#bd6022')

    def onLeaveregister(event):
        register.config(bg='#034f37')

    def onEnterregister(event):
        register.config(bg='#010008')

    def onLeavelogin(event):
        login.config(bg='#3e248f')

    def onEnterlogin(event):
        login.config(bg='#e09cf0')

    def quit_window():
        l = tkinter.messagebox.askyesno("Predictive Cricket", "Do you really want to quit ?")
        if l > 0:
            top.destroy()
        else:
            pass

    top = Tk()
    top.geometry("500x500+530+150")
    top.configure(bg="orange")
    top.title("Main window")


    temp = PhotoImage(file = "image//3.png")
    Label(top, image = temp).place(x=0,y=0)

    title = Label(top, text = "PREDICTIVE CRICKET",width=20,font=("bold",25),bg="#ed9613")
    title.place(x = 55,y = 35)

    message = Marquee(top, text = "!!! Welcome all :) It's not only the game! \
                    but it's also gonna check your ability to tackle computer. !!!",\
                    borderwidth=2, relief="sunken")
    message.place(x = 90,y = 90)

    login = Button(top, text = "Login",width=20,bd=8,font=("bold",12),
                bg="brown",fg="white",command=login_func)
    login.place(x = 50,y = 190)
    login.bind('<Leave>', onLeavelogin)
    login.bind('<Enter>', onEnterlogin)

    register = Button(top, text = "Register",width=20,bd=8,font=("bold",12),
                bg="green",fg="white",command=register_func)
    register.place(x = 250,y = 190)
    register.bind('<Leave>', onLeaveregister)
    register.bind('<Enter>', onEnterregister)

    about = Button(top, text = "About",width=20,bd=8,font=("bold",12),
                bg="#8f118d",fg="white",command=about_func)
    about.place(x = 150,y = 260)
    about.bind('<Leave>', onLeaveabout)
    about.bind('<Enter>', onEnterabout)

    quit1 = Button(top, text = "Quit",width=20,bd=8,font=("bold",12),
                bg="red",fg="white",command=quit_window)
    quit1.place(x = 150,y = 320)
    quit1.bind('<Leave>', onLeavequit)
    quit1.bind('<Enter>', onEnterquit)

    top.mainloop()

main()
'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Code End~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
