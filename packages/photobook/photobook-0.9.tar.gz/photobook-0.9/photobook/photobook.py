from fpdf import FPDF
from .cropping import cut_save
from pathlib import Path

class Photobook(FPDF):
    FIG = Path("./fig/")
    OUT = Path("./build/")

    def __init__(self, name,
                 bg_color = (0, 0, 0),
                 txt_color = (255, 255, 255),
                 sep = 3,
                 pdf_size= (24.447, 20.955),
                 page_size = (24.13, 20.32),
                 security_margin_out = 0.635,
                 security_margin_binding = 1.27,
                 base_fig = "./fig/",
                 margin = -1,
                 img_px=1,
                 ):
        super().__init__("P", "mm", pdf_size)
        self.name = name
        self.bg_color = bg_color
        self.txt_color = txt_color
        self.set_fill_color(*self.bg_color)
        self.set_text_color(*self.txt_color)
        self._sep = sep

        if margin >= 0:
            self.t_margin_ori = margin
            self.l_margin_ori = margin
            self.r_margin_ori = margin
            self.restore_margin()
        else:
            self.t_margin_ori = self.t_margin
            self.l_margin_ori = self.l_margin
            self.r_margin_ori = self.r_margin

        self._fig_folder = Path('')
        self._base_fig = Path(base_fig)

        self.img_px = img_px

    @property
    def fig_path(self):
        return self._base_fig / self._fig_folder

    def set_fig_folder(self, fig_folder):
        self._fig_folder = fig_folder

    def set_sep(self, sep):
        self._sep = sep

    def restore_margin(self):
        self.set_top_margin(self.t_margin_ori)
        self.set_right_margin(self.r_margin_ori)
        self.set_left_margin(self.l_margin_ori)

    @property
    def sep(self):
        return self._sep

    @property
    def dest(self):
        return self.OUT / (self.name.replace(" ", "_") + ".pdf")

    @property
    def fig_src(self):
        return self._base_fig / self._fig_folder
        #return self.FIG

    @property
    def size(self):
        return (self.w, self.h)

    @property
    def epw(self):
        """ Effective page width """
        return self.w - self.r_margin - self.l_margin

    @property
    def eph(self):
        """ Effective page height """
        return self.h - 2 * self.t_margin

    def add_page(self, orientation='P'):
        super().add_page(orientation)
        self.rect(0, 0, self.w, self.h, style="F")

    def img_process(self, img, ratio=0):
        """ Process the image.
        if no ratio is given, the image is not cropped
        """
        img_src = self.fig_src / Path(img)
        img_dest = str(cut_save(img_src, self.OUT, ratio, self.img_px))
        return img_dest

    def one_fullpage(self, img):
        """ Display the picture fullpage """
        self.add_page()
        self.append_content(img, 0, 0, *self.size)
        # img_dest = self.img_process(img, self.size)
        # self.image(img_dest, 0, 0, *self.size)

    def one_centered(self, img, text=""):
        """ Display the picture centered with text """
        self.add_page()

        if text == "":
            text_size = (0, 0)
        else:
            text_size = (self.epw, (self.eph-self.sep)/6-self.sep)

        img_size = (self.epw, self.eph - text_size[1])
        img_dest = self.img_process(img, img_size)

        self.image(img_dest, self.l_margin, self.t_margin, *img_size)

        self.set_xy(self.l_margin, self.t_margin+img_size[1]+self.sep)
        if '\n' in text:
            self.multi_cell(text_size[0], self.font_size, text, align='J', border=1)
        else:
            self.cell(text_size[0], text_size[1]-self.sep, text, align='C', border=1)

    def one_side(self, img, txt=""):
        """ Display the image on the outside of the page
        along with text on the other side
        """
        self.add_page()
        p_no = self.page_no()
        win_dim = (self.size[0]*2/3, self.size[1])
        img_dest = self.img_process(img, win_dim)
        if p_no % 2 == 1:
            self.set_xy(win_dim[0], self.size[1]/2)
            self.multi_cell(self.size[0]/3, self.font_size, txt, align="C")
            self.image(img_dest, 0, 0, *win_dim)
        else:
            self.set_xy(0, self.size[1]/2)
            self.multi_cell(self.size[0]/3, self.font_size, txt, align="C")
            self.image(img_dest, self.size[0]/3, 0, *win_dim)

    def one_side_nocut(self, img, txt=""):
        """ Display the image on the outside of the page without resize it
        """
        self.add_page()
        p_no = self.page_no()
        win_dim = (self.size[0], self.size[1])
        img_dest = self.img_process(img, win_dim)
        if p_no % 2 == 1:
            self.set_xy(win_dim[0], self.size[1]/2)
            self.image(img_dest, 0, 0, *win_dim)
        else:
            self.set_xy(0, self.size[1]/2)
            self.image(img_dest, self.size[0]/3, 0, *win_dim)

    def rows(self, imgs, with_margin=True, with_sep=True):
        """ Pictures in rows """
        self.add_page()

        if with_margin:
            pg_size = (self.epw, self.eph)
            top = self.t_margin
            left = self.l_margin
        else:
            pg_size = self.size
            top = 0
            left = 0

        if with_sep:
            sep = self.sep
        else:
            sep = 0

        img_number = len(imgs)
        win_dim = (pg_size[0],
                   (pg_size[1] - (img_number - 1) * sep) / img_number)

        for img in imgs:
            self.append_content(img, left, top, *win_dim)
            # img_dest = self.img_process(img, win_dim)
            # self.image(img_dest, left, top, *win_dim)
            top += win_dim[1] + sep

    def grid_row(self, content, layout=[], with_margin=True, with_sep=True):
        """ Custom layout define by rows

        :param content: img or text to display in layout's cells
        :param layout: cell layout with weight (need same shape than content)
        :param with_margin: Put margins around pictures
        :param with_sep: Put separation between pictures
        """
        self.add_page()

        if with_margin:
            pg_size = (self.epw, self.eph)
            ori_top = self.t_margin
            ori_left = self.l_margin
        else:
            pg_size = self.size
            ori_top = 0
            ori_left = 0

        if with_sep:
            sep = self.sep
        else:
            sep = 0

        if layout == []:
            layout = [[1 for c in row] for row in content]
        else:
            if len(content) != len(layout):
                raise ValueError("Content and Layout need to have same number of rows")
            for (r, row) in enumerate(content):
                if len(row) != len(layout[r]):
                    raise ValueError(f"Content and Layout need to have same number of columns at row {r}")

        top = ori_top
        left = ori_left
        height_unit = (pg_size[1] - (len(layout) - 1) * sep) / len(layout)

        for (r, row) in enumerate(layout):
            width_unit = (pg_size[0] - (len(row) - 1) * sep) / sum(row)

            for (c, weight) in enumerate(row):
                dim = (width_unit * weight, height_unit)
                self.append_content(content[r][c], left, top, *dim)

                left += dim[0] + sep
            top += height_unit + sep
            left = ori_left

    def grid_column(self, content, layout=[], with_margin=True, with_sep=True):
        """ Custom layout define by column

        :param content: img or text to display in layout's cells 
        :param layout: cell layout with weight (need same shape than content)
        :param with_margin: Put margins around pictures
        :param with_sep: Put separation between pictures
        """
        self.add_page()

        if with_margin:
            pg_size = (self.epw, self.eph)
            ori_top = self.t_margin
            ori_left = self.l_margin
        else:
            pg_size = self.size
            ori_top = 0
            ori_left = 0

        if with_sep:
            sep = self.sep
        else:
            sep = 0

        if layout == []:
            layout = [[1 for r in column] for column in content]
        else:
            if len(content) != len(layout):
                raise ValueError("Content and Layout need to have same number of columns")
            for (r, column) in enumerate(content):
                if len(column) != len(layout[r]):
                    raise ValueError(f"Content and Layout need to have same number of columns at column {r}")

        top = ori_top
        left = ori_left
        width_unit = (pg_size[0] - (len(layout) - 1) * sep) / len(layout)

        for (c, column) in enumerate(layout):
            height_unit = (pg_size[1] - (len(column) - 1) * sep) / sum(column)

            for (r, weight) in enumerate(column):
                dim = (width_unit, height_unit * weight)
                self.append_content(content[c][r], left, top, *dim)

                top += dim[1] + sep
            left += width_unit + sep
            top = ori_top

    def append_content(self, content, left, top, width, height):
        try:
            img_dest = self.img_process(content, (width, height))
            self.image(img_dest, left, top, width, height)
        except (FileNotFoundError, IsADirectoryError):
            self.set_xy(left, top)
            if '\n' in content:
                self.multi_cell(width, self.font_size, content, align='J', border=1)
            else:
                self.cell(width, height, content, align='C', border=1)

