import numpy as np
import matplotlib.pyplot as plt
import itertools
from cycler import cycler

from materials.beam import Beam
from materials.joint import Joint

def local_K(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array(
        [[c**2, c*s, -c**2, -c*s],
         [c*s, s**2, -c*s, -s**2],
         [-c**2, -c*s, c**2, c*s],
         [-c*s, -s**2, c*s, s**2]])

def get_rotation(pos1, pos2):
    if (pos1[1] - pos2[1]) != 0:
        return np.arctan((pos1[1] - pos2[1]) / (pos1[0] - pos2[0]))
    else:
        return 0

def stiffness_matrix(nodes, beams):
    size = len(nodes)*2
    E = 210e3 #MPa
    A = 1000 #mm^2

    K = np.zeros(shape=(size, size))

    for b in beams:
        rotation = get_rotation(nodes[b[0]], nodes[b[1]])
        L = ((nodes[b[0]][0] - nodes[b[1]][0])**2 + (nodes[b[0]][1] - nodes[b[1]][1])**2)**0.5
        k = E*A / L
        rot_k = local_K(rotation)

        possible_combinations = ((b[0], b[0]), (b[0], b[1]), (b[1], b[0]), (b[1], b[1]))
        for i, (idx1, idx2) in enumerate(possible_combinations):
            i1 = i%2
            i2 = i//2
            K[idx1*2][idx2*2] += k * rot_k[i1*2][i2*2]
            K[idx1*2 + 1][idx2*2] += k * rot_k[i1*2 + 1][i2*2]
            K[idx1*2][idx2*2 + 1] += k * rot_k[i1*2][i2*2 + 1]
            K[idx1*2 + 1][idx2*2 + 1] += k * rot_k[i1*2 + 1][i2*2 + 1]

    return K

def stiffness_matrix_obj(nodes, beams: [Beam]):
    size = len(nodes)*2
    E = 210e3 #MPa
    A = 1000 #mm^2

    K = np.zeros(shape=(size, size))

    for b in beams:
        pos1, pos2 = b.get_positions()
        rotation = get_rotation(pos1, pos2)

        L = np.sqrt(np.sum((pos1 - pos2)**2))
        k = E*A / L
        rot_k = local_K(rotation)

        idx1, idx2 = [nodes.index(joint) for joint in b.get_joints()]
        possible_combinations = ((idx1, idx1), (idx1, idx2), (idx2, idx1), (idx2, idx2))
        for i, (idx1, idx2) in enumerate(possible_combinations):
            i1 = i%2
            i2 = i//2
            K[idx1*2][idx2*2] += k * rot_k[i1*2][i2*2]
            K[idx1*2 + 1][idx2*2] += k * rot_k[i1*2 + 1][i2*2]
            K[idx1*2][idx2*2 + 1] += k * rot_k[i1*2][i2*2 + 1]
            K[idx1*2 + 1][idx2*2 + 1] += k * rot_k[i1*2 + 1][i2*2 + 1]

    return K

def FEA(nodes: [Joint or tuple], bars: [Beam or tuple], anchors: [int], loads: [int]) -> np.ndarray:
    """
    Calculate displacement of a properly confined body consisting of bar elements.
    a bar element is an element consisting of two nodes that exists on a 2d coordinate system
    these nodes can displace in both the x and y direction 
    bar elements only take axial forces
    

    @parameters
    nodes -- list of tuples, tuple contains x and y coordinates of a point in the global coordinate system
    beams -- list of tuples, tuple contains the index of two node elements
    anchors -- list of indices, the index sets the degrees of freedom to 0 for the chosen node

    @return
    displacements -- list of tuples, tuple contains x and y displacements for the given nodes
                     anchor nodes have a displacement of 0
    """
    assert len(nodes)*2 == len(loads), "the loads should have the same size as the nodes"

    NODES_SIZE = len(nodes)*2
    anchors.sort()

    #get the stiffness matrix, delete the anchor rows and columns from the K matrix afterwards
    if type(nodes[0]) == Joint:
        K = stiffness_matrix_obj(nodes, bars)
    else:
        K = stiffness_matrix(nodes, bars)

    non_confined_row_cols = list(range(NODES_SIZE))
    [(non_confined_row_cols.remove(idx*2), non_confined_row_cols.remove(idx*2+1)) for idx in anchors]

    confined_K = K[non_confined_row_cols][: , non_confined_row_cols]

    inverted_confined_K = np.linalg.inv(confined_K)
    
    #remove the load component working on confined nodes (anchors)
    confined_loads = loads[non_confined_row_cols]

    #calculate the displacement with moore's law
    displacements = np.matmul(confined_loads, inverted_confined_K)

    anchor_idx = []
    for i, idx in enumerate(anchors):
        anchor_idx.append(idx-i)

    displacements = np.insert(displacements, [idx*2 for idx in anchor_idx*2], 0)

    return displacements


def main():
    DISPLACEMENT_FACTOR = 1
    h = 2

    nodes = [(0,0), (2,0), (1,4), (4,0), (3,4), (6,0), (5,4), (8, 0), (7, 4), (10, 0), (9, 4)]
    beams = [(0, 1), (0, 2), (1, 2), (2, 4), (1, 3), (1, 4), (3, 4), (4, 6), (3, 5), (3, 6), (5, 6), (6, 8), (5, 7), (5, 8), (7, 8), (8, 10), (7, 9), (7, 10), (9, 10)] #beam consists of a pair of node indices

    nodes2 = [Joint(0,0), Joint(2,0), Joint(1,h), Joint(4,0), Joint(3,h), Joint(6,0), Joint(5,h), Joint(8, 0), Joint(7, h), Joint(10, 0), Joint(9, h)]
    beams2 = [Beam(nodes2[0], nodes2[1]), 
             Beam(nodes2[0], nodes2[2]), 
             Beam(nodes2[1], nodes2[2]), 
             Beam(nodes2[2], nodes2[4]), 
             Beam(nodes2[1], nodes2[3]), 
             Beam(nodes2[1], nodes2[4]), 
             Beam(nodes2[3], nodes2[4]), 
             Beam(nodes2[4], nodes2[6]), 
             Beam(nodes2[3], nodes2[5]), 
             Beam(nodes2[3], nodes2[6]), 
             Beam(nodes2[5], nodes2[6]), 
             Beam(nodes2[6], nodes2[8]), 
             Beam(nodes2[5], nodes2[7]), 
             Beam(nodes2[5], nodes2[8]), 
             Beam(nodes2[7], nodes2[8]), 
             Beam(nodes2[8], nodes2[10]), 
             Beam(nodes2[7], nodes2[9]), 
             Beam(nodes2[7], nodes2[10]), 
             Beam(nodes2[9], nodes2[10])]


    loads = np.ones(shape=(len(nodes)*2))
    loads[13] = -1000000

    displacements = FEA(nodes, beams, [0, 7], loads)
    displacements *= DISPLACEMENT_FACTOR

    displacements_obj = FEA(nodes2, beams2, [0, 9], loads)
    displacements_obj *= DISPLACEMENT_FACTOR

    #plotting data lists
    data = [((nodes[b[0]][0],nodes[b[1]][0]), (nodes[b[0]][1], nodes[b[1]][1]), 'g') for b in beams]
    data = list(itertools.chain.from_iterable(data))

    displaced_nodes = [(n[0]+displacements[i*2], n[1]+displacements[i*2+1]) for i, n in enumerate(nodes)]

    displaced_data = [((displaced_nodes[b[0]][0],displaced_nodes[b[1]][0]), (displaced_nodes[b[0]][1], displaced_nodes[b[1]][1]), 'b') for b in beams]
    displaced_data = list(itertools.chain.from_iterable(displaced_data))

    #plotting data objects
    data2 = [(*b.get_positions_xxyy(), 'g') for b in beams2]
    data2 = list(itertools.chain.from_iterable(data2))

    [node.set_displacement(*displacements_obj[i*2:(i+1)*2]) for i, node in enumerate(nodes2)]

    stresses = np.array([b.get_stress() for b in beams2])
    custom_cycler = (cycler(color=['r', 'g', 'b']))
    color_unstressed = np.array([33, 181, 191])
    color_stressed = np.array([207, 82, 14])
    max_stress = max(stresses)
    print(max_stress)

    stresses /= max_stress

    color_unstressed + 1 * (color_stressed - color_unstressed)
    hex_colors = ['#%02x%02x%02x' % tuple((color_unstressed + stress * (color_stressed - color_unstressed)).astype(int)) for stress in stresses]

    displaced_obj_data = [(*(b.get_positions_xxyy()), hex_colors[i]) for i, b in enumerate(beams2)]
    displaced_obj_data = list(itertools.chain.from_iterable(displaced_obj_data))

    #plot
    #plt.plot(*data2)
    #plt.plot(*displaced_data)
    fig, (ax1, ax2) = plt.subplots(nrows=2)
    ax1.set_prop_cycle(custom_cycler)
    ax1.plot(*displaced_obj_data)
    ax2.plot(*data2)
    #plt.ylim([-5, 5])
    #wplt.xlim([0, 10])
    plt.show()

    

if __name__ == "__main__":
    main()