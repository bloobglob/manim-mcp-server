
from manim import *
from mylib import *

class Main(Scene):
    def construct(self):
        play_circ_area_proof(scene=self)
        play_deriv(r"area(big square)=area(small square)+area(four triangles)", scene=self)
        
        # play_pythag_visual(scene=self, a=5, b=12)
        # play_deriv(r"a^2+b^2=c^2", r"3^2+4^2=c^2", r"9+16=c^2", r"25=c^2", r"c=5", scene=self)
        