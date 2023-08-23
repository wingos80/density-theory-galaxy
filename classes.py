import numpy as np

class Ellipse:
    def __init__(self, radial_distance, eccentricity, rotatoin_angle) -> None:
        self.r = radial_distance
        self.eccentricity = eccentricity
        self.rot = rotatoin_angle

        self._calc_axis()
        self._calc_perimeter()

    def _calc_axis(self):
        self.semi_major = np.sqrt(self.r**2/(1-self.eccentricity**2))
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
        self.semi_major   = Ellipse.semi_major
        self.eccentricity = Ellipse.eccentricity
        self.rot_matrix   = Ellipse.rotation_matrix
        self.theta        = np.random.uniform(0, 2*3.1416)
        self.r_norm       = None
        self.r            = self.semi_major*(1-self.eccentricity**2)/(1+self.eccentricity*np.cos(self.theta))

    def _vel_function(self, r):

        assert self.r_norm != None, "Radius normalization factor not initialized"
        radius = r/self.r_norm

        log = 0.3*np.log(11*radius)
        sine = 0.15*np.sin(6.77*radius**0.4)
        linear = -0.65*radius + 1
        vel = (log + sine + linear)/1.1395

        return vel
    
    def _update_kepler_radius(self, dt):
        self.theta += dt*self._vel_function(self.r)
        num         = self.semi_major*(1-self.eccentricity**2)
        den         = 1 + self.eccentricity*np.cos(self.theta)
        self.r      = num/den

    def _update_pos(self):
        self.x = self.r*np.cos(self.theta)
        self.y = self.r*np.sin(self.theta)


    def move(self, dt):
        self._update_kepler_radius(dt)
        self._update_pos()

    def get_pos(self):
        xy = np.array([self.x, self.y])
        return np.matmul(self.rot_matrix, xy)