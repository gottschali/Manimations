from manimlib.imports import *

class AxisMarker(RegularPolygon):
    def __init__(self, x_axis=True):
        start_angle = TAU / 4 if x_axis else 0
        super().__init__(n=3, start_angle=start_angle)
        self.set_fill(WHITE, 1)
        self.set_stroke(width=0)
        self.scale(0.1)

class Point:
    def __init__(self, graph, x=0):
        self.graph = graph
        self.update(x)

    def update(self, x):
        self.x = x
        self.y = self.graph.underlying_function(x)


class PlotGraph(GraphScene):
    y_max = 9
    y_min = -1
    x_max = 6
    x_min = -1
    function = lambda x: 1 - x**2 + 2**x
    error = 0.001
    CONFIG = {
        "y_max" : y_max,
        "y_min" : y_min,
        "x_max" : x_max,
        "x_min" : x_min,
        "y_tick_frequency" : 1,
        "x_tick_frequency" : 1,
        "axes_color" : BLUE,
        "y_labeled_nums": range(y_min, y_max, 2),
        "x_labeled_nums": range(x_min, x_max, 2),
        "x_label_decimal": 1,
        "graph_origin": 2.5*LEFT+2*DOWN,
        "x_label_direction": DOWN,
        "y_label_direction": RIGHT,
        "x_axis_label": None,
        "x_axis_width": 10,
    }

    def construct(self):
        self.setup_axes(animate=False) #animate=True to add animation
        self.y_axis_label_mob.next_to(self.y_axis[0].get_end(),UP)

        def get_x_point(point):
            return self.coords_to_point(point.x, 0)

        def get_y_point(point):
            return self.coords_to_point(0, point.y)

        def get_graph_point(point):
            return self.coords_to_point(point.x, point.y)

        def get_v_line(point):
            return DashedLine(get_x_point(point), get_graph_point(point), stroke_width=2)

        def get_h_line(point):
            return DashedLine(get_graph_point(point), get_y_point(point), stroke_width=2)

        def get_t_line(point):
            return Line(get_graph_point(point),
                    self.coords_to_point(x_intercept(point), 0), stroke_width=2)

        def derivative(x, func, dx=0.001):
            return (func(x+dx)-func(x))/dx

        def get_new_newton_point(point):
            p = Point(graph)
            p.update(point.x - point.y / derivative(point.x, PlotGraph.function))
            return p

        def get_slope_line(point):
            return self.get_secant_slope_group(
                x=point.x,
                graph=graph,
                dx=0.001,
                secant_line_color=RED,
                secant_line_length=20
            ).secant_line

        graph = self.get_graph(PlotGraph.function, color = GREEN)

        # Setup Initial guess
        p1 = Point(graph, 0.9)
        input_triangle_p1 = AxisMarker(x_axis=True)
        output_triangle_p1 = AxisMarker(x_axis=False)
        x_label_p1 = TexMobject("x_0")
        output_label_p1 = TexMobject("f(x_0)")
        v_line_p1 = get_v_line(p1)
        h_line_p1 = get_h_line(p1)
        graph_dot_p1 = Dot(color=YELLOW)
        x_label_p1.next_to(v_line_p1, 2*DOWN)
        output_label_p1.next_to(h_line_p1, 2*LEFT)
        input_triangle_p1.next_to(v_line_p1, DOWN, buff=0)
        output_triangle_p1.next_to(h_line_p1, LEFT, buff=0)
        graph_dot_p1.move_to(get_graph_point(p1))

        # Draw Graph
        self.play(
            ShowCreation(graph),
            run_time = 2
        )
        # Animate first guess
        self.play(
            DrawBorderThenFill(input_triangle_p1),
            Write(x_label_p1),
            ShowCreation(v_line_p1),
            ShowCreation(h_line_p1),
            DrawBorderThenFill(output_triangle_p1),
            Write(output_label_p1),
            GrowFromCenter(graph_dot_p1),
            run_time=0.5
            )

        # Iterate
        p_old = p1
        p_new = get_new_newton_point(p1)
        i = 1
        print(p_old.x, p_new.x)
        while abs(p_new.x-p_old.x) > PlotGraph.error:
            print(i, p_old.x, p_new.x)
            p_new = get_new_newton_point(p_old)

            input_triangle_p_new = AxisMarker(x_axis=True)
            output_triangle_p_new = AxisMarker(x_axis=False)

            x_label_p_new = TexMobject(f"x_{i}")
            output_label_p_new = TexMobject(f"f(x_{i})")

            v_line_p_new = get_v_line(p_new)
            h_line_p_new = get_h_line(p_new)

            slope_line = get_slope_line(p_old)

            graph_dot_p_new = Dot(color=YELLOW)
            graph_dot_intercept = Dot(color=YELLOW)

            # reposition mobjects
            x_label_p_new.next_to(v_line_p_new, 2*DOWN)
            output_label_p_new.next_to(h_line_p_new, 2*LEFT)

            input_triangle_p_new.next_to(v_line_p_new, DOWN, buff=0)
            output_triangle_p_new.next_to(h_line_p_new, LEFT, buff=0)

            graph_dot_intercept.move_to(get_x_point(p_new))
            graph_dot_p_new.move_to(get_graph_point(p_new))

            # TODO fadout noise

            self.play(GrowFromPoint(slope_line, get_graph_point(p1)))
            self.play(GrowFromCenter(graph_dot_intercept))
            self.play(GrowFromPoint(v_line_p_new, get_x_point(p_new)))
            self.play(
                DrawBorderThenFill(input_triangle_p_new),
                Write(x_label_p_new),
                # ShowCreation(h_line_p_new),
                DrawBorderThenFill(output_triangle_p_new),
                Write(output_label_p_new),
                GrowFromCenter(graph_dot_p_new),
            )
            self.wait(1)
            i += 1
            p_temp = p_new
            p_old = p_temp
            p_new = get_new_newton_point(p_temp)
        print(i, p_old.x, p_new.x)


