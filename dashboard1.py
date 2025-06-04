import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import csv
from logic import load_symptoms_data, detect_symptom, save_frequency_to_csv, calculate_intensity_score, generate_symptom_graph
from resources import Resources
from result_window import show_results_window
from theme import get_theme


class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mental Health Dashboard")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f0f2f5")

        self.data = load_symptoms_data("symptoms_data.csv")
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=10)
        style.configure("TCombobox", font=("Segoe UI", 11), padding=5)
        style.configure("Accent.TButton", background="#1abc9c", foreground="white", font=("Segoe UI", 11, "bold"))

        self.sidebar = tk.Frame(self.root, bg="#2c3e50", width=200)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self.root, bg="white")
        self.content.pack(side="right", expand=True, fill="both")

        nav_items = [
            ("Home", self.show_home),
            ("Resources", self.show_resources),
            ("Test", self.show_test),
            ("Appointment", self.show_appointment),
            ("About", self.show_about)
        ]

        for text, command in nav_items:
            btn = tk.Button(self.sidebar, text=text, font=("Segoe UI", 12), fg="white", bg="#34495e",
                            activebackground="#1abc9c", activeforeground="white", relief="flat",
                            command=command)
            btn.pack(fill="x", padx=10, pady=5)

        self.show_home()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()
        tk.Label(self.content, text="🏠 Welcome to the Mental Health Dashboard",
                 font=("Segoe UI", 16, "bold"), bg="white").pack(pady=30)

    def show_resources(self):
        Resources.show_resources(self.content)

    def show_about(self):
        self.clear_content()
        tk.Label(self.content, text="ℹ️ About This Project", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=30)
        about_text = (
            "This application helps detect anxiety symptoms based on the GAD-7 framework.\n"
            "Users can enter diary-like symptom entries for 15 days, and the system analyzes\n"
            "them to classify anxiety intensity as minimal, mild, moderate, or severe.\n"
            "\nThe dashboard also includes useful mental health resources and doctor appointment details."
        )
        tk.Label(self.content, text=about_text, font=("Segoe UI", 12), bg="white", justify="left", wraplength=800).pack(padx=20)

    def show_test(self):
        self.clear_content()
        tk.Label(self.content, text="🧪 Mental Health Test", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=20)

        button_frame = tk.Frame(self.content, bg="white")
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Single Text", command=self.show_single_test).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="15 Days Text", command=self.show_15days_test).grid(row=0, column=1, padx=10)

        self.test_section = tk.Frame(self.content, bg="white")
        self.test_section.pack(fill="both", expand=True)

    def show_single_test(self):
        for widget in self.test_section.winfo_children():
            widget.destroy()

        tk.Label(self.test_section, text="मराठीत एक वाक्य लिहा:", font=("Segoe UI", 12), bg="white").pack(pady=10)

        self.single_input = tk.StringVar()
        input_entry = ttk.Entry(self.test_section, textvariable=self.single_input, font=("Segoe UI", 12), width=60)
        input_entry.pack(pady=5)

        ttk.Button(self.test_section, text="🔍 लक्षण शोधा", command=self.check_single_symptom).pack(pady=10)

        self.single_result = tk.Label(self.test_section, text="", font=("Segoe UI", 13, "bold"), bg="white", fg="#2980b9", justify="left")
        self.single_result.pack(pady=10)

    def check_single_symptom(self):
        user_text = self.single_input.get()
        results = detect_symptom(user_text, self.data)

        if results:
            formatted = "\n".join(f"➡️ {symptom}" for symptom in results)
            self.single_result.config(text=formatted)
        else:
            self.single_result.config(text="❌ लक्षण आढळले नाही")

    def show_15days_test(self):
        for widget in self.test_section.winfo_children():
            widget.destroy()

        tk.Label(self.test_section, text="15 दिवसांचे मराठी वाक्य (प्रत्येक दिवसासाठी एक वाक्य):", font=("Segoe UI", 12), bg="white").pack(pady=10)

        self.day_entries = []
        form_frame = tk.Frame(self.test_section, bg="white")
        form_frame.pack()

        for i in range(15):
            row = tk.Frame(form_frame, bg="white")
            row.pack(pady=2)
            tk.Label(row, text=f"Day {i + 1}:", font=("Segoe UI", 11), bg="white", width=10, anchor="w").pack(side="left")
            entry = ttk.Entry(row, font=("Segoe UI", 11), width=60)
            entry.pack(side="left", padx=5)
            self.day_entries.append(entry)

        ttk.Button(self.test_section, text="🔍 लक्षणे शोधा", command=self.check_multiple_symptoms).pack(pady=10)

        self.graph_btn = None
        self.theme_button = None
        self.multi_result = tk.Label(self.test_section, text="", font=("Segoe UI", 13), bg="white", fg="#2c3e50", justify="left")
        self.multi_result.pack(pady=10)

    def check_multiple_symptoms(self):
        frequency = {}
        daywise = {}
        all_text = []

        for idx, entry in enumerate(self.day_entries):
            line = entry.get().strip()
            if line:
                all_text.append(line)
                symptoms = detect_symptom(line, self.data)
                for symptom in symptoms:
                    frequency[symptom] = frequency.get(symptom, 0) + 1
                    if symptom not in daywise:
                        daywise[symptom] = []
                    daywise[symptom].append(f"Day {idx + 1}")

        if frequency:
            save_frequency_to_csv(frequency)
            intensity = calculate_intensity_score(frequency)
            show_results_window(frequency, daywise, intensity)

            detected_theme = get_theme(" ".join(all_text))

            if self.theme_button:
                self.theme_button.destroy()

            self.theme_button = ttk.Button(self.test_section, text=f"📘 Theme: {detected_theme}", style="Accent.TButton")
            self.theme_button.pack(pady=5)

            if self.graph_btn:
                self.graph_btn.destroy()

            self.graph_btn = ttk.Button(self.test_section, text="📈 Show Symptom Graph",
                                        command=lambda: generate_symptom_graph(daywise))
            self.graph_btn.pack(pady=10)

        else:
            self.multi_result.config(text="❌ एकही लक्षण सापडले नाही.")

    def show_appointment(self):
        self.clear_content()
        tk.Label(self.content, text="🗓️ डॉक्टर अपॉइंटमेंट", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=20)

        dropdown_frame = tk.Frame(self.content, bg="white")
        dropdown_frame.pack(pady=10)

        tk.Label(dropdown_frame, text="Select City:", font=("Segoe UI", 12), bg="white").pack(side="left", padx=5)

        self.selected_city = tk.StringVar()
        city_combo = ttk.Combobox(dropdown_frame, textvariable=self.selected_city, values=["Thane", "Mumbai", "Navi Mumbai"],
                                   font=("Segoe UI", 12), state="readonly", width=20)
        city_combo.pack(side="left", padx=5)
        city_combo.bind("<<ComboboxSelected>>", self.display_doctors)

        self.doctor_container = tk.Frame(self.content, bg="white")
        self.doctor_container.pack(pady=20, fill="both", expand=True)

    def display_doctors(self, event):
        for widget in self.doctor_container.winfo_children():
            widget.destroy()

        city = self.selected_city.get()
        doctors = {
            "Thane": [
                {"name": "Dr. Neha Deshmukh", "time": "10am - 1pm", "degree": "MD Psychiatry", "fees": "₹800", "email": "neha@clinic.com", "contact": "9988776655"},
                {"name": "Dr. Karan Mehta", "time": "2pm - 5pm", "degree": "MBBS, DPM", "fees": "₹700", "email": "karan@mindcare.com", "contact": "9876543210"},
                {"name": "Dr. Swati Pawar", "time": "6pm - 9pm", "degree": "PhD, Psychiatry", "fees": "₹900", "email": "swati@wellbeing.com", "contact": "9765432100"},
            ],
            "Mumbai": [
                {"name": "Dr. Priya Shah", "time": "11am - 3pm", "degree": "MD Psychiatry", "fees": "₹1000", "email": "priya@mumbaihealth.com", "contact": "9123456789"},
                {"name": "Dr. Anand Joshi", "time": "4pm - 7pm", "degree": "MBBS, DNB", "fees": "₹950", "email": "anand@calmclinic.com", "contact": "9234567890"},
                {"name": "Dr. Ruchi Jain", "time": "9am - 12pm", "degree": "M.D., DPM", "fees": "₹850", "email": "ruchi@mindspace.com", "contact": "9345612789"},
            ],
            "Navi Mumbai": [
                {"name": "Dr. Seema Kulkarni", "time": "9am - 12pm", "degree": "Psychiatrist", "fees": "₹750", "email": "seema@naviwell.com", "contact": "9345678901"},
                {"name": "Dr. Rohan Patil", "time": "1pm - 4pm", "degree": "MD Psychiatry", "fees": "₹850", "email": "rohan@peaceclinic.com", "contact": "9456789012"},
                {"name": "Dr. Meena Verma", "time": "5pm - 8pm", "degree": "MBBS, MRC Psych", "fees": "₹920", "email": "meena@wellbeing.com", "contact": "9556677889"},
            ]
        }.get(city, [])

        grid = tk.Frame(self.doctor_container, bg="white")
        grid.pack()

        for i, doc in enumerate(doctors):
            card = tk.Frame(grid, bg="#ecf0f1", bd=1, relief="solid", width=280, height=200)
            card.grid(row=0, column=i, padx=15, pady=10)
            card.pack_propagate(False)

            info = f"""\U0001f468\u200d\U0001f3eb {doc['name']}
\U0001f393 {doc['degree']}
\U0001f552 {doc['time']}
\U0001f4b0 {doc['fees']}
\U0001f4e7 {doc['email']}
\U0001f4de {doc['contact']}"""

            tk.Label(card, text=info, font=("Segoe UI", 11), bg="#ecf0f1", justify="left", anchor="w").pack(padx=10, pady=10)


# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
