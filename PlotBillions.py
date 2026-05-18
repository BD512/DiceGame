import math

class Square:
    def __init__(self, s):
        self.s = s
        self.centre_radius = self.s/2
        self.corner_radius = math.sqrt(s**2+s**2)/2-self.centre_radius# (math.sqrt(self.centre_radius)**2+math.sqrt(self.centre_radius)**2)-self.centre_radius

    def findRemainingCoordinates(self):
        points = []
        count = 0
        for x in range(self.s+1):
            for y in range(self.s+1):
                if (x-self.s)**2+(y-self.s)**2 <= self.corner_radius**2:
                    pass
                elif x**2+(y-self.s)**2 <= self.corner_radius**2:
                    pass
                elif (x-self.s)**2+y**2 <= self.corner_radius**2:
                    pass
                elif x**2 + y**2 <= self.corner_radius**2:
                    pass
                elif (x-self.s/2)**2+(y-self.s/2)**2 <= self.centre_radius**2:
                    pass
                else:
                    print(f"{x},{y},0,1")
                    points.append([x,y])
                    count += 1
        return count, points

print(Square(808000000).findRemainingCoordinates())



