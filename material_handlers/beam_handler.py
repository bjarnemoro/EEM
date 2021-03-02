from materials.beam import Beam

class BeamHandler:
    def __init__(self):
        self.__beams = []

    def add_beam(beam: Beam):
        if Beam in beam.__mro__:
            self.__beams.append(beam)
        else:
            raise ValueError("parameter supposed to be of type Beam")

    def get_beams(self) -> list:
        return self.__beams