import math
from tkinter import *
import turtle
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


def write_log():
    from datetime import datetime
    with open("pomodoro_log.dat", 'a') as logfile:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M\n")
        log_text = f'Study length: {WORK_MIN} minutes. Study Session time: {dt_string}'
        logfile.write(log_text)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global timer
    global reps
    reps = 0
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    action["text"] = "Timer"
    checkmark["text"] = ""
    timing_setup()

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    window.state("normal")
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)
    window.bell()
    global reps
    reps += 1
    if reps % 2 == 0 and reps > 1:
        marks = ""
        for _ in range(math.floor(reps/2)):
            marks += "✔"
        checkmark["text"] = marks
        write_log()

    if reps % 2 == 1:
        action["text"] = "Work"
        action.config(fg=GREEN)
        count_down(WORK_MIN * 60)
    elif reps % 2 == 0 and reps != 8:
        action["text"] = "Break"
        action.config(fg=PINK)
        count_down(SHORT_BREAK_MIN * 60)
    if reps % 8 == 0:
        action["text"] = "Break"
        action.config(fg=RED)
        count_down(LONG_BREAK_MIN * 60)



# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    elif count == 0:
        start_timer()


def timing_setup():
    screen = turtle.Screen()
    screen.setup(10, 10)

    global WORK_MIN
    global LONG_BREAK_MIN
    global SHORT_BREAK_MIN
    try:
        WORK_MIN = int(turtle.textinput("Working Time", "Write working minutes: "))
        SHORT_BREAK_MIN = int(turtle.textinput("Break Time", "Write break minutes: "))
        LONG_BREAK_MIN = int(turtle.textinput("Long Break Time", "Write long break minutes: "))
    except:
        print("Deafault values used")
    finally:
        turtle.bye()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

action = Label(font=(FONT_NAME, 50, "bold"), fg=GREEN, text="TIMER", bg=YELLOW)
action.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png") #para pasarle una imagen al canvas
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)


start = Button(text="Start", font=(FONT_NAME, 10), command=start_timer)
start.grid(column=0, row=2)

reset = Button(text="Reset", font=(FONT_NAME, 10), command=reset_timer)
reset.grid(column=2, row=2)

checkmark = Label(font=(FONT_NAME, 15, "bold"), fg=GREEN)
checkmark.grid(column=1, row=3)


timing_setup()



















window.mainloop()