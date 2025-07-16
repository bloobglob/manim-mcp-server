

from manim import *
from mylib import *

class Main(Scene):
    def construct(self):
        # method goes here
        play_pythag_proof(scene=self)
        # derivation goes here
        play_deriv(r"A_{big square} = A_{four triangles} + A_{small square}", r"A_{big square} = 4 \cdot \frac{1}{2}ab + c^2", r"A_{big square} = 2ab + c^2", r"A_{big square} = (a+b)^2", r"(a+b)^2 = 2ab + c^2", r"a^2 + 2ab + b^2 = 2ab + c^2", r"a^2 + b^2 = c^2", scene=self)
