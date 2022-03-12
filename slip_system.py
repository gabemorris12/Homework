import sympy as sp
from IPython.display import display, Latex


# noinspection PyTypeChecker
class SlipSystem:
    def __init__(self, force_dir, slip_planes, *slip_dirs, digits=2):
        """
        :param force_dir: An array with 3 items indicating the direction of the force. The magnitude is of no concern.
        :param slip_planes: A list of slip planes.
        :param slip_dirs: Each argument of slip_dirs should be a list of lists in which each list is a slip direction on the plane corresponding to slip_planes
        """

        assert len(slip_planes) == len(slip_dirs), 'Number of slip planes does not match input slip directions.'

        self.F = sp.Matrix(force_dir)
        self.slip_planes = [sp.Matrix(plane) for plane in slip_planes]
        self.slip_dirs = [[sp.Matrix(dir_) for dir_ in plane] for plane in slip_dirs]

        self.n_planes = len(slip_planes)
        self.n_dirs = len(slip_dirs[0])
        self.n = self.n_dirs*self.n_planes

        self.digits = digits

    def get_cos_phi(self, plane):
        plane = self.slip_planes[plane]
        return (self.F.dot(plane)/(self.mag(plane)*self.mag(self.F))).n(self.digits)

    def get_cos_lambda(self, plane, dir_):
        dir_ = self.slip_dirs[plane][dir_]
        return (self.F.dot(dir_)/(self.mag(self.F)*self.mag(dir_))).n(self.digits)

    def generate_table(self, print_=False):
        n = self.n + 1
        lines = [r'\begin{center}',
                 r'\addtolength{\leftskip}{-2cm}',
                 r'\addtolength{\rightskip}{-2cm}',
                 fr'\begin{{tabular}}{{{"l"*n}}}',
                 fr'\multicolumn{{{n}}}{{c}}{{Force Direction: {self.format_vector(self.F)}}} \\',
                 r'\toprule']
        row1 = ['Slip Plane']
        row2 = ['Slip Direction']
        row3 = [r'$\cos(\phi)$']
        row4 = [r'$\cos(\lambda)$']
        row5 = [r'|S.F.|']
        for p, plane in enumerate(self.slip_planes):
            str_plane = self.format_vector(plane, plane=True)
            row1.append(fr'\multicolumn{{{self.n_dirs}}}{{c}}{{{str_plane}}}')
            for d, dir_ in enumerate(self.slip_dirs[p]):
                cos_phi = self.get_cos_phi(p)
                cos_lamb = self.get_cos_lambda(p, d)
                row2.append(self.format_vector(dir_))
                row3.append(str(cos_phi))
                row4.append(str(cos_lamb))
                row5.append(str(sp.Abs(cos_phi*cos_lamb).n(self.digits)))
        lines.append(' & '.join(row1) + r' \\')
        lines.append(r'\midrule')
        [lines.append(' & '.join(row) + r' \\') for row in [row2, row3, row4, row5]]
        lines.extend([r'\end{tabular}', r'\end{center}'])
        latex_string = '\n'.join(lines)
        if print_:
            print(latex_string)
        display(Latex(latex_string))

    @staticmethod
    def format_vector(vector, plane=False):
        items = []
        multiple = any([abs(i) >= 10 for i in vector])
        for i in vector:
            if i >= 0:
                items.append(str(i))
            elif multiple:
                items.append(r'\overline{' + str(abs(i)) + '}')
            else:
                items.append(r'\bar{' + str(abs(i)) + '}')
        if plane:
            head, tail = '$(', ')$'
        else:
            head, tail = '$[', ']$'
        items.insert(0, head)
        items.append(tail)
        if not multiple:
            return ''.join(items)
        return r'\,'.join(items)

    @staticmethod
    def mag(vector):
        return sp.sqrt(sum([value**2 for value in vector]))
