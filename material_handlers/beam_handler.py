from materials.beam import Beam
from materials.joint import Joint

class BeamHandler:
    def __init__(self):
        self.__beams = []

    def add_beam(self, beam: Beam):
        if Beam in beam.__class__.__mro__:
            self.__beams.append(beam)
        else:
            raise ValueError("parameter supposed to be of type Beam")

    def get_beams(self) -> list:
        return self.__beams

    def delete_by_joint(self, joint: Joint) -> None:
        #TODO: store beams adress in joints to speed up the program
        for beam in self.__beams[::-1]:
            if joint in beam.get_joints():
                self.__beams.remove(beam)