
# A singular pin
class Pin:
    def __init__(self, coords, img):
        self.coords = coords
        self.x,self.y,self.w,self.h = coords
        
        self.img = img[self.x : self.x+self.w, self.y: self.y+self.h] # img of only the result
        self.rgb = self.get_rgb_avg()

    def get_rgb_avg(self):
        img = self.img
        coords_sq = self.coords
        x, y, h, w = coords_sq
        n = h*w # n of pixels
        R_avg = []
        G_avg = [] 
        B_avg = []
        
        for wi in range(x, x+w):
            for hi in range(y, y+h):
                r, g, b = img[wi, hi]
                #print(f"({r}, {g}, {b})")
                R_avg.append(r)
                G_avg.append(g)
                B_avg.append(b)

        R_avg = round(sum(R_avg)/n, 2)
        G_avg = round(sum(G_avg)/n, 2)
        B_avg = round(sum(B_avg)/n, 2)

        return f"({R_avg}, {G_avg}, {B_avg})"

