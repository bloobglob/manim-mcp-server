from manim import *

class PythagoreanTheorem(Scene):
    def construct(self):
        theorem = MathTex(r"a^2 + b^2 = c^2", font_size=48, color=GOLD)
        theorem.to_edge(UP)
        self.play(Write(theorem))
        self.wait(1)
        
        P = np.array([-3, -3, 0])
        Q = np.array([-3, 3, 0])
        R = np.array([3, 3, 0])
        S = np.array([3, -3, 0])
        
        W = np.array([-3, -3/7, 0])
        X = np.array([-3/7, 3, 0])
        Y = np.array([3, 3/7, 0])
        Z = np.array([3/7, -3, 0])
        
        ab_square = Polygon(P, Q, R, S, color=WHITE, fill_opacity=0.2, fill_color=BLUE)
        c_square = Polygon(W, X, Y, Z, color=WHITE, fill_opacity=0.2, fill_color=RED)
        
        self.play(Create(ab_square))
        self.wait(1)
        self.play(Create(c_square))
        
        labels_a = [MathTex("a", font_size=48, color=WHITE).next_to(Line(P, W).get_center(), LEFT, buff=0.1),
                    MathTex("a", font_size=48, color=WHITE).next_to(Line(Q, X).get_center(), UP, buff=0.1),
                    MathTex("a", font_size=48, color=WHITE).next_to(Line(R, Y).get_center(), RIGHT, buff=0.1),
                    MathTex("a", font_size=48, color=WHITE).next_to(Line(S, Z).get_center(), DOWN, buff=0.1)]
        
        labels_b = [MathTex("b", font_size=48, color=WHITE).next_to(Line(W, Q).get_center(), LEFT, buff=0.1),
                    MathTex("b", font_size=48, color=WHITE).next_to(Line(X, R).get_center(), UP, buff=0.1),
                    MathTex("b", font_size=48, color=WHITE).next_to(Line(Y, S).get_center(), RIGHT, buff=0.1),
                    MathTex("b", font_size=48, color=WHITE).next_to(Line(Z, P).get_center(), DOWN, buff=0.1)]
        
        labels_c = [MathTex("c", font_size=48, color=WHITE).next_to(Line(W, X).get_center(), LEFT, buff=0.1),
                    MathTex("c", font_size=48, color=WHITE).next_to(Line(X, Y).get_center(), UP, buff=0.1),
                    MathTex("c", font_size=48, color=WHITE).next_to(Line(Y, Z).get_center(), RIGHT, buff=0.1),
                    MathTex("c", font_size=48, color=WHITE).next_to(Line(Z, W).get_center(), DOWN, buff=0.1)]
        
        self.play(*[Write(label) for label in labels_a])
        self.wait(1)
        self.play(*[Write(label) for label in labels_b])
        self.wait(1)
        self.play(*[Write(label) for label in labels_c])
        self.wait(1)
        
        derivation = [
            Text(r"area(big square) = area(four triangles) + area(small square)", font_size=36),
            MathTex(r"(a+b)^2=4*\frac{1}{2}ab+c^2", font_size=36),
            MathTex(r"a^2+2ab+b^2=2ab+c^2", font_size=36),
            MathTex(r"a^2+b^2=c^2", font_size=36, color=GREEN)
        ]
        
        for i, line in enumerate(derivation):
            if i == 0:
                line.to_edge(RIGHT)
            else:
                line.next_to(derivation[i-1], DOWN, buff=0.2)
            self.play(Write(line))
            self.wait(1)
            
        self.wait(1)

from manim import *

class Main(Scene):
    def construct(self):
        # create objects
        P = np.array([1, 3, 0])
        Q = np.array([2, 2, 0])
        R = np.array([3, 1, 0])
        S = np.array([4, 0, 0])
        square = Polygon(P, Q, R, S, color=BLUE, fill_opacity=0.2, fill_color=BLUE)

        # create labels
        n = MathTex("n", font_size=48, color=WHITE).next_to(Line(P, S).get_center(), LEFT, buff=0)
        sum_n = MathTex(r"1+2+3+\cdots+n=\frac{n(n+1)}{2}", font_size=36, color=WHITE).next_to(square, UP, buff=1)

        # create derivation
        derivation = [
            MathTex(r"1+2+3+\cdots+n", font_size=36),
            MathTex(r"=1+2+3+\cdots+n", font_size=36),
            MathTex(r"=\frac{n(n+1)}{2}", font_size=36, color=GREEN)
        ]
        for i, line in enumerate(derivation):
            if i == 0:
                line.move_to(np.array([4, 3, 0]))
            else:
                line.next_to(derivation[i-1], DOWN, buff=0.2)

        # animate objects
        self.play(Create(square))
        self.wait(1)

        # animate labels
        self.play(Write(n))
        self.wait(1)

        # animate derivation
        for line in derivation:
            self.play(Write(line))
            self.wait(1)