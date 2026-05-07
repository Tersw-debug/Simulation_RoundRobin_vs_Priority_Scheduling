import tkinter as tk
from tkinter import messagebox
import customtkinter as tkk
from collections import deque

class Process:
    def __init__(self, pid: int, arrival: int, burst: int, priority:int = 0, quantum: int = 0):
        self.id = pid
        self.burst = burst
        self.remaining = burst
        self.start = None
        self.arrival = arrival
        self.priority = priority
        self.completion = 0
        self.quantum = quantum
        


def round_robin(processes, quantum):
    time = 0
    n = len(processes)
    queue = deque()
    in_queue = [False] * n
    completed = 0
    time_line = []

    while completed < n :
        for i, proc in enumerate(processes):
            if proc.arrival <= time and not in_queue[i] and proc.remaining > 0:
                queue.append(i)
                in_queue[i] = True
        
        if not queue: # if the queue is empty then add 1 more second
            time_line.append(("Idle", time, time + 1))
            time += 1
            continue

        i = queue.popleft()
        p = processes[i]

        if p.start is None:   # in this second of starting the process we take the
            p.start = time    # time from the algorithm 
        exec_time = min(quantum, p.remaining) # Here we have two cases if the
        time_line.append((p.id , time, (time+exec_time) ))
        time += exec_time    # quantum time is bigger than remaining time of the
        p.remaining -= exec_time # process it then it return again to the queue if not
                             #then the process burst and ends
        
        for j, proc in enumerate(processes):
            if proc.arrival <= time and not in_queue[j] and proc.remaining > 0:
                queue.append(j)
                in_queue[j] = True
        if p.remaining > 0:
            queue.append(i)
        else:
            p.completion = time
            completed += 1
    return processes, time_line
        

def prioity_scheduling(processes):
    time = 0
    completed = 0
    n = len(processes)
    done = [False] * n
    time_line = []

    while completed < n:
        best = float('inf')
        position = -1
        for i, p in enumerate(processes):
            if not done[i] and p.arrival <= time:
                if p.priority < best:
                    best = p.priority
                    position = i

        if position == -1:
            time_line.append(("Idle", time, time + 1))
            time +=1
            continue

        p = processes[position]
        if p.start is None:
            p.start = time
        
        time_line.append((p.id, time, time+p.burst))
        
        time += p.burst
        p.completion = time
        done[position] = True
        completed += 1
    return processes, time_line


def calculate_metrcies(processes):
    result = []
    total_wt = total_tat = total_rt = 0

    for p in processes:
        turn_around_time = p.completion - p.arrival
        waiting_time = turn_around_time - p.burst
        response_time = p.start - p.arrival

        total_wt += waiting_time
        total_tat += turn_around_time
        total_rt += response_time

        result.append((p.id, turn_around_time, waiting_time, response_time))
    
    n = len(processes)
    avg = (total_tat/n, total_wt/n, total_rt/n)
    return result, avg


