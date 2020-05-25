import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import ttk
from shapes import Circle, Angle, Polygon, Web
import random

"""
This parabolic_curves.py file contains the GUI that interacts with the user.
Draws instances of Angle, Polygon, Web, and Circle shapes to the canvas
based on user input. 

"""

CANVAS_SIZE = 500


class MainApp:
    # class variable
    mouse_click_counter = 0

    def __init__(self, master):
        self.temp_clicked_values = []
        self.lines_of_poly_widgets = []  # for clicked poly

        # holds the labels that update to show user clicked input
        self.angle_vertices_labels = []
        self.poly_vertices_labels = []
        self.web_vertices_labels = []
        # holds the user input boxes for typed input
        self.angle_vertices_entries = []
        self.poly_vertices_entries = []
        self.web_vertices_entries = []

        self.poly_each_vertex_labels = []

        self.web_msgs = ["Top of y-axis: ", "Bottom of y-axis: ", "Left of x-axis: ", "Right of x-axis: "]

        self.circle_ids = Circle.get_all_circles()
        self.label_ids = Circle.get_all_labels()

        # GUI elements
        self.master = master
        self.master.title("Parabolic Curves")

        self.base_frame1 = tk.Frame(self.master)
        self.base_frame2 = tk.Frame(self.master)

        self.canvas = tk.Canvas(self.base_frame1, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white")

        self.base_frame1.grid(row=0, column=0)
        self.base_frame2.grid(row=0, column=1)
        self.canvas.grid(row=0, column=0)
        self.instantiate_circles()
        self.create_shape_controls()
        self.create_input_controls()
        self.create_toggled_frames()
        self.create_buttons()
        self.create_status_bar()
        self.mouse_click_counter = 0
        self.color = 'black'  # default color

    def instantiate_circles(self):
        self.angle_circle = Circle(self.canvas)
        self.poly_circle = Circle(self.canvas)
        self.web_circle = Circle(self.canvas)

    def create_shape_controls(self):
        # 1. Choose shape
        # set up StringVar for Shape radiobuttons, with values of 'angle', 'poly', or 'web', with default 'angle' selected
        self.shape_svar = tk.StringVar(None, "angle")
        self.shape_frame = tk.Frame(self.base_frame2)
        self.shape_label = tk.Label(self.shape_frame, text="Choose shape to draw:", font=13)
        self.angle_rb = tk.Radiobutton(self.shape_frame,
                                       text="Angle",
                                       variable=self.shape_svar,
                                       value="angle",
                                       command=lambda: self.toggle_input_view(self.shape_svar.get(),
                                                                              self.input_svar.get()))
        self.polygon_rb = tk.Radiobutton(self.shape_frame,
                                         text="Polygon",
                                         variable=self.shape_svar,
                                         value="poly",
                                         command=lambda: self.toggle_input_view(self.shape_svar.get(),
                                                                                self.input_svar.get()))
        self.web_rb = tk.Radiobutton(self.shape_frame,
                                     text="Web",
                                     variable=self.shape_svar,
                                     value="web",
                                     command=lambda: self.toggle_input_view(self.shape_svar.get(),
                                                                            self.input_svar.get()))
        self.shape_separator = tk.ttk.Separator(self.shape_frame, orient='horizontal')

        self.shape_frame.grid(row=0, column=0)
        self.shape_label.grid(row=0, columnspan=3)
        self.angle_rb.grid(row=1, column=0)
        self.polygon_rb.grid(row=1, column=1)
        self.web_rb.grid(row=1, column=2)
        self.shape_separator.grid(row=2, column=0, columnspan=3, sticky='ew', pady=5)

    def create_input_controls(self):
        # set a StringVar for Input Style radiobuttons, with values of 'typed' or 'clicked', default 'typed' selected
        self.input_svar = tk.StringVar(None, "typed")  # sets default value of typed
        self.input_frame = tk.Frame(self.base_frame2)
        self.input_control_label = tk.Label(self.input_frame, text="Choose how to input:", font=13)
        self.input_typed_rb = tk.Radiobutton(self.input_frame,
                                             text="Type",
                                             variable=self.input_svar,
                                             value="typed",
                                             command=lambda: self.toggle_input_view(self.shape_svar.get(),
                                                                                    self.input_svar.get()))
        self.input_clicked_rb = tk.Radiobutton(self.input_frame,
                                               text="Click",
                                               variable=self.input_svar,
                                               value="clicked",
                                               command=lambda: self.toggle_input_view(self.shape_svar.get(),
                                                                                      self.input_svar.get()))
        self.input_separator = tk.ttk.Separator(self.input_frame, orient='horizontal')

        self.input_frame.grid(row=1, column=0)
        self.input_control_label.grid(row=0, column=0, columnspan=2)
        self.input_typed_rb.grid(row=1, column=0)
        self.input_clicked_rb.grid(row=1, column=1)
        self.input_separator.grid(row=2, column=0, columnspan=2, sticky='ew', pady=5)

    def create_toggled_frames(self):
        # 3. Container for shape/input 6 frames
        self.container_frame = tk.Frame(self.base_frame2)
        self.container_frame.grid(row=2, column=0)

        self.angle_typed_frame = tk.Frame(self.container_frame)
        self.angle_clicked_frame = tk.Frame(self.container_frame)
        self.poly_typed_frame = tk.Frame(self.container_frame)
        self.poly_clicked_frame = tk.Frame(self.container_frame)
        self.web_typed_frame = tk.Frame(self.container_frame)
        self.web_clicked_frame = tk.Frame(self.container_frame)

        # sort frames into lists by typed or clicked
        self.toggled_frames_typed = [self.angle_typed_frame, self.poly_typed_frame, self.web_typed_frame]
        self.toggled_frames_clicked = [self.angle_clicked_frame, self.poly_clicked_frame, self.web_clicked_frame]

        for i in range(3):
            # create labels for each of the six frames
            t_label = tk.Label(self.toggled_frames_typed[i], text="Enter Vertices")
            c_label = tk.Label(self.toggled_frames_clicked[i], text="Click to Enter Vertices")
            xy = tk.Label(self.toggled_frames_typed[i], text="(x, y)")
            xy2 = tk.Label(self.toggled_frames_clicked[i], text="(x, y)")

            # grid labels to frame
            t_label.grid(row=0, columnspan=3)
            c_label.grid(row=0, columnspan=3)
            xy.grid(row=1, column=1, columnspan=2)
            xy2.grid(row=1, column=1, columnspan=2)

        # create angle frames widgets
        self.create_typed_widgets(3, self.angle_typed_frame, self.angle_vertices_entries, False)
        self.create_clicked_widgets(3, self.angle_clicked_frame, self.angle_vertices_labels, False)
        # create web frames widgets
        self.create_typed_widgets(4, self.web_typed_frame, self.web_vertices_entries, True)
        self.create_clicked_widgets(4, self.web_clicked_frame, self.web_vertices_labels, True)

        # polygons: Entry boxes get created only after user enters # sides for the polygon (calls enter_poly_sides_num)
        self.poly_sides_label = tk.Label(self.poly_typed_frame, text="Enter the number of \nsides in polygon: ")
        self.poly_sides_entry = tk.Entry(self.poly_typed_frame, width=5, validate="key")
        self.poly_sides_entry.configure(validatecommand=(self.poly_sides_entry.register(self.validate_input), '%P', '%d'))
        self.poly_sides_button = tk.Button(self.poly_typed_frame, text="Submit",
                                           command=lambda: self.enter_poly_sides_num())

        self.poly_sides_label.grid(row=0, column=0)
        self.poly_sides_entry.grid(row=0, column=1)
        self.poly_sides_button.grid(row=0, column=2)

        # have the angle typed frame be default
        self.angle_typed_frame.grid()

    def enter_poly_sides_num(self):
        """
        Gets user input for the number of sides of polygon
        Draws the polygon only if the user has entered a number
        between 3 and 12
        """
        text = self.poly_sides_entry.get()
        if text == '':
            messagebox.showwarning(title="Nothing Entered", message="Please enter a value.")
        else:
            num_vertices = int(text)
            if num_vertices < 3:
                messagebox.showwarning(title="Improper Polygon", message="A polygon must have at least 3 vertices.")
            elif num_vertices > 12:
                messagebox.showwarning(title="Improper Polygon", message="A dodecagon is the greatest you can draw!")
            else:
                # clear the previously existing widgets on the poly_frame every time user enters a new number of sides
                self.clear_polygon_widgets()
                self.create_typed_widgets(num_vertices, self.poly_typed_frame,
                                          self.poly_vertices_entries, False)

    def create_typed_widgets(self, num_vertices, frame, entries_list, is_web):
        """
        Creates widgets for 'typed' frames
        """
        for v in range(num_vertices):
            new_label = tk.Label(frame, text="Enter vertex " + str(v + 1) + ": ")
            # if the shape is a web, change the labels printed to delineate axes rather than vertices
            if is_web:
                new_label.config(text=self.web_msgs[v])
            new_label.grid(row=v + 2, column=0)
            if self.shape_svar.get() == 'poly':
                # store the side labels for polygons because a user may resubmit the # side before drawing or clearing
                self.poly_each_vertex_labels.append(new_label)

            entry_x = tk.Entry(frame, width=4, validate="key")
            entry_x.configure(validatecommand=(entry_x.register(self.validate_input), '%P', '%d'))
            entry_y = tk.Entry(frame, width=4, validate="key")
            entry_y.configure(validatecommand=(entry_x.register(self.validate_input), '%P', '%d'))
            entries_list.append([entry_x, entry_y])

            entry_x.grid(row=v + 2, column=1)
            entry_y.grid(row=v + 2, column=2)

    def create_clicked_widgets(self, num_vertices, frame, labels_list, is_web):
        """
        Creates widgets on 'clicked' frames for angles and webs ONLY and stores the labels into a list,
        which will be updated when the user clicks on the canvas to choose coordinates
        """
        for v in range(num_vertices):
            new_label = tk.Label(frame, text="Enter vertex: " + str(v + 1))
            if is_web:
                new_label.config(text=self.web_msgs[v])
            xy_label = tk.Label(frame, text='')
            labels_list.append(xy_label)

            new_label.grid(row=v + 2, column=0)
            xy_label.grid(row=v + 2, column=1, columnspan=2)

    def create_line_of_widgets(self, mouse_click_counter_):
        """
        Creates widgets for poly clicked frame.
        One line of Enter Vertex: label and blank label to hold the coordinates
        for the polygon_clicked_frame
        """
        new_label = tk.Label(self.poly_clicked_frame, text="Enter vertex: " + str(mouse_click_counter_ + 1))
        xy_label = tk.Label(self.poly_clicked_frame, text='')
        self.poly_vertices_labels.append(xy_label)
        self.lines_of_poly_widgets.append(new_label)

        new_label.grid(row=mouse_click_counter_ + 2, column=0)
        xy_label.grid(row=mouse_click_counter_ + 2, column=1, columnspan=2)

    def clear_polygon_widgets(self):
        """
        Destroys all widgets (Vertex #: -- -- )
        on the poly frame so that they can be recreated with
        a different number each time, also clears the lists that
        they're held in
        """
        # destroys the x and y input Entry boxes
        for entry in self.poly_vertices_entries:
            entry[0].destroy()
            entry[1].destroy()
        # clears the list that holds the entry boxes
        self.poly_vertices_entries.clear()
        # destroys the "(x, y)" user input values labels
        for entry in self.poly_vertices_labels:
            entry.destroy()
        self.poly_vertices_labels.clear()
        # destroy the "Vertex 1:, Vertex 2:.." labels to the sides of the Entry boxes
        for entry in self.poly_each_vertex_labels:
            entry.destroy()
        self.poly_each_vertex_labels.clear()


    def create_buttons(self):
        """
        Creates the buttons to choose color, choose number
        of segments, draw to screen, and clear canvas
        """
        self.random_on_off = tk.IntVar()
        self.random_on_off.set(1)  # sets default to checked
        self.buttons_frame = tk.Frame(self.base_frame2)
        self.color_checkbox = tk.Checkbutton(self.buttons_frame, text="Randomize color", variable=self.random_on_off,
                                             command=self.set_random_color)
        self.color_button = tk.Button(self.buttons_frame, text="Set Color", width=10, command=self.choose_color)
        self.color_label = tk.Label(self.buttons_frame, text='Color = ???', width=15)

        self.segment_label = tk.Label(self.buttons_frame, text="Enter the number\nof segments:")
        self.segment_entry = tk.Entry(self.buttons_frame, width=5, validate="key")
        self.segment_entry.insert(0, '20')
        self.segment_entry.configure(validatecommand=(self.segment_entry.register(self.validate_input), '%P', '%d'))

        self.draw_button = tk.Button(self.buttons_frame, text="Draw", width=10,
                                     command=lambda: self.draw_btn_clicked(self.shape_svar.get(), self.input_svar.get()))
        self.clear_button = tk.Button(self.buttons_frame, text="Clear canvas", width=10, command=self.clear_canvas)

        self.buttons_frame.grid(row=3, column=0)
        # self.buttons_frame.pack()
        self.segment_label.grid(row=1, column=0, )
        self.segment_entry.grid(row=1, column=1, pady=5)
        self.color_checkbox.grid(row=2, column=0, pady=5, padx=5)
        self.color_button.grid(row=2, column=1, pady=5, padx=5)
        self.color_label.grid(row=3, column=0, columnspan=2, pady=5, padx=5)
        self.draw_button.grid(row=4, column=0, pady=10, padx=5)
        self.clear_button.grid(row=4, column=1, pady=10, padx=5)


    def create_status_bar(self):
        self.status_bar_text = tk.StringVar()
        self.mouse_location = tk.StringVar()
        self.canvas.bind("<Motion>", self.track_mouse)
        self.status_bar = tk.Label(self.master, textvariable=self.status_bar_text, bd=1, relief='sunken', anchor='w')
        self.status_bar.grid(row=1, columnspan=2, sticky='ew')

    """
     ****************************
     **** end create methods ****
     ****************************
    """

    def validate_input(self, entry_value, toa):
        """
        Prevents the user from entering anything other than digits
        in entry boxes
        """
        if toa == '1':
            if not entry_value.isdigit():
                return False
        return True

    def clear_circles(self):
        """
        Checks if there are any circle objects on the canvas
        and deletes them
        """
        if len(self.circle_ids) > 0:
            for i in range(len(self.circle_ids)):
                self.canvas.delete(self.circle_ids[i])
                self.canvas.delete(self.label_ids[i])
        self.circle_ids.clear()
        self.label_ids.clear()

    def toggle_input_view(self, shape_rb, input_rb):
        """
        toggles between the six input view frames
        """
        # reset mouse_click_counter to 0
        self.mouse_click_counter = 0
        # clear circles from canvas, if any
        self.clear_circles()

        if input_rb == 'typed':
            self.angle_clicked_frame.grid_forget()
            self.poly_clicked_frame.grid_forget()
            self.web_clicked_frame.grid_forget()
            if shape_rb == 'angle':
                self.angle_typed_frame.grid()
                self.poly_typed_frame.grid_forget()
                self.web_typed_frame.grid_forget()
            elif shape_rb == 'poly':
                self.angle_typed_frame.grid_forget()
                self.poly_typed_frame.grid()
                self.web_typed_frame.grid_forget()
            else:  # shape_rb == 'web'
                self.angle_typed_frame.grid_forget()
                self.poly_typed_frame.grid_forget()
                self.web_typed_frame.grid()

        else:  # if input_rb == 'clicked':
            # bind mouse click actions to the canvas
            self.canvas.bind('<Button-1>', lambda event: self.handle_mouse_clicks(event))
            self.angle_typed_frame.grid_forget()
            self.poly_typed_frame.grid_forget()
            self.web_typed_frame.grid_forget()
            if shape_rb == 'angle':
                self.angle_clicked_frame.grid()
                self.poly_clicked_frame.grid_forget()
                self.web_clicked_frame.grid_forget()
            elif shape_rb == 'poly':
                self.angle_clicked_frame.grid_forget()
                self.poly_clicked_frame.grid()
                self.web_clicked_frame.grid_forget()
            else:  # shape_rb == 'web'
                self.angle_clicked_frame.grid_forget()
                self.poly_clicked_frame.grid_forget()
                self.web_clicked_frame.grid()

    def handle_mouse_clicks(self, event):
        x, y = event.x, event.y

        if self.input_svar.get() == 'clicked' and self.shape_svar.get() == 'angle':
            if self.mouse_click_counter < 3:
                self.mouse_click_counter += 1
                # update the labels as mouse is clicked
                self.angle_vertices_labels[self.mouse_click_counter - 1].config(text="(%d, %d)" % (x, y))
                self.temp_clicked_values.append((x, y))
                # draw the circle object to the canvas
                self.angle_circle.set_text('P' + str(self.mouse_click_counter))
                self.angle_circle.set_color('blue')
                self.angle_circle.draw_circle(event)
        elif self.input_svar.get() == 'clicked' and self.shape_svar.get() == 'poly':
            if self.mouse_click_counter < 12:
                self.create_line_of_widgets(self.mouse_click_counter)
                self.mouse_click_counter += 1
                # update the labels as mouse is clicked
                self.poly_vertices_labels[self.mouse_click_counter - 1].config(text="(%d, %d)" % (x, y))
                self.temp_clicked_values.append([x, y])
                self.poly_circle.set_text('P' + str(self.mouse_click_counter))
                self.poly_circle.set_color('red')
                self.poly_circle.draw_circle(event)
        elif self.input_svar.get() == 'clicked' and self.shape_svar.get() == 'web':
            if self.mouse_click_counter < 4:
                self.mouse_click_counter += 1
                # update the labels as mouse is clicked
                self.web_vertices_labels[self.mouse_click_counter - 1].config(text="(%d, %d)" % (x, y))
                self.temp_clicked_values.append([x, y])
                self.web_circle.set_text('P' + str(self.mouse_click_counter))
                self.web_circle.set_color('green')
                self.web_circle.draw_circle(event)

    def draw_btn_clicked(self, shape_, input_):
        """
        Called when 'Draw' Button is clicked.
        splits into typed or clicked cases.
        """
        if input_ == 'typed':
            self.handle_typed_input(shape_)
            self.clear_polygon_widgets()
            # neccesary along with .clear_polygon_widgets() to catch the bug
            # of clicked poly labels not clearing between toggles
            self.destroy_poly_child_widgets()
        else:
            self.handle_clicked_input(shape_)
            self.clear_polygon_widgets()
            self.destroy_poly_child_widgets()

    def destroy_poly_child_widgets(self):
        children = self.poly_clicked_frame.winfo_children()
        for child in children:
            child.destroy()
        self.poly_vertices_entries.clear()
        self.poly_each_vertex_labels.clear()
        self.poly_each_vertex_labels.clear()

    def draw_shape(self, shape_, user_input_list_):
        """
        Param: shape specified, list of coordinates
        Draws indicated shape to canvas.
        """
        if self.segment_entry.get() == '':
            seg = 20
        else:
            seg = int(self.segment_entry.get())
        if self.random_on_off.get() == 1:
            self.color = '#' + ''.join([random.choice('0123456789ABCDEF') for i in range(6)])

        if shape_ == 'angle':
            new_angle = Angle(user_input_list_, seg, self.color)
            new_angle.fill_angle(self.canvas)
        elif shape_ == 'poly':
            new_poly = Polygon(user_input_list_, seg, self.color)
            new_poly.fill_polygon(self.canvas)
        else:
            new_web = Web(user_input_list_, seg, self.color)
            # draw web only if lines intersect on canvas
            if new_web.get_point_of_int() is None:
                tk.messagebox.showwarning(title="Non-Intersecting Lines",
                                          message="Your lines do not intersect. Please try again.")
            else:
                new_web.fill_web(self.canvas)

    def return_validated_and_converted_vals_(self, entries_list_):
        """
        Returns the list containing strings as a list of ints after
        checking to see if they are within range of canvas.
        """
        int_converted_vals = []
        if self.validate_coord_range(entries_list_):
            for pair in entries_list_:
                # convert to int and put into list
                _x = int(pair[0].get())
                _y = int(pair[1].get())
                int_converted_vals.append((_x, _y))
            return int_converted_vals
        else:
            return 'invalid'

    def handle_typed_input(self, shape_):
        """
        Validates the range of the user inputted coordinates
        then passes the int values to the Shape constructor to
        draw the object to canvas.
        """
        if shape_ == 'angle':
            passed_list = self.angle_vertices_entries
        elif shape_ == 'poly':
            passed_list = self.poly_vertices_entries
        else:
            passed_list = self.web_vertices_entries

        validated_list = self.return_validated_and_converted_vals_(passed_list)
        if validated_list != 'invalid':
            # create the object
            self.draw_shape(shape_, validated_list)
        # clear the entries boxes
        self.clear_text(passed_list)


    def handle_clicked_input(self, shape_):
        """

        """
        if shape_ == 'angle':
            passed_list = self.angle_vertices_labels
        elif shape_ == 'poly':
            passed_list = self.poly_vertices_labels
            # destroy all lines of poly widgets
            for widget in self.lines_of_poly_widgets:
                widget.destroy()
            # and clear the list
            self.lines_of_poly_widgets.clear()
            self.poly_vertices_labels.clear()
        else:
            passed_list = self.web_vertices_labels

        self.draw_shape(shape_, self.temp_clicked_values)
        self.clear_labels(passed_list)
        # clear the user input list
        self.temp_clicked_values.clear()
        # reset mouse click
        self.mouse_click_counter = 0
        # delete all clicked circles from canvas
        self.clear_circles()

    def validate_coord_range(self, _entries):
        try:
            for pair in _entries:
                _x = int(pair[0].get())
                _y = int(pair[1].get())
                if _x < 0:
                    return False
                elif _x >= CANVAS_SIZE:
                    return False
                elif _y < 0:
                    return False
                elif _y >= CANVAS_SIZE:
                    return False
            return True
        except ValueError:
            messagebox.showwarning(title="Invalid Entry", message="Please enter valid values!")

    def set_segments(self):
        """
        Gets user input for the number of segments for
        the shape. Default is 20.
        """
        text = self.segment_entry.get()
        if text == '':
            self.segment = 20
        else:
            converted_val = int(text)
            self.segment = converted_val

    def choose_color(self):
        """
        Has the user choose the color
        """
        self.color = colorchooser.askcolor()[1]  # get the hex color
        # set color_label bg
        self.color_label.config(bg=self.color)
        self.color_label.config(text='My color', fg='black')
        self.color_checkbox.deselect()


    def set_random_color(self):
        """
        sets a random color each time the shape is drawn
        """
        if self.random_on_off.get() == 1:  # if user has checked random color
            # set color_label text and restores the default color
            self.color_label.config(text="Color = ???", fg='black')
            self.color_label.config(bg='SystemButtonFace')
        else:
            self.color_label.config(text="Default color", fg='white')
            self.color_label.config(bg='black')
            self.color = 'black'

    def update_statusbar(self, a, b, c):
        newtext = self.mouse_location.get()
        self.status_bar_text.set(newtext)

    def track_mouse(self, event):
        self.mouse_location.set("Canvas coordinates: x: %d, y: %d" % (event.x, event.y))
        self.mouse_location.trace('w', self.update_statusbar)

    def clear_text(self, user_input):
        for pair in user_input:
            pair[0].delete(0, 'end')
            pair[1].delete(0, 'end')

    def clear_labels(self, labels_list):
        for label in labels_list:
            label.config(text='')

    def clear_canvas(self):
        # clear the canvas
        self.canvas.delete('all')
        # clear all the Entry boxes
        self.clear_text(self.angle_vertices_entries)
        self.clear_text(self.poly_vertices_entries)
        self.clear_text(self.web_vertices_entries)
        # clear all labels
        for label in self.angle_vertices_labels:
            label.config(text='')
        for label in self.poly_vertices_labels:
            label.config(text='')
        for label in self.web_vertices_labels:
            label.config(text='')
        # reset the mouse clicks and list to store clicked values at 0
        self.mouse_click_counter = 0
        self.temp_clicked_values.clear()
        # destroy the lines of widgets in poly_clicked frames to clear the window
        for widget in self.lines_of_poly_widgets:
            widget.destroy()




def main():
    root = tk.Tk()
    ma = MainApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
