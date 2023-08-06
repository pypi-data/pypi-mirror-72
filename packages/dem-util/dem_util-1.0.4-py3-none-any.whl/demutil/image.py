from demutil.util import vector_to_radian
import cairocffi as cairo
import math
import io


__alpha__ = 0.8


__COLORS__ = [
    (33/255, 93/255, 60/255, __alpha__),
    (29/255, 164/255, 79/255, __alpha__),
    (71/255, 208/255, 69/255, __alpha__),
    (155/255, 231/255, 65/255, __alpha__),
    (245/255, 216/255, 48/255, __alpha__),
    (245/255, 162/255, 48/255, __alpha__),
    (245/255, 94/255, 48/255, __alpha__),
    (245/255, 48/255, 48/255, __alpha__)
]


def draw_polygon(context, shape):
    path = shape.exterior
    context.move_to(path.coords[0][0], path.coords[0][1])
    for pt in path.coords[1:]:
        context.line_to(pt[0], pt[1])

    for path in shape.interiors:
        context.move_to(path.coords[0][0], path.coords[0][1])
        for pt in path.coords[1:]:
            context.line_to(pt[0], pt[1])

    context.close_path()


def get_image(shape, vectors):
    bound = shape.bounds
    start = [bound[0], bound[1]]
    width = bound[2] - bound[0]
    height = bound[3] - bound[1]

    # Create Image Surface
    svg = io.BytesIO()
    surface = cairo.SVGSurface(svg, width, height)
    # surface = cairo.SVGSurface("test.svg", width, height)
    context = cairo.Context(surface)

    # 상하 flip
    context.translate(0, height)
    context.scale(1, -1)

    # origin point 설정
    context.translate(-start[0], -start[1])

    context.set_source_rgb(1.0, 1.0, 1.0)
    context.paint()

    # box 그리기
    for pos in vectors:
        x = pos[0]
        y = pos[1]

        slope = math.degrees(vector_to_radian(pos[3:6]))
        idx = ((slope - 10.0) / 5.0)
        idx = 0 if idx < 0 else 7 if idx > 7 else idx
        context.set_source_rgba(*__COLORS__[int(idx)])
        context.rectangle(x, y, 10, 10)
        context.fill()

    # 외곽 흐리게 처리
    context.move_to(start[0], start[1])
    context.line_to(start[0]+width, start[1])
    context.line_to(start[0]+width, start[1]+height)
    context.line_to(start[0], start[1]+height)
    context.line_to(start[0], start[1])
    draw_polygon(context, shape)
    context.clip()

    context.set_source_rgba(1.0, 1.0, 1.0, 0.8)
    context.paint()

    # 윤곽선 그리기
    context.reset_clip()

    context.set_source_rgb(0.0, 123/255, 1.0)
    context.set_line_width(2.0)
    draw_polygon(context, shape)
    context.stroke()

    surface.finish()

    # optimization
    # print("Start optimization...")
    # options = scour.sanitizeOptions(options=None)
    # options.remove_metadata = True
    # options.remove_descriptive_elements = True
    # options.strip_comments = True
    # options.enable_viewboxing = True
    # options.indent_type = None
    # options.newlines = False
    # options.strip_ids = True
    # options.shorten_ids = True
    # options.strip_xml_prolog = True
    # options.digits = 3

    source = svg.getvalue().decode()
    # output = scour.scourString(source, options)

    return source
