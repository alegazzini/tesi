import cv2
from Face import Face


def resize_text_to_fit(text, font, max_width, max_height, font_scale=1, font_thickness=2):
    # Initialize the font size
    current_font_scale = font_scale

    # Loop until the text fits within the specified rectangle
    while True:
        # Get the size of the text
        text_size = cv2.getTextSize(text, font, current_font_scale, font_thickness)[0]

        # Check if the text fits within the specified rectangle
        if text_size[0] < max_width and text_size[1] < max_height:
            break

        # Reduce the font size
        current_font_scale -= 0.1
        if current_font_scale < 0.1:
            # If the font size becomes too small, break the loop
            break

    return current_font_scale


def drawing_rect_name(face_name: str, face: Face, frame, color: tuple):
    # Drawing: text box with name
    x2_rect_name = int(face.x_img + (face.w_img / 2))
    y2_rect_name = int(face.y_img - (face.w_img / 2 / 3.5))
    w_rect_name = abs(int(face.x_img - x2_rect_name))
    h_rect_name = abs(int(face.y_img - y2_rect_name))
    cv2.rectangle(
        frame,
        face.first_point(), [x2_rect_name, y2_rect_name],
        color,
        -1
    )
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (0, 0, 0)
    font_thickness = 2
    font_scale = resize_text_to_fit(face_name, font, w_rect_name, h_rect_name)
    cv2.putText(frame, face_name, [int(face.x_img), int(face.y_img - h_rect_name / 2)], font, font_scale, font_color,
                font_thickness)

    return frame
