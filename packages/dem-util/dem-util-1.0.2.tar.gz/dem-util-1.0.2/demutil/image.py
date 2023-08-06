from demutil.util import vector_to_radian
# from PIL import Image, ImageDraw, ImageOps
import cairocffi as cairo
import math
import io
from scour import scour


__COLORS__ = [
    (33/255, 93/255, 60/255, 204/255),
    (29/255, 164/255, 79/255, 204/255),
    (71/255, 208/255, 69/255, 204/255),
    (155/255, 231/255, 65/255, 204/255),
    (245/255, 216/255, 48/255, 204/255),
    (245/255, 162/255, 48/255, 204/255),
    (245/255, 94/255, 48/255, 204/255),
    (245/255, 48/255, 48/255, 204/255)
]


def draw_path(context, path):
    context.move_to(path.coords[0][0], path.coords[0][1])
    for pt in path.coords[1:]:
        context.line_to(pt[0], pt[1])
    context.close_path()


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
    # start = vectors[0][0:2]
    # end = vectors[-1][0:2]
    #
    # resolution = end - start
    # width = int(resolution[0])
    # height = int(resolution[1])

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

    # clip 영역 설정
    # draw_path(context, shape.exterior)
    draw_polygon(context, shape)
    context.clip()

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

    # 윤곽선 그리기
    context.set_source_rgb(0.0, 123/255, 1.0)
    context.set_line_width(2.0)
    draw_polygon(context, shape)
    context.stroke()

    # surface 에 그리기
    surface.finish()

    # optimization
    # print("Start optimization...")
    options = scour.sanitizeOptions(options=None)
    options.remove_metadata = True
    options.remove_descriptive_elements = True
    options.strip_comments = True
    options.enable_viewboxing = True
    options.indent_type = None
    options.newlines = False
    options.strip_ids = True
    options.shorten_ids = True
    options.strip_xml_prolog = True
    options.digits = 3

    source = svg.getvalue().decode()
    output = scour.scourString(source, options)

    # print(len(source), len(output), len(output)/len(source)*100)

    return output


# def get_image(shape, vectors):
#     start = vectors[0][0:2]
#     end = vectors[-1][0:2]
#
#     resolution = end - start
#
#     img = Image.new("RGBA", (int(resolution[0]), int(resolution[1])))
#     height = Image.new("RGBA", (int(resolution[0]), int(resolution[1])))
#     img1 = ImageDraw.Draw(height)
#
#     mask = Image.new("RGBA", (int(resolution[0]), int(resolution[1])), color="#ffffff")
#     img2 = ImageDraw.Draw(mask)
#
#     for pos in vectors:
#         x = pos[0] - start[0]
#         y = pos[1] - start[1]
#
#         slope = math.degrees(vector_to_radian(pos[3:6]))
#         idx = ((slope - 10.0) / 5.0)
#         idx = 0 if idx < 0 else 7 if idx > 7 else idx
#         img1.rectangle([(x, y), (x + 10, y + 10)], fill=__COLORS__[int(idx)])
#         # img1.polygon([x+2, y+8, x+8, y+5, x+5, y+5, x+5, y+2, x+2, y+8], fill=white)
#
#     shp = [(int(round(x[0] - start[0])), int(round(x[1] - start[1]))) for x in shape.exterior.coords]
#
#     img2.polygon(shp, fill=0)
#
#     img = Image.composite(img, height, mask)
#     img3 = ImageDraw.Draw(img)
#     img3.line(shp, fill="#007BFF", width=5, joint="round")
#     img = ImageOps.flip(img)
#
#     return img