# GUI
class APP:
    def __init__(self, root):

        root.title("Scheduling Comparison")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        self.main_frame = tkk.CTkFrame(root)
        self.main_frame.grid(row=0, column=0 ,sticky='nsew')
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.input_frame = tkk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=0, column=0, sticky="nsew")
        self.input_frame.grid_rowconfigure(0, weight=0)
        self.input_frame.grid_rowconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)
        
        self.result_frame = tkk.CTkScrollableFrame(self.main_frame, height=800)
        self.result_frame.grid_rowconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(1, weight=0) 
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_columnconfigure(1, weight=1)

        pad_buttons = {"padx": 5, "pady": 5}
        pad = {"padx": 5, "pady": 5}
        self.entries_padding = {"padx": 10, "pady": 10}
        self.buttons_padding = {"padx": 10, "pady": 10}
        self.frame_of_buttons_padding = {"padx": 10, "pady": 10}
        self.my_font_menu_buttons = tkk.CTkFont(family="Arial", size=16, weight="normal")
        self.my_font = tkk.CTkFont(family="Arial", size=18, weight="normal")
        self.my_font_label = tkk.CTkFont(family="Arial", size=20, weight="normal")
        self.my_font_label_main = tkk.CTkFont(family="Arial", size=22, weight="normal")
        self.count_process_round_robin = ""
        self.count_process_priority = ""
        self.arr_p_round_robin = []
        self.arr_p_priority = []

        self.entries = []

        # -----------Menu Bar--------------
        self.menu_bar = tkk.CTkFrame(self.input_frame, width=100)
        self.menu_bar.grid(row=0, column=0, columnspan=2 ,sticky="we")

        self.load_button_case1 = tkk.CTkButton(self.menu_bar, text="Load Case A", fg_color="black", font=self.my_font_menu_buttons, command=self.load_case_a)
        self.load_button_case1.grid(row=0, column=0, **pad_buttons)

        self.load_button_case2 = tkk.CTkButton(self.menu_bar, text="Load Case B", fg_color="black", font=self.my_font_menu_buttons, command=self.load_case_b)
        self.load_button_case2.grid(row=0, column=1, **pad_buttons)

        self.load_button_case3 = tkk.CTkButton(self.menu_bar, text="Load Case C", fg_color="black", font=self.my_font_menu_buttons, command=self.load_case_c)
        self.load_button_case3.grid(row=0, column=2, **pad_buttons)

        self.load_button_case4 = tkk.CTkButton(self.menu_bar, text="Load Case D", fg_color="black", font=self.my_font_menu_buttons, command=self.load_case_d)
        self.load_button_case4.grid(row=0, column=3, **pad_buttons)

        self.load_button_case5 = tkk.CTkButton(self.menu_bar, text="Load Case E", fg_color="black", font=self.my_font_menu_buttons)
        self.load_button_case5.grid(row=0, column=4, **pad_buttons)


        # -----------Left Frame-----------
        self.left_frame = tkk.CTkFrame(self.input_frame)
        self.left_frame.grid(row=1, column=0, sticky="nsew")


        self.left_frame_label = tkk.CTkLabel(self.left_frame, text="Priority Scheduling", font=self.my_font_label_main)
        self.left_frame_label.grid(row=0, columnspan=2)

        self.left_frame_label_entry1 = tkk.CTkLabel(self.left_frame, text="Process ID", font=self.my_font_label)
        self.left_frame_label_entry1.grid(row=1, column=0)
        self.left_frame_entry1 = tkk.CTkEntry(self.left_frame, font=self.my_font)
        self.left_frame_entry1.grid(row=1, column=1, sticky="nsew", **self.entries_padding)

        self.left_frame_label_entry2 = tkk.CTkLabel(self.left_frame, text="Process arrival", font=self.my_font_label)
        self.left_frame_label_entry2.grid(row=2 , column=0)
        self.left_frame_entry2 = tkk.CTkEntry(self.left_frame, font=self.my_font)
        self.left_frame_entry2.grid(row=2, column=1, sticky="nsew", **self.entries_padding)

        self.left_frame_label_entry3 = tkk.CTkLabel(self.left_frame, text="Process burst", font=self.my_font_label)
        self.left_frame_label_entry3.grid(row=3, column=0)
        self.left_frame_entry3 = tkk.CTkEntry(self.left_frame, font=self.my_font)
        self.left_frame_entry3.grid(row=3, column=1, sticky="nsew", **self.entries_padding)

        self.left_frame_label_entry4 = tkk.CTkLabel(self.left_frame, text="Process Priority", font=self.my_font_label)
        self.left_frame_label_entry4.grid(row=4, column=0)
        self.left_frame_entry4 = tkk.CTkEntry(self.left_frame, font=self.my_font)
        self.left_frame_entry4.grid(row=4, column=1, sticky="nsew", **self.entries_padding)

        # -------------left frame of Buttons-------------
        self.left_frame_frame_buttons = tkk.CTkFrame(self.left_frame)
        self.left_frame_frame_buttons.grid(row=5, column=1, sticky="nsew", **self.frame_of_buttons_padding)
        self.left_frame_frame_buttons.grid_columnconfigure((0, 1, 2), weight=1)
        self.left_frame_frame_buttons.grid_rowconfigure(0, weight=1)

        self.left_frame_add_process = tkk.CTkButton(self.left_frame_frame_buttons, text="Add Process", font=self.my_font, command=self.add_process_priority)
        self.left_frame_add_process.grid(row=0, column=0, sticky="nsew", **self.buttons_padding)

        self.left_frame_reset_process = tkk.CTkButton(self.left_frame_frame_buttons, text="Reset Processes", font=self.my_font, fg_color="red", command=self.reset_process_priority)
        self.left_frame_reset_process.grid(row=0, column=1, sticky="nsew", **self.buttons_padding)

        self.left_frame_load_process = tkk.CTkButton(self.left_frame_frame_buttons, text="Load Process", font=self.my_font, fg_color="black", command=self.load_process_priority)
        self.left_frame_load_process.grid(row=0, column=2, sticky="nsew", **self.buttons_padding)


        self.left_frame_count_process = tkk.CTkLabel(self.left_frame, text="Prcoess Number: 0", font=self.my_font_label)
        self.left_frame_count_process.grid(row=5, column=0, **pad)

        # ---------Right Frame--------
        self.right_frame = tkk.CTkFrame(self.input_frame)
        self.right_frame.grid(row=1, column=1, sticky="nsew")
        self.right_frame_label = tkk.CTkLabel(self.right_frame, text="Round Robin", font=self.my_font_label_main)
        self.right_frame_label.grid(row=0, columnspan=2)

        
        self.right_frame_label_entry1 = tkk.CTkLabel(self.right_frame, text="Process ID", font=self.my_font_label)
        self.right_frame_label_entry1.grid(row=1, column=0)
        self.right_frame_entry1 = tkk.CTkEntry(self.right_frame, font=self.my_font)
        self.right_frame_entry1.grid(row=1, column=1, sticky="nsew", **self.entries_padding)

        self.right_frame_label_entry2 = tkk.CTkLabel(self.right_frame, text="Process arrival", font=self.my_font_label)
        self.right_frame_label_entry2.grid(row=2 , column=0)
        self.right_frame_entry2 = tkk.CTkEntry(self.right_frame, font=self.my_font)
        self.right_frame_entry2.grid(row=2, column=1, sticky="nsew", **self.entries_padding)

        self.right_frame_label_entry3 = tkk.CTkLabel(self.right_frame, text="Process burst", font=self.my_font_label)
        self.right_frame_label_entry3.grid(row=3, column=0)
        self.right_frame_entry3 = tkk.CTkEntry(self.right_frame, font=self.my_font)
        self.right_frame_entry3.grid(row=3, column=1, sticky="nsew" , **self.entries_padding)

        self.right_frame_label_entry4 = tkk.CTkLabel(self.right_frame, text="Quantum Time", font=self.my_font_label)
        self.right_frame_label_entry4.grid(row=4, column=0)
        self.right_frame_entry4 = tkk.CTkEntry(self.right_frame, font=self.my_font)
        self.right_frame_entry4.grid(row=4, column=1, sticky="nsew" , **self.entries_padding)
        

        # -------Frame of Buttons-------
        self.right_frame_frame_buttons = tkk.CTkFrame(self.right_frame)
        self.right_frame_frame_buttons.grid(row=5, column=1, sticky="nsew", **self.frame_of_buttons_padding)
        self.right_frame_frame_buttons.grid_columnconfigure((0, 1, 2), weight=1)
        self.right_frame_frame_buttons.grid_rowconfigure(0, weight=1)

        self.right_frame_add_process = tkk.CTkButton(self.right_frame_frame_buttons, text="Add Process", font=self.my_font, command=self.add_process_round_robin)
        self.right_frame_add_process.grid(row=0, column=0, sticky="nsew", **self.buttons_padding)

        self.right_frame_reset_process = tkk.CTkButton(self.right_frame_frame_buttons, text="Reset Processes", font=self.my_font, fg_color="red", command=self.reset_process_round_robin)
        self.right_frame_reset_process.grid(row=0, column=1, sticky="nsew", **self.buttons_padding)

        self.right_frame_load_process = tkk.CTkButton(self.right_frame_frame_buttons, text="Load Process", font=self.my_font, fg_color="black", command=self.load_process_round_robin)
        self.right_frame_load_process.grid(row=0, column=2, sticky="nsew", **self.buttons_padding)


        self.right_frame_count_process = tkk.CTkLabel(self.right_frame, text="Prcoess Number: 0", font=self.my_font_label)
        self.right_frame_count_process.grid(row=5, column=0)

        # ----------Start Simulation button------------

        self.run_simulation = tkk.CTkButton(self.input_frame, text="Start Simulation", height=80, font=self.my_font_label , command=self.start_simulation)
        self.run_simulation.grid(row=2, column=0, columnspan=2, sticky="nsew", **pad)

        for i in range(6):  # rows
            self.left_frame.grid_rowconfigure(i, weight=1)
            self.right_frame.grid_rowconfigure(i, weight=1)


        self.left_frame.grid_columnconfigure(0, weight=2)
        self.left_frame.grid_columnconfigure(1, weight=3)

        self.right_frame.grid_columnconfigure(0, weight=2)
        self.right_frame.grid_columnconfigure(1, weight=3)


    def add_process_round_robin(self):
        try:
            pid = int(self.right_frame_entry1.get())
            arrival = int(self.right_frame_entry2.get())
            burst = int(self.right_frame_entry3.get())
            self.quantum = int(self.right_frame_entry4.get())

            
            if pid < 0 or arrival < 0 or burst < 0 or self.quantum < 0:
                messagebox.showerror("Error", "Invalid Input: Values cannot be negative")
                return
            
            for pi, a in enumerate(self.arr_p_round_robin):
                if pid == a.id:
                    messagebox.showerror("Error", "Process IP already exist.")
                    self.right_frame_entry1.delete(0, tk.END)
                    self.right_frame_entry2.delete(0, tk.END)
                    self.right_frame_entry3.delete(0, tk.END)
                    self.right_frame_entry4.delete(0, tk.END)
                    self.quantum = None
                    return

            p = Process(pid, arrival, burst,quantum=self.quantum)
            self.arr_p_round_robin.append(p)

            # 3. Dynamically update the count label text
            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")

            # Clear inputs after successfully adding
            self.right_frame_entry1.delete(0, tk.END)
            self.right_frame_entry2.delete(0, tk.END)
            self.right_frame_entry3.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Please fill all fields with numbers.")


    def add_process_priority(self):
        try:
            pid = int(self.left_frame_entry1.get())
            arrival = int(self.left_frame_entry2.get())
            burst = int(self.left_frame_entry3.get())
            # FIXED: point to left_frame_entry4 instead of entry3
            priority = int(self.left_frame_entry4.get())
            
           


            if pid < 0 or arrival < 0 or burst < 0 or priority < 0:
                messagebox.showerror("Error", "Invalid Input: Values cannot be negative")
                return
            
             
            for pi, a in enumerate(self.arr_p_priority):
                if pid == a.id:
                    messagebox.showerror("Error", "Process IP already exist.")
                    self.left_frame_entry1.delete(0, tk.END)
                    self.left_frame_entry2.delete(0, tk.END)
                    self.left_frame_entry3.delete(0, tk.END)
                    self.left_frame_entry4.delete(0, tk.END)
                    return

            p = Process(pid, arrival, burst, priority)
            self.arr_p_priority.append(p)

            # 3. Dynamically update the count label text
            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")

            # Clear inputs after successfully adding
            self.left_frame_entry1.delete(0, tk.END)
            self.left_frame_entry2.delete(0, tk.END)
            self.left_frame_entry3.delete(0, tk.END)
            self.left_frame_entry4.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Please fill all fields with numbers.")
    
    def reset_process_priority(self):
        try:
            self.arr_p_priority.clear()

            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")

            self.left_frame_entry1.delete(0, tk.END)
            self.left_frame_entry2.delete(0, tk.END)
            self.left_frame_entry3.delete(0, tk.END)
            self.left_frame_entry4.delete(0, tk.END)
            messagebox.showinfo("Success", "Processes has been resetted")
        except ValueError:
            messagebox.showerror("Error", "Couldn't Delete Processes")

    def reset_process_round_robin(self):
        try:
            self.arr_p_round_robin.clear()

            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")

            self.right_frame_entry1.delete(0, tk.END)
            self.right_frame_entry2.delete(0, tk.END)
            self.right_frame_entry3.delete(0, tk.END)
            self.right_frame_entry4.delete(0, tk.END)
            messagebox.showinfo("Success", "Processes has been resetted")
        except ValueError:
            messagebox.showerror("Error", "Couldn't Delete Processes")

    def load_case_a(self):
        try:
            self.arr_p_round_robin.clear()
            self.arr_p_priority.clear()
            pid = [1, 2, 3]
            p_arrival = [0, 1, 2]
            p_burst = [5,3,4]
            p_priority = [2, 1, 3]
            self.quantum = 3


            for i in range(len(pid)):
                p_rr = Process(pid[i], p_arrival[i], p_burst[i], quantum=self.quantum)
                p_pp = Process(pid[i], p_arrival[i], p_burst[i], p_priority[i])
                self.arr_p_round_robin.append(p_rr)
                self.arr_p_priority.append(p_pp)
                
            
            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")

            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")


            messagebox.showinfo("Success", "Loaded Processes of The Two Algorithms")

        except ValueError:
            messagebox.showerror("Error", "Failed to load data")

    def load_case_b(self):
        try:
            self.arr_p_round_robin.clear()
            self.arr_p_priority.clear()
            pid = [1, 2, 3]
            p_arrival = [0, 1, 2]
            p_burst = [8,8,2]
            p_priority = [3, 3, 1]
            self.quantum = 3


            for i in range(len(pid)):
                p_rr = Process(pid[i], p_arrival[i], p_burst[i], quantum=self.quantum)
                p_pp = Process(pid[i], p_arrival[i], p_burst[i], p_priority[i])
                self.arr_p_round_robin.append(p_rr)
                self.arr_p_priority.append(p_pp)
                
            
            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")

            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")


            messagebox.showinfo("Success", "Loaded Processes of The Two Algorithms")

        except ValueError:
            messagebox.showerror("Error", "Failed to load data")

    def load_case_c(self):
        try:
            self.arr_p_round_robin.clear()
            self.arr_p_priority.clear()
            self.quantum = 2
            pid = [1, 2, 3]
            p_arrival = [0, 0, 0]
            p_burst = [10,10,10]
            p_priority = [1, 2, 3]



            for i in range(len(pid)):
                p_rr = Process(pid[i], p_arrival[i], p_burst[i], quantum=self.quantum)
                p_pp = Process(pid[i], p_arrival[i], p_burst[i], p_priority[i])
                self.arr_p_round_robin.append(p_rr)
                self.arr_p_priority.append(p_pp)
                
            
            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")

            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")


            messagebox.showinfo("Success", "Loaded Processes of The Two Algorithms")

        except ValueError:
            messagebox.showerror("Error", "Failed to load data")

    def load_case_d(self):
        try:
            self.arr_p_round_robin.clear()
            self.arr_p_priority.clear()
            self.quantum = 3
            pid = [1, 2, 3, 4]
            p_arrival = [0, 1, 3, 5]
            p_burst = [10,3,3,3]
            p_priority = [4, 1, 1, 1]



            for i in range(len(pid)):
                p_rr = Process(pid[i], p_arrival[i], p_burst[i], quantum=self.quantum)
                p_pp = Process(pid[i], p_arrival[i], p_burst[i], p_priority[i])
                self.arr_p_round_robin.append(p_rr)
                self.arr_p_priority.append(p_pp)
                
            
            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")

            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")


            messagebox.showinfo("Success", "Loaded Processes of The Two Algorithms")

        except ValueError:
            messagebox.showerror("Error", "Failed to load data")


    def load_process_round_robin(self):
        try:
            self.arr_p_round_robin.clear()
            pid = [1, 2, 3, 4]
            p_arrival = [0, 1, 2, 4]
            p_burst = [5, 3, 8, 6]
            self.quantum = 3


            for i in range(4):
                p_rr = Process(pid[i], p_arrival[i], p_burst[i], quantum=self.quantum)
                self.arr_p_round_robin.append(p_rr)
            
            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")

            messagebox.showinfo("Success", "Loaded Process for Round Robin")

        except ValueError:
            messagebox.showerror("Error", "Failed to load data")
    
    def load_process_priority(self):
        try:
            self.arr_p_priority.clear()
            pid = [1, 2, 3, 4]
            p_arrival = [0, 1, 2, 4]
            p_burst = [5, 3, 8, 6]
            p_priority = [2, 1, 4, 3]

            for i in range(4):
                p_pp = Process(pid[i], p_arrival[i], p_burst[i], p_priority[i])
                self.arr_p_priority.append(p_pp)
            
            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")

            messagebox.showinfo("Success", "Loaded Process for Priority Scheduling")        

        except ValueError:
            messagebox.showerror("Error", "Failed to load data")


    def create_gantt_chart(self, frame, timeline, row_start, num_process):
        if not timeline:
            return


        frame.update_idletasks()

        frame_width = frame.winfo_width()
        visible_width = frame_width - 30 if frame_width > 100 else 370


        total_time = timeline[-1][2]
        pixels_per_unit = 25  
        calculated_width = total_time * pixels_per_unit
        

        canvas_draw_width = max(visible_width, calculated_width)


        container = tk.Frame(frame, bg="#2b2b2b")
        container.grid(row=row_start, column=0, columnspan=4, sticky="ew", pady=15, padx=15)
        container.grid_columnconfigure(0, weight=1)


        canvas = tk.Canvas(
            container, 
            width=visible_width, 
            height=90, 
            bg="#2b2b2b", 
            highlightthickness=0
        )
        
       
        if calculated_width > visible_width:
            scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
            canvas.configure(xscrollcommand=scrollbar.set)
            
            canvas.grid(row=0, column=0, sticky="ew")
            scrollbar.grid(row=1, column=0, sticky="ew", pady=(5, 0))
            

            canvas.bind("<MouseWheel>", lambda event: canvas.xview_scroll(int(-1 * (event.delta / 120)), "units"))
            canvas.bind("<Button-4>", lambda event: canvas.xview_scroll(-1, "units")) 

            canvas.bind("<Button-5>", lambda event: canvas.xview_scroll(1, "units"))
        else:
            canvas.grid(row=0, column=0, sticky="ew")


        canvas.config(scrollregion=(0, 0, canvas_draw_width, 90))


        margin = 15
        usable_width = canvas_draw_width - (2 * margin)
        scale = usable_width / total_time if total_time > 0 else 1

        x = margin
        for pid, start, end in timeline:
            width = (end - start) * scale
            color = "#1f6aa5" if pid != "Idle" else "#555555"


            canvas.create_rectangle(x, 15, x + width, 50, fill=color, outline="white", width=1)

            
            label_text = f"P{pid}" if pid != "Idle" else "Idle"
            if width > 35:
                canvas.create_text(x + width/2, 32, text=label_text, fill="white", font=("Arial", 10, "bold"))
            elif width > 18:
               
                short_text = str(pid) if pid != "Idle" else "I"
                canvas.create_text(x + width/2, 32, text=short_text, fill="white", font=("Arial", 8, "bold"))

   
            canvas.create_text(x, 60, text=str(start), fill="#cccccc", font=("Arial", 9), anchor="n")

            x += width


        canvas.create_text(x, 60, text=str(timeline[-1][2]), fill="#cccccc", font=("Arial", 9), anchor="n")
    
    def back_to_input(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        self.result_frame.grid_forget()
        self.input_frame.grid(row=0, column=0, sticky="nsew")


    def generate_analysis(self, prio_avg, rr_avg):
        prio_tat, prio_wt, prio_rt = prio_avg
        rr_tat, rr_wt, rr_rt = rr_avg

        analysis = []

        # 1. Waiting Time
        if prio_wt < rr_wt:
            analysis.append("Priority Scheduling gave better average waiting time.")
        elif rr_wt < prio_wt:
            analysis.append("Round Robin gave better average waiting time.")
        else:
            analysis.append("Both algorithms have equal waiting time.")

        # 2. Response Time
        if prio_rt < rr_rt:
            analysis.append("Priority Scheduling gave better response time.")
        elif rr_rt < prio_rt:
            analysis.append("Round Robin gave better response time.")
        else:
            analysis.append("Both algorithms have equal response time.")

        # 3. Priority advantage
        analysis.append("Higher-priority processes were executed earlier in Priority Scheduling.")

        # 4. Fairness
        analysis.append("Round Robin distributes CPU time more evenly among processes.")

        # 5. Starvation
        if prio_wt > rr_wt * 1.5:
            analysis.append("Possible starvation detected in Priority Scheduling.")
        else:
            analysis.append("No strong starvation observed.")

        # 6. Recommendation
        if rr_wt < prio_wt:
            analysis.append("Round Robin is recommended for fairness.")
        else:
            analysis.append("Priority Scheduling is recommended for urgent tasks.")

        return analysis
        
    def start_simulation(self):
        if not hasattr(self, "quantum"):
            messagebox.showerror("Error", "Please set Quantum Time for Round Robin")
            return
        if self.quantum is None:
            self.quantum = self.arr_p_round_robin[0].quantum
        from copy import deepcopy

        # ---------Validate Input----------
        if not self.arr_p_priority or not self.arr_p_round_robin:
            messagebox.showerror("Error", "Please add processes first.")
            return

        # ---------Clone Processes---------
        prio_processes = deepcopy(self.arr_p_priority)
        rr_processes = deepcopy(self.arr_p_round_robin)

        # ---------Run Algorithms---------
        prio_done, prio_time_line = prioity_scheduling(prio_processes)
        rr_done, rr_time_line = round_robin(rr_processes, self.quantum)

        # -----------Calculate Metrics-----------
        prio_results, prio_avg = calculate_metrcies(prio_done)
        rr_results, rr_avg = calculate_metrcies(rr_done)

        # -----------Clear Old UI-----------
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        self.input_frame.grid_forget()
        self.result_frame.grid(row=0, column=0, sticky="nsew")

        back_btn = tkk.CTkButton(
            self.result_frame,
            text="Back",
            command=self.back_to_input
        )
        back_btn.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        

        # ----------- Table Builder -----------
        def create_table(frame, title, results, avg, time_line):
            frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
            count  = 0
            # Title
            tkk.CTkLabel(frame, text=title, font=self.my_font_label_main)\
                .grid(row=0, column=0, columnspan=4, pady=10)

            # Headers
            headers = ["PID", "WT", "TAT", "RT"]
            for col, h in enumerate(headers):
                tkk.CTkLabel(frame, text=h, font=self.my_font_label)\
                    .grid(row=1, column=col, padx=5, pady=5)

            # Data Rows
            for i, (pid, tat, wt, rt) in enumerate(results, start=2):
                count += 1
                tkk.CTkLabel(frame, text=str(pid), font=self.my_font)\
                    .grid(row=i, column=0)

                tkk.CTkLabel(frame, text=str(wt), font=self.my_font)\
                    .grid(row=i, column=1)

                tkk.CTkLabel(frame, text=str(tat), font=self.my_font)\
                    .grid(row=i, column=2)

                tkk.CTkLabel(frame, text=str(rt), font=self.my_font)\
                    .grid(row=i, column=3)

            # Averages
            avg_tat, avg_wt, avg_rt = avg
            last_row = len(results) + 2

            tkk.CTkLabel(frame, text="AVG", font=self.my_font_label)\
                .grid(row=last_row, column=0)

            tkk.CTkLabel(frame, text=f"{avg_wt:.2f}", font=self.my_font)\
                .grid(row=last_row, column=1)

            tkk.CTkLabel(frame, text=f"{avg_tat:.2f}", font=self.my_font)\
                .grid(row=last_row, column=2)

            tkk.CTkLabel(frame, text=f"{avg_rt:.2f}", font=self.my_font)\
                .grid(row=last_row, column=3)
            
            for r in range(last_row + 2):
                frame.grid_rowconfigure(r, weight=1)
            self.create_gantt_chart(frame, time_line, last_row + 1, count)


        # -----------Recreate Frames-----------
        self.left_frame_result = tkk.CTkFrame(self.result_frame)
        self.left_frame_result.grid(row=0, column=0, sticky="nsew")

        self.right_frame_result = tkk.CTkFrame(self.result_frame)
        self.right_frame_result.grid(row=0, column=1, sticky="nsew")

        self.bottom_frame_result = tkk.CTkFrame(self.result_frame)
        self.bottom_frame_result.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # -----------Fill Tables-----------
        create_table(
            self.left_frame_result,
            "Priority Scheduling Results",
            prio_results,
            prio_avg,
            prio_time_line
        )

        create_table(
            self.right_frame_result,
            "Round Robin Results",
            rr_results,
            rr_avg,
            rr_time_line
        )
        self.comparison_frame = tkk.CTkFrame(self.bottom_frame_result)
        self.comparison_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
  
        self.comparison_frame.grid_columnconfigure(0, weight=3)
        self.comparison_frame.grid_columnconfigure(1, weight=2)

        #------------Left Container - Summary & Analysis--------------
        analysis_container = tkk.CTkFrame(self.comparison_frame, fg_color="transparent")
        analysis_container.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        tkk.CTkLabel(
            analysis_container,
            text="Summary & Analysis",
            font=self.my_font_label_main
        ).pack(pady=(0, 10), anchor="w")

        analysis = self.generate_analysis(prio_avg, rr_avg)
        for line in analysis:
            tkk.CTkLabel(
                analysis_container,
                text="• " + line, 
                font=self.my_font, 
                anchor='w',
                justify='left'
            ).pack(anchor="w", pady=4)
        
        # 2. Right Container - Conclusion
        conclusion_container = tkk.CTkFrame(self.comparison_frame, fg_color="transparent")
        conclusion_container.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        tkk.CTkLabel(
            conclusion_container,
            text="Conclusion",
            font=self.my_font_label_main
        ).pack(pady=(0, 10), anchor="w")

        better_algo = "Round Robin" if rr_avg[1] < prio_avg[1] else "Priority Scheduling"
        starvation_risk = "Yes" if prio_avg[1] > rr_avg[1] else "Low"

        conclusions = [
            f"Better Algorithm: {better_algo}",
            "Priority improves urgent-task execution.",
            "Round Robin improves fairness.",
            f"Starvation risk: {starvation_risk}"
        ]

        for line in conclusions:
            tkk.CTkLabel(
                conclusion_container,
                text="• " + line,
                font=self.my_font,
                anchor='w',
                justify='left'
            ).pack(anchor="w", pady=4)




# -------RUN-------
root = tk.Tk()
root.geometry("800x500")
root.configure(background='black')
app = APP(root)
root.mainloop()



# CASE A
quantum = 3
process_id = [1, 2, 3]
arrival_time = [0, 1, 2]
burst_time = [5,3,4]
priority = [2, 1, 3]




# CASE B
quantum = 3
process_id = [1, 2, 3]
arrival_time = [0, 1, 2]
burst_time = [8,8,2]
priority = [3, 3, 1]


# CASE C
quantum = 2
process_id = [1, 2, 3]
arrival_time = [0, 0, 0]
burst_time = [10,10,10]
priority = [1, 2, 3]


# CASE D
quantum = 3
process_id = [1, 2, 3, 4]
arrival_time = [0, 1, 3, 5]
burst_time = [10,3,3,3]
priority = [4, 1, 1, 1]



# CASE E
"""
Field,    Input Value,      Expected App Behavior,                      Code Triggered
Any Field   ,Leave Empty,"Show Error: Please fill all fields with numbers.",except ValueError
Any Field  ,abc or 12.5,"Show Error: Please fill all fields with numbers.",except ValueError
Process ID  ,-5,"Show Error: Invalid Input: Values cannot be negative",if pid < 0 boundary check
Process ID  ,1 (Twice),"Show Error: Process IP already exist.",for pid == a.id duplicate check
Start Simulation   ,No processes added,"Show Error: Please add processes first.",if not self.arr_p_priority validation
"""
