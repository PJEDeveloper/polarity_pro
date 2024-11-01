import tkinter as tk
import ato

# Main function to initialize and start the GUI application
def main():
    root = tk.Tk()  # Create the main window for the GUI
    root.title("Polarity Pro - Speech Recognition and Analysis")  # Set window  title for identification
    ato.init_gui(root)  # Call the GUI initialization function from ato.py
    root.mainloop()  # Start the Tkinter event loop to keep the window open

# Run main to execute script directly
if __name__ == '__main__':
    main()
