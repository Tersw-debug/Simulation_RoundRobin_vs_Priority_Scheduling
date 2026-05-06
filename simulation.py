
# Python + Tkinter Scheduling Comparison Project
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
                if p.priority < best :
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
        self.input_frame.grid_rowconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)
        
        self.result_frame = tkk.CTkFrame(self.main_frame)
        self.result_frame.grid_rowconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(1, weight=0) 
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_columnconfigure(1, weight=1)

        pad = {"padx": 5, "pady": 5}
        self.entries_padding = {"padx": 10, "pady": 10}
        self.buttons_padding = {"padx": 10, "pady": 10}
        self.frame_of_buttons_padding = {"padx": 10, "pady": 10}
        self.my_font = tkk.CTkFont(family="Arial", size=18, weight="normal")
        self.my_font_label = tkk.CTkFont(family="Arial", size=20, weight="normal")
        self.my_font_label_main = tkk.CTkFont(family="Arial", size=22, weight="normal")
        self.count_process_round_robin = ""
        self.count_process_priority = ""
        self.arr_p_round_robin = []
        self.arr_p_priority = []

        self.entries = []

        # -----------Left Frame-----------
        self.left_frame = tkk.CTkFrame(self.input_frame)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
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

        # ----------------left frame of Buttons----------------
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

        # -----------Right Frame------------
        self.right_frame = tkk.CTkFrame(self.input_frame)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
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
        

        # ---------Frame of Buttons---------
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
        self.run_simulation.grid(row=1, column=0, columnspan=2, sticky="nsew", **pad)

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
        # Force Tkinter to finish laying out widgets so winfo_width() returns a real value
        frame.update_idletasks()
        
        # Determine usable width. Fall back to 380 (a safe size for 800px window) if not yet drawn.
        frame_width = frame.winfo_width()
        canvas_width = frame_width - 30 if frame_width > 100 else 370
        
        # Create canvas with dynamic width
        canvas = tk.Canvas(frame, width=canvas_width, height=90, bg="#2b2b2b", highlightthickness=0)
        canvas.grid(row=row_start, column=0, columnspan=4, sticky="ew", pady=15, padx=15)

        if not timeline:
            return

        total_time = timeline[-1][2]
        
        # Margin prevents the first/last timestamps from clipping off the edges
        margin = 15
        usable_width = canvas_width - (2 * margin)
        scale = usable_width / total_time if total_time > 0 else 1

        x = margin
        for pid, start, end in timeline:
            width = (end - start) * scale
            color = "#1f6aa5" if pid != "Idle" else "#555555"

            # 1. Draw block rectangle with a clean white border
            canvas.create_rectangle(x, 15, x + width, 50, fill=color, outline="white", width=1)

            # 2. Label inside (Using white text for visibility!)
            label_text = f"P{pid}" if pid != "Idle" else "Idle"
            canvas.create_text(x + width/2, 32, text=label_text, fill="white", font=("Arial", 11, "bold"))

            # 3. Time markers (Using light-gray text!)
            canvas.create_text(x, 60, text=str(start), fill="#cccccc", font=("Arial", 9), anchor="n")

            x += width

        # 4. Final closing timestamp marker
        canvas.create_text(x, 60, text=str(timeline[-1][2]), fill="#cccccc", font=("Arial", 9), anchor="n")
    
    def back_to_input(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        self.result_frame.grid_forget()
        self.input_frame.grid(row=0, column=0, sticky="nsew")
    
    def start_simulation(self):
        if not hasattr(self, "quantum"):
            messagebox.showerror("Error", "Please set Quantum Time for Round Robin")
            return
        if self.quantum is None:
            self.quantum = self.arr_p_round_robin[0].quantum
        from copy import deepcopy

        # -----------Validate Input-----------
        if not self.arr_p_priority or not self.arr_p_round_robin:
            messagebox.showerror("Error", "Please add processes first.")
            return

        # -----------Clone Processes-----------
        prio_processes = deepcopy(self.arr_p_priority)
        rr_processes = deepcopy(self.arr_p_round_robin)

        # -----------Run Algorithms-----------
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
        back_btn.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        

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






# -------RUN-------
root = tk.Tk()
root.geometry("800x500")
root.configure(background='black')
app = APP(root)
root.mainloop()


"""
Things Needed to be added

What is still missing (for full marks)
1. ❌ Gantt Charts (IMPORTANT)

Right now → text only

You should add:

Canvas widget
Draw rectangles like a timeline

If you want, I can add that next (it’s actually easy in Tkinter).

2. ❌ Comparison Section

You need a clear conclusion block, like:

RR is more fair because...
Priority favors urgent processes...
Starvation observed when...

Right now → not implemented

3. ❌ Separate UI Sections

Better structure:

Input area
RR results
Priority results
Comparison section

Right now → everything is dumped in one text box

4. ⚠️ Priority Rule (must be stated in report)

Your system uses:

Smaller number = higher priority
Non-preemptive
Tie → first arrived

You must write this explicitly in your report.

"""