# state length of numbers found
# reset button for runtime info frame
# finds files all over the system
# proper division of info in textbox
# put more sorts
# loading screen

from Tkinter import *
import timeit

def do_nothing():
    pass

def configure_button(btn, command):
    btn.configure(state=command)

def pop_up(title, message, size, command):
    configure_button(find_btn, DISABLED)
    pop_up = Tk()
    pop_up.protocol("WM_DELETE_WINDOW", do_nothing)

    pop_up.geometry(size)
    pop_up.resizable(0, 0)
    pop_up.wm_title(title)
    content = Label(pop_up, text=message)
    content.pack()
    ok_btn = Button(pop_up, text="Okay", command=lambda: [command, configure_button(find_btn, ACTIVE), pop_up.destroy()])
    ok_btn.pack(side=BOTTOM)

    pop_up.mainloop()

def populate_runtime_frame(info, sorter, cardinality, runtime):
    if sorter == "Insertion":
        info.insert(END, sorter)
        info.insert(END, "\t ")
    else:
        info.insert(END, sorter)
        info.insert(END, "\t   ")
    info.insert(END, cardinality)
    info.insert(END, "\t  ")
    info.insert(END, "{:.8f}".format(float(runtime)))
    info.insert(END, "\n")

#     "{:.8f}".format(float("8.99284722486562e-02"))

def populate_list_frame(frame, cont):
    for widget in frame.winfo_children():
        widget.destroy()

    text = Text(frame, height=10, width=20)
    text_scrollbar = Scrollbar(frame)
    text.pack(side=LEFT, fill=Y)
    text_scrollbar.pack(side=RIGHT, fill=Y)
    text_scrollbar.config(command=text.yview)
    text.config(yscrollcommand=text_scrollbar.set)

    index = 0
    text.insert(END, "Index   |  Number\n")
    for number in cont:
        text.insert(END, "%d\t  " % (index))
        text.insert(END, number)
        text.insert(END, "\n")

        index += 1

    text.config(state=DISABLED)

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[i] < arr[l]:
        largest = l

    if r < n and arr[largest] < arr[r]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]

        heapify(arr, n, largest)

