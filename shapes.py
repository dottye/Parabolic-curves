import math

"""
the shapes.py file contains the Circle, Angle, Polygon, and Web classes that 
contain the code to instantiate the objects of those classes. 

"""


class Circle:
    """
    A circle object is drawn to the canvas with its center at the
    coordinates of the mouse click. It has an optional label floating
    to the right and above the circle.
    """
    # class variables
    radius = 5
    text_x_padding = 10
    text_y_padding = 15
    all_circles = []
    all_labels = []

    def __init__(self, canvas, label_text='', color='black'):
        """
        Constructor: instantiates a new Circle object at the x and y location
        of the mouse click event and draws it to the canvas.
        Parameters: mouse-click event, canvas,text of label, and fill color
        Returns: None
        """
        self.x = 0
        self.y = 0
        self.canvas = canvas
        self.label_text = label_text
        self.color = color

    def draw_circle(self, event):
        """
        Positions the circle with the center at the mouse click
        coordinates passed. Draws the circle and label to the canvas.
        """
        self.x = event.x
        self.y = event.y
        start_x = self.x - self.radius
        start_y = self.y - self.radius
        end_x = self.x + self.radius
        end_y = self.y + self.radius
        self.circle = self.canvas.create_oval(start_x, start_y, end_x, end_y, fill=self.color)
        self.all_circles.append(self.circle)  # add the id of the circle object to the list
        self.add_label()

    def add_label(self):
        """
        Positions the label to the right and to the top of the circle.
        Draws the label to the canvas.
        """
        text_x = self.x + self.text_x_padding
        text_y = self.y - self.text_y_padding
        self.label = self.canvas.create_text(text_x, text_y, text=self.label_text)
        self.all_labels.append(self.label)  # add the id of the text object to the list

    def delete_circle(self):
        """
        Deletes the circle and label from the canvas.
        """
        self.canvas.delete(self.circle)
        self.canvas.delete(self.label)

    # setters
    def set_text(self, label_text):
        self.label_text = label_text

    def set_color(self, color):
        self.color = color

    @classmethod
    def get_all_circles(cls):
        """
        returns the list of all circle object ids.
        """
        return cls.all_circles

    @classmethod
    def get_all_labels(cls):
        """
        returns the list of all label (text) object ids.
        """
        return cls.all_labels


class Angle:
    # constructor
    def __init__(self, vertices, segments=30, color='black'):
        self.vertices = vertices
        self.segments = segments
        self.color = color

    @staticmethod
    def calc_slope(point1, point2):
        """
        Input: takes two tuples
        Output: returns a float
        slope = change of x / change of y
        """
        # get x1, y1, x2, y2 from lists
        x1 = point1[0]
        y1 = point1[1]
        x2 = point2[0]
        y2 = point2[1]
        if x1 == x2:
            m = None
        else:
            m = ((y2 - y1) / (x2 - x1)) + 0  # add zero to catch negative zero float
        return m

    @staticmethod
    def calc_distance(point1, point2):
        # get x1, y1, x2, y2 from lists
        x1 = point1[0]
        y1 = point1[1]
        x2 = point2[0]
        y2 = point2[1]

        dx = x2 - x1
        dy = y2 - y1
        d = math.sqrt((dx * dx) + (dy * dy))
        return d

    @staticmethod
    def find_point2(start_point, end_point_of_line, m, d):
        """
        :param start_point:
        :param end_point_of_line:
        :param m: slope
        :param d:
        :return:
        returns one point that is d distance away from start_point,
        lying on the line drawn from start_point to end_point
        """
        x1 = start_point[0]
        y1 = start_point[1]
        if m is None:  # if the line is vertical
            x2 = x1  # x1 and x2 are the same
            # check if vertical line is ascending or descending from start point
            if end_point_of_line[1] > y1:  # y values are increasing, add
                y2 = y1 + d
            else:  # y values are decreasing, subtract
                y2 = y1 - d
        else:  # if line is not vertical
            # determine direction of vector
            if end_point_of_line[0] > x1:  # if x values are increasing, add
                x2 = x1 + d * math.sqrt(1 / (1 + m * m))
            else:  # if x values are decreasing, subtract
                x2 = x1 - d * math.sqrt(1 / (1 + m * m))
            y2 = y1 - m * (x1 - x2)  # modified point-slope formula to find y2

        coord_points = [0, 0]
        # put x2 and y2 into the list
        coord_points[0] = x2
        coord_points[1] = y2

        # return the list
        return coord_points

    def populate_points(self, start_point, end_point):
        """
        returns a list of all points lying on the line drawn by
        start and end points given, with a slope of m, spaced at
        div_units apart.
        """
        m = self.calc_slope(start_point, end_point)
        dist = self.calc_distance(start_point, end_point)
        div_unit = dist / self.segments
        line_list = []
        first_point = self.find_point2(start_point, end_point, m, div_unit)
        line_list.append(first_point)
        for i in range(self.segments - 2):
            some_point = self.find_point2(line_list[i], end_point, m, div_unit)
            line_list.append(some_point)
        return line_list

    def draw_outline(self, canvas):
        pt1 = self.vertices[0]
        center = self.vertices[1]
        pt2 = self.vertices[2]
        canvas.create_line(pt1[0], pt1[1], center[0], center[1],
                           fill=self.color)
        canvas.create_line(pt2[0], pt2[1], center[0], center[1],
                           fill=self.color)

    def draw_curve(self, line1_pts, line2_pts, canvas):
        """
        For a n number of points lying on two lines, draws lines between
        corresponding points of of the two lines.
        """
        for x in range(len(line1_pts)):
            canvas.create_line(line1_pts[x][0], line1_pts[x][1], line2_pts[x][0], line2_pts[x][1],
                               fill=self.color)

    def curve_btw_two_lines(self, pt1, pt2, center, canvas):
        """
        takes three points as parameters that form an angle
        p1, center, p2.
        Draws a parabolic curve on the angle between those two lines.
        """
        # places evenly spaced points all along the lines
        l1_points = self.populate_points(pt1, center)
        l2_points = self.populate_points(pt2, center)
        # reverses the order of the line 2 so that the points of two lines correspond inversely
        l2_points.reverse()
        # draw the lines connecting the points on the lines to form a curve
        self.draw_curve(l1_points, l2_points, canvas)

    def fill_angle(self, canvas):
        """
        Calls the curve_btw_two_lines with the vertices of the instance of the Angle object.
        """
        pt1 = self.vertices[0]
        center = self.vertices[1]
        pt2 = self.vertices[2]
        self.draw_outline(canvas)
        self.curve_btw_two_lines(pt1, pt2, center, canvas)


