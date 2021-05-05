import numpy as np

def test_x_movement():
    k1 = 20 #n/m
    k2 = 30
    k3 = 20
    k4 = 50
    k5 = 20

    K1 = np.array([
        [k1, 0 ,0],
        [0, 0, 0],
        [0, 0, 0]])

    K2 = np.array([
        [k2, -k2, 0],
         [-k2, k2, 0],
         [0, 0, 0]])
            

    K3 = np.array([
        [k3, -k3, 0],
         [-k3, k3, 0],
         [0, 0, 0]])

    K4 = np.array([
        [k4, 0, -k4],
         [0, 0, 0],
         [-k4, 0, k4]])

    K5 = np.array([
        [0, 0, 0],
        [0, k5, -k5],
        [0, -k5, k5]])
            
    K_total = K1 + K2 + K3 + K4 + K5

    R1 = 100 #N
    R2 = 50
    R3 = 25

    R_total = np.array([R1, R2, R3])

    print(K_total, R_total)

    print(np.linalg.inv(K_total))

    print(R_total)

    print(np.matmul(np.linalg.inv(K_total), R_total))
            

if __name__ == "__main__":
    test_x_movement()