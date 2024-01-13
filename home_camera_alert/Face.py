from dataclasses import dataclass, field

@dataclass
class Face:
    x_img: float = field(default=0.0)
    y_img: float = field(default=0.0)
    w_img: float = field(default=0.0)
    h_img: float = field(default=0.0)

    def __post_init__(self):
        self.x_img = int(self.x_img)
        self.y_img = int(self.y_img)
        self.w_img = int(self.w_img)
        self.h_img = int(self.h_img)

    def first_point(self):
        return [int(self.x_img), int(self.y_img)]
    
    def second_point(self):
        return [int(self.x_img+self.w_img), int(self.y_img)]
    
    def third_point(self):
        return [int(self.x_img), int(self.y_img+self.h_img)]
    
    def fourth_point(self):
        return [int(self.x_img+self.w_img), int(self.y_img+self.h_img)]