class Polygon(Angle):
    def __init__(self, vertices, segments, color):
        super().__init__(vertices, segments, color)

    def draw_outline(self, canvas):
        endpoints = self.vertices
        line_color = self.color
        for i in range(len(endpoints)):
            if i == len(endpoints) - 1:  # when i reaches the last point of the endpoints,
                index = 0  #
            else:
                index = i + 1
            canvas.create_line(endpoints[i][0], endpoints[i][1], endpoints[index][0], endpoints[index][1],
                               fill=line_color)

    def fill_polygon(self, canvas):
        """
        For a shape with an unknown number of vertices, populate the empty
        array 'all_lines[]' with the arrays of points that lie on the sides
        of the shape.
        Then draw connecting lines that form the parabolic curve from one
        side to the adjacent side until it reaches the starting point again.
        :param canvas:
        :return:
        """
        self.draw_outline(canvas)
        all_lines = []
        # fill all sides of the polygon with points
        for i in range(len(self.vertices)):
            x = i
            if x == len(self.vertices) - 1:
                y = 0
            else:
                y = i + 1
            single_line = self.populate_points(self.vertices[x], self.vertices[y])
            all_lines.append(single_line)

        # draw connecting lines for all points in all lines to create the curves
        for i in range(len(self.vertices)):
            if i == len(self.vertices) - 1:
                line1 = all_lines[i]
                line2 = all_lines[0]
            else:
                line1 = all_lines[i]
                line2 = all_lines[i + 1]
            self.draw_curve(line1, line2, canvas)


class Web(Angle):
    def __init__(self, vertices, segments, color):
        super().__init__(vertices, segments, color)
        self.ytop = vertices[0]  # top of y axis
        self.ybottom = vertices[1]  # bottom of y axis
        self.xleft = vertices[2]  # left of x axis
        self.xright = vertices[3]  # right of x axis
        self.segments = segments
        self.color = color
        self.point_of_int = self.get_intersection(self.ytop, self.ybottom, self.xleft, self.xright)

    def get_point_of_int(self):
        return self.point_of_int

    @staticmethod
    def get_intersection(ytop, ybottom, xleft, xright):
        """
        takes in four tuples and computes the point of intersection
        code taken and modified from Stack Overflow:
        https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
        returns a tuple for the coord
        """
        line1 = (ytop, ybottom)
        line2 = (xleft, xright)

        xdiff = (ytop[0] - ybottom[0], xleft[0] - xright[0])
        ydiff = (ytop[1] - ybottom[1], xleft[1] - xright[1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        def check_if_int_within_canvas():
            if x < 0:
                return False
            if x > 499:
                return False
            if y < 0:
                return False
            if y > 499:
                return False
            return True

        if check_if_int_within_canvas():
            return x, y
        else:
            return None

    def draw_axes(self, canvas):
        # draws two intersecting lines on canvas
        canvas.create_line(self.ytop[0], self.ytop[1], self.ybottom[0], self.ybottom[1], fill=self.color)
        canvas.create_line(self.xleft[0], self.xleft[1], self.xright[0], self.xright[1], fill=self.color)

    def fill_web(self, canvas):
        """
        draws a 'web' of four parabolic curves around two intersecting lines
        denoted by the four points passed as parameters
        """
        _ytop = self.vertices[0]
        _ybottom = self.vertices[1]
        _xleft = self.vertices[2]
        _xright = self.vertices[3]

        # draw the axes
        self.draw_axes(canvas)
        # draw four parabolic curves for each 'quadrant'
        self.curve_btw_two_lines(_ytop, _xright, self.point_of_int, canvas)  # first quadrant
        self.curve_btw_two_lines(_xright, _ybottom, self.point_of_int, canvas)  # second quadrant
        self.curve_btw_two_lines(_ybottom, _xleft, self.point_of_int, canvas)  # third quadrant
        self.curve_btw_two_lines(_xleft, _ytop, self.point_of_int, canvas)  # fourth quadrant