def heap_sort(arr, n):
    for i in range(n, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

def bubble_sort(arr, r):

    for i in range(r):
        for j in range(0, r - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def insertion_sort(arr, l, r):
    for i in range(l, r):
        key = arr[i]

        j = i - 1

        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]

            j -= 1

        arr[j + 1] = key

def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    L = [0] * (n1)
    R = [0] * (n2)

    for i in range(0, n1):
        L[i] = arr[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    i = 0
    j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def merge_sort(arr, l, r):
    if l < r:

        m = (l + (r - 1)) / 2

        merge_sort(arr, l, m)
        merge_sort(arr, m + 1, r)
        merge(arr, l, m, r)

def sort(sorter, cardinality, number_cont):
    if cardinality == "":
        pop_up("Invalid Input", "Please provide size to sort.", "250x50", configure_button(sort_btn, ACTIVE))

    temp_number_cont = []
    for number in number_cont:
        temp_number_cont.append(number)

    if sorter == "Merge":
        start_time = timeit.default_timer()

        merge_sort(temp_number_cont, 0, int(cardinality)-1)

        elapsed_time = timeit.default_timer() - start_time

        populate_runtime_frame(runtime_info, sorter, int(cardinality), elapsed_time)

    elif sorter == "Insertion":
        start_time = timeit.default_timer()

        insertion_sort(temp_number_cont, 0, int(cardinality))

        elapsed_time = timeit.default_timer() - start_time

        populate_runtime_frame(runtime_info, sorter, cardinality, elapsed_time)

    elif sorter == "Bubble":
        start_time = timeit.default_timer()

        bubble_sort(temp_number_cont, int(cardinality))

        elapsed_time = timeit.default_timer() - start_time

        populate_runtime_frame(runtime_info, sorter, cardinality, elapsed_time)

    elif sorter == "Heap":
        start_time = timeit.default_timer()

        heap_sort(temp_number_cont, int(cardinality))

        elapsed_time = timeit.default_timer() - start_time

        populate_runtime_frame(runtime_info, sorter, cardinality, elapsed_time)

    populate_list_frame(text2_frame, temp_number_cont[0:int(cardinality)])

def find_file(number_list, number_cont):
    try:
        with open(number_list, "r") as number_list:
            reader = number_list.read()
            cont = reader.split(" ")

            for number in cont:
                number_cont.append(int(number))
            number_list.close()

            populate_list_frame(text1_frame, number_cont)

            pop_up("Success", "File found successfully. You can now sort.", "250x50", configure_button(sort_btn, ACTIVE))


    except IOError:
        pop_up("File Error", "File does not exist.", "420x70", configure_button(sort_btn, DISABLED))

def int_check(*args):
    letters_only = ""
    for char in cardinality_entry.get():
        try:
            int(char)

        except(ValueError):
            letters_only = letters_only + char

    cardinality.set(cardinality.get().replace(letters_only, ""))

number_cont = []
sorter_list = ["Merge", "Insertion", "Bubble", "Heap"]
runtime_list = []

root = Tk()

# LEFT VAR
left_frame = Frame(root)

configure_frame = Frame(left_frame, borderwidth=1, relief=SUNKEN)
space1_frame = Frame(left_frame, height=20)
runtime_frame = Frame(left_frame)

runtime_info = Text(runtime_frame, height=5, width=36)
runtime_info_scrollbar = Scrollbar(runtime_frame)
runtime_info.insert(END, "Sorter    | Size |   Runtime\n")

number_list_label = Label(configure_frame, text="File Name:", width=20)
cardinality_label = Label(configure_frame, text="Size:", width=20)
sorter_label = Label(configure_frame, text="Sorter:", width=20)

number_list = StringVar()
number_list_entry = Entry(configure_frame, textvariable=number_list)
number_list.set("number_list.txt")

find_btn = Button(configure_frame, command=lambda: find_file(number_list.get(), number_cont), text="FIND", fg="darkgreen")

sorter = StringVar()
sorter.set(sorter_list[0])
sorter_options = OptionMenu(configure_frame, sorter, *sorter_list)

cardinality = StringVar()
cardinality.trace("w", int_check)
cardinality_entry = Entry(configure_frame, textvariable=cardinality)

sort_btn = Button(configure_frame, command=lambda: sort(sorter.get(), cardinality.get(), number_cont), text="SORT", fg="darkgreen")

configure_button(sort_btn, DISABLED)

# SPACE BETWEEN L AND R
space2_frame = Frame(root, width=50)

# RIGHT VAR
right_frame = Frame(root)
title_frame = Frame(right_frame, height=20)
list_frame = Frame(right_frame)
text1_frame = Frame(list_frame)
text2_frame = Frame(list_frame)
number_list_title = Label(title_frame, text="Number List")
space_title = Label(title_frame, text="                          ")
sorted_number_list_title = Label(title_frame, text="Sorted Number List")



# UI
root.title("Number Sorter")
root.geometry("750x200")
root.resizable(0, 0)

# ROOT LEFT FRAME
left_frame.pack(side=LEFT)

# LEFT FRAME - TOP
configure_frame.grid(row=0)
number_list_label.grid(row=0)
cardinality_label.grid(row=1)
sorter_label.grid(row=2)
number_list_entry.grid(row=0, column=1)
cardinality_entry.grid(row=1, column=1)
sorter_options.grid(row=2, column=1)
sorter_options.configure(width=15)
sort_btn.grid(row=2, column=2)
find_btn.grid(row=0, column=2)

# LEFT FRAME - MIDDLE
space1_frame.grid(row=1)

# LEFT FRAME - BOTTOM
runtime_info.pack(side=LEFT, fill=Y)
runtime_info_scrollbar.pack(side=RIGHT, fill=Y)
runtime_info_scrollbar.config(command=runtime_info.yview)
runtime_info.config(yscrollcommand=runtime_info_scrollbar.set)
runtime_frame.grid(row=2)

# SPACE FRAME BETWEEN L AND R
space2_frame.pack(side=LEFT)

# ROOT RIGHT FRAME
right_frame.pack(side=LEFT)

# RIGHT FRAME - TOP
title_frame.pack(side=TOP)
number_list_title.grid(row=0, column=0)
space_title.grid(row=0, column=1)
sorted_number_list_title.grid(row=0, column=2)

# RIGHT FRAME - BOTTOM
list_frame.pack(side=BOTTOM)

# RIGHT FRAME - BOTTOM - LEFT
text1_frame.pack(side=LEFT)
text1_scrollbar = Scrollbar(text1_frame)
text1 = Text(text1_frame, height=10, width=20)
text1_scrollbar.pack(side=RIGHT, fill=Y)
text1.pack(side=LEFT, fill=Y)

text1_scrollbar.config(command=text1.yview)
text1.insert(END, "Index   |  Number\n")
text1.config(yscrollcommand=text1_scrollbar.set, state=DISABLED)

# RIGHT FRAME - BOTTOM - RIGHT
text2_frame.pack(side=LEFT)
text2_scrollbar = Scrollbar(text2_frame)
text2 = Text(text2_frame, height=10, width=20)
text2_scrollbar.pack(side=RIGHT, fill=Y)
text2.pack(side=LEFT, fill=Y)

text2_scrollbar.config(command=text2.yview)
text2.insert(END, "Index   |  Number\n")
text2.config(yscrollcommand=text2_scrollbar.set, state=DISABLED)

root.mainloop()