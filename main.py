import tkinter as tk
from actions import btn1_action, btn2_action, segment, upload_action

# Set up the root window
root = tk.Tk()
root.title("Image Viewer")
root.geometry("1100x800")


# Create the frames for buttons and image
def set_interface(root):

    left_frame = tk.Frame(root, width=200, height=800, bg='white')
    left_frame.grid(row=0, column=0, padx=10, pady=5)
    left_frame.grid_propagate(False)

    right_frame = tk.Frame(root, width=1000, height=800, bg='lightgray')
    right_frame.grid(row=0, column=1, padx=10, pady=5)
    right_frame.grid_propagate(False)

    canvas = tk.Canvas(right_frame, width=1000, height=800)
    canvas.pack()
    return left_frame, canvas


left_frame, canvas = set_interface(root)


upload_btn = tk.Button(left_frame, text="Upload", command=lambda:upload_action(tk, canvas))
upload_btn.pack(pady=10)

create_points_btn = tk.Button(left_frame, text="Points", command=lambda: btn1_action(canvas))
create_points_btn.pack(pady=10)

create_box_btn = tk.Button(left_frame, text="Box", command=lambda: btn2_action(canvas))
create_box_btn.pack(pady=10)

segment_btn = tk.Button(left_frame, text="segment!", command=segment)
segment_btn.pack(pady=10)



root.mainloop()