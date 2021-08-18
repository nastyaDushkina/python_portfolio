# -*- coding: utf-8 -*-

import simple_draw as sd


def get_polygon(n):
    def draw_polygon(start_point=sd.get_point(sd.resolution[0] // 2, sd.resolution[1] // 2), angle=0, length=50):
        angle_step = 360 // n
        point = start_point

        for current_angle in range(0, 360 - angle_step - n, angle_step):
            point = sd.vector(start=point, angle=angle + current_angle, length=length, width=3)

        sd.line(point, start_point, width=3)

    return draw_polygon


draw_triangle = get_polygon(n=3)
draw_triangle(start_point=sd.get_point(200, 200), angle=13, length=200)

sd.pause()
