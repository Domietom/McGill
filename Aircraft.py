class Aircraft:

    def __init__(self, ID=0):
        self.ID = ID
        self.trajectory = []
        self.segmentSpeed = {}
        self.conflicts = []

    def __repr__(self):
        return f'Aircraft {self.ID}'