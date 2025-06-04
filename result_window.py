import tkinter as tk
from tkinter import ttk
from logic import generate_symptom_graph  # 👈 Import the graph function

# Sample dictionary of symptom translations (add more as needed)
SYMPTOM_TRANSLATIONS = {
    "Feeling nervous, anxious, or on edge": "चिंतेत, अस्वस्थ वाटणे",
    "Not being able to stop or control worrying": "चिंता थांबवू न शकणे",
    "Worrying too much about different things": "वेगवेगळ्या गोष्टींबद्दल खूप चिंता करणे",
    "Trouble relaxing": "विश्रांती घेण्यात अडचण",
    "Being so restless that it is hard to sit still": "खूप अस्वस्थ वाटणे",
    "Becoming easily annoyed or irritable": "सहज चिडणे",
    "Feeling afraid as if something awful might happen": "भीती वाटणे की काहीतरी वाईट घडेल",
}

def show_results_window(frequency_dict, daywise_dict, intensity):
    result_win = tk.Toplevel()
    result_win.title("तपशीलवार अहवाल")
    result_win.geometry("700x500")
    result_win.configure(bg="white")

    tk.Label(result_win, text=f"💡 चिंता तीव्रता पातळी: {intensity}",
             font=("Segoe UI", 15, "bold"), fg="#2c3e50", bg="white").pack(pady=20)

    canvas = tk.Canvas(result_win, bg="white", borderwidth=0, highlightthickness=0)
    frame = tk.Frame(canvas, bg="white")
    scrollbar = ttk.Scrollbar(result_win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_frame_configure)

    for symptom, days in daywise_dict.items():
        if frequency_dict.get(symptom, 0) > 0:
            marathi = SYMPTOM_TRANSLATIONS.get(symptom, "")
            label_text = f"➡️ {symptom} ({marathi})\n    दिवस: {', '.join(days)}"
            tk.Label(frame, text=label_text, font=("Segoe UI", 12), bg="white",
                     justify="left", anchor="w", wraplength=650).pack(anchor="w", padx=20, pady=8)

    # 👇 Add this button to show graph
    tk.Button(result_win, text="📊 १५ दिवसांचा लक्षणे ग्राफ पहा",
              font=("Segoe UI", 11), command=lambda: generate_symptom_graph(daywise_dict)).pack(pady=15)

    result_win.mainloop()