if __name__ == "__main__":
    name = "annee3"
    pagesize = (250, 200)
    src_fig = Path("./fig/")
    output = Path("./build/")
    dest = output / (name + ".pdf")
    out_fig = output / "fig"

    photobook = Photobook(name, pdf_size=pagesize)
    photobook.set_font('Arial', 'B', 20)
    photobook.set_auto_page_break(False)

    photobook.rows(["chronologie/annee3/1-DD/DD-01.jpg"])
    photobook.rows(["chronologie/annee3/1-DD/DD-01.jpg", "chronologie/annee3/1-DD/DD-02.jpg"])
    photobook.rows(["chronologie/annee3/1-DD/DD-01.jpg", "chronologie/annee3/1-DD/DD-02.jpg"], with_margin=False)
    photobook.rows(["chronologie/annee3/1-DD/DD-01.jpg", "chronologie/annee3/1-DD/DD-02.jpg"], with_sep=False)
    photobook.rows(["chronologie/annee3/1-DD/DD-01.jpg", "chronologie/annee3/1-DD/DD-02.jpg"], with_margin=False, with_sep=False)
    photobook.rows(["chronologie/annee3/1-DD/DD-01.jpg",
                    "Tralalala",
                    "chronologie/annee3/1-DD/DD-02.jpg",
                    "chronologie/annee3/1-DD/DD-02.jpg"])

    photobook.grid_row([["chronologie/annee3/1-DD/DD-01.jpg", "chronologie/annee3/1-DD/DD-02.jpg"],
                        ["Coucou c'est moi!!", "chronologie/annee3/1-DD/DD-04.jpg"]],
                       [[1, 2], [3, 1]],
                       )
    photobook.grid_row([["chronologie/annee3/1-DD/DD-01.jpg", "chronologie/annee3/1-DD/DD-02.jpg"],
                        ["Coucou c'est moi!! \ncjfkldsq", "chronologie/annee3/1-DD/DD-04.jpg"]],
                       [[1, 2], [3, 1]])
    photobook.grid_row([["chronologie/annee3/1-DD/DD-01.jpg", "chronologie/annee3/1-DD/DD-02.jpg"],
                        ["chronologie/annee3/1-DD/DD-03.jpg", "chronologie/annee3/1-DD/DD-04.jpg"]],
                       [[1, 2], [3, 1]])
    photobook.set_top_margin(40)
    photobook.grid_row([["chronologie/annee3/1-DD/DD-01.jpg", "chronologie/annee3/1-DD/DD-02.jpg"],
                        ["chronologie/annee3/1-DD/DD-03.jpg", "chronologie/annee3/1-DD/DD-04.jpg"]],
                       [[1, 2], [3, 1]],)
    photobook.restore_margin()
    photobook.grid_row([["chronologie/annee3/1-DD/DD-01.jpg", "chronologie/annee3/1-DD/DD-02.jpg"],
                        ["chronologie/annee3/1-DD/DD-03.jpg", "chronologie/annee3/1-DD/DD-04.jpg"]],
                       [[1, 1], [1, 1]],
                       with_margin=False, with_sep=False
                       )


    photobook.output(dest)

