import tkinter as tk
import webbrowser

class Resources:
    @staticmethod
    def open_link(url):
        webbrowser.open(url, new=2)

    @staticmethod
    def show_resources(content_frame):
        # Clear any previous content
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Heading
        tk.Label(content_frame, text="📚 Mental Health Resources", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=30)

        # Links to different resources
        resource_links = [
            ("Mental Health Foundation", "https://www.mentalhealth.org.uk"),
            ("World Health Organization - Mental Health", "https://www.who.int/mental_health"),
            ("National Institute of Mental Health", "https://www.nimh.nih.gov"),
            ("Mind - Mental Health Charity", "https://www.mind.org.uk"),
            ("Anxiety Support", "https://www.anxietyuk.org.uk")
        ]

        # Display resources with clickable links
        for text, url in resource_links:
            link_label = tk.Label(content_frame, text=text, font=("Segoe UI", 12, "underline"), fg="#2980b9", bg="white")
            link_label.pack(pady=10)

            # Bind each label to open the URL when clicked
            link_label.bind("<Button-1>", lambda e, url=url: Resources.open_link(url))

