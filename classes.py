import numpy as np




class Ellipse:
    def __init__(self, radial_distance, eccentricity, rotatoin_angle) -> None:
        self.r = radial_distance
        self.e = eccentricity
        self.rot = rotatoin_angle

        self._calc_axis()
        self._calc_perimeter()

    def _calc_axis(self):
        self.semi_major = np.sqrt(self.r**2/(1-self.e**2))
        self.semi_minor = self.r

    def _calc_perimeter(self):
        t = np.linspace(0, 2*3.1416, 200)
        x = self.semi_major * np.cos(t)
        y = self.semi_minor * np.sin(t)
        xy_vector = np.array([x, y])
        self.rotation_matrix = np.array([[np.cos(self.rot), -np.sin(self.rot)], [np.sin(self.rot), np.cos(self.rot)]])
        self.perimeter = np.matmul(self.rotation_matrix, xy_vector)

        

class Star:
    def __init__(self, Ellipse) -> None:
        self.semi_major = Ellipse.semi_major
        self.semi_minor = Ellipse.semi_minor
        self.rot_matrix = Ellipse.rotation_matrix
        self.theta = np.random.uniform(0, 2*3.1416)
        self.r_norm = None

        self._update_pos()
        self._update_radius()

    def _vel_function(self, r):

        assert self.r_norm != None, "Radius normalization factor not initialized"
        radius = r/self.r_norm

        log = 0.3*np.log(11*radius)
        sine = 0.15*np.sin(6.77*radius**0.4)
        linear = -0.65*radius + 1
        vel = (log + sine + linear)/1.1395

        return vel

    def _update_angle(self, dt):
        f_r = self._vel_function(self.r)
        num = f_r*dt*self.r
        den = np.sqrt((self.semi_major*self.y)**2 + (self.semi_minor*self.x)**2)

        self.theta += num/den


    def _update_pos(self):
        self.x = self.semi_major*np.cos(self.theta)
        self.y = self.semi_minor*np.sin(self.theta)


    def _update_radius(self):
        self.r = np.sqrt(self.x**2 + self.y**2)


    def move(self, dt):
        self._update_angle(dt)
        self._update_pos()
        self._update_radius()

    def get_pos(self):
        xy = np.array([self.x, self.y])
        return np.matmul(self.rot_matrix, xy)
