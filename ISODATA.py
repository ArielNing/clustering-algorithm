from numpy import *
import sys
# load dataset
def loadDataSet(fileName):
    data = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = list(map(float, curLine))
        data.append(fltLine)
    return data

# measure distance between two points
def distEclud(a, b):
    a=mat(a)
    b=mat(b)
    return sqrt(sum(power(a - b, 2)))


# estimate volume of the cluster
def volume_estimation(cluster, center):
    num_of_points = len(cluster)
    distance = []
    for i in range(num_of_points):
        distance.append(distEclud(center, cluster[i]))

    return sum(distance) / num_of_points


# defining of new cluster center
def new_cluster_centers(cluster):
    s = list(map(sum, zip(*cluster)))
    length = len(cluster)
    return [c/length for c in s]


# measure distances between each two pairs of cluster centers
def center_distance(centers):
    D_ij = {}
    k=0
    for i in range(len(centers)):
        for j in range(k, len(centers)):
            if i!=j:
                D_ij[(i, j)] = distEclud(centers[i], centers[j])
        k+=1
    return D_ij


# standart deviation vector for cluster
def standart_deviation(cluster, center):
    n = len(cluster)
    v_len=len(center)
    v=[[]for i in range(v_len)]
    V=[]
    for i in range(v_len):
        for j in range(n):
            v[i].append((cluster[j][i] - center[i]) ** 2)
        x=sqrt(sum(v[i]) / n)
        V.append(x)

    return V


def cluster_points_distribution(centers, points):
    centers_len = len(centers)
    points_len = len(points)
    distances = []
    distance = []

    # define array for clusters
    clusters = [[] for i in range(centers_len)]

    # iteration throught all points
    for i in range(points_len):
        # iteration throught all centers
        for j in range(centers_len):
            distance.append(distEclud(centers[j],points[i]))
        distances.append(distance)
        distance = []

    # distribution
    for i in range(points_len):
        ind = distances[i].index(min(distances[i]))
        clusters[ind].append(points[i])

    return clusters


def cluster_division(center, dev_vector):
    # divide only center of clusters

    # coeficient 分裂系数
    k = 0.5

    max_deviation = max(dev_vector)
    index = dev_vector.index(max(dev_vector))
    g = k * max_deviation

    # defining new centers
    center1 = list(center)
    center2 = list(center)
    center1[index] += g
    center2[index] -= g

    return center1,center2


def cluster_union(cluster1, cluster2, center1, center2):
    center=[]
    n1 = len(cluster1)
    n2 = len(cluster2)
    for i in range(len(center1)):
        x1=center1[i]
        x2=center2[i]
        x = (n1 * x1 + n2 * x2) / (n1 + n2)
        center.append(x)

    return center

    # K  max cluster number
    # THETA_N   for cluster elimination
    # THETA_S  for cluster division
    # THETA_C   for cluster union
    # L    max number of the pairs of union points at one iteration
    # I   max number of iterations
    # N_c    number of primary cluster centers
def ISODATA(dataSet,K,THETA_N,THETA_S,THETA_C,L,I,N_c):
    centers = []  # clusters centers
    clusters = []  # array for clusters points
    iteration = 1  # number of current iteration
    for i in range(N_c):
        centers.append(dataSet[i])

    while iteration <= I:
        # step 2
        if len(centers) <= 1:
            clusters.append(dataSet)
        else:
            clusters = cluster_points_distribution(centers, dataSet)

        # step 3
        # eliminating small clusters
        elim_centers=[] # list of eliminated centers index
        for i in range(len(clusters)):
            if len(clusters[i]) < THETA_N:
                elim_centers.append(i)
                N_c-=N_c
        centers = [item for i, item in enumerate(centers) if i not in elim_centers]
        clusters=cluster_points_distribution(centers,dataSet)

        # step 4
        # erasing existing centers and defining a new ones
        centers = []
        for i in range(len(clusters)):
            centers.append(new_cluster_centers(clusters[i]))

        # step 5 - estimating volumes of all clusters 类内平均距离
        D_vol = [] # array for clusters volume
        for i in range(len(centers)):
            D_vol.append(volume_estimation(clusters[i], centers[i]))

        # step 6
        if len(clusters) <= 1:
            D = 0 # 平均距离
        else:
            cluster_length = []
            vol_sum = []
            for i in range(len(centers)):
                cluster_length.append(len(clusters[i]))
                vol_sum.append(cluster_length[i] * D_vol[i])

            D = sum(vol_sum) / len(dataSet)

        # step 7
        hasdivide=False
        if iteration >= I:
            THETA_C = 0

        elif (N_c >= 2 * K) or (iteration % 2 == 0):
            pass

        else:
            # step 8
            vectors = [] # vectors of all clusters standart deviation
            for i in range(len(centers)):
                vectors.append(standart_deviation(clusters[i], centers[i]))

            # step 9
            max_s = []
            for v in vectors:
                max_s.append(max(v))

            # step 10 (cluster division)
            div_centers=[] # list of divided centers index
            for i in range(len(max_s)):
                length = len(clusters[i])
                coef = 2 * (THETA_N + 1)

                if (max_s[i] > THETA_S) and ((D_vol[i] > D and length > coef) or N_c < float(K) / 2):
                    center1, center2 = cluster_division(centers[i], vectors[i])
                    div_centers.append(i)
                    centers.append(center1)
                    centers.append(center2)
                    N_c += 1
                    hasdivide=True

                else:
                    pass

            centers = [item for i, item in enumerate(centers) if i not in div_centers]

        # step 11
        if hasdivide==False:
            D_ij = center_distance(centers)
            D_l = {}
            # step 12
            for d in D_ij:
                if D_ij[d] < THETA_C:
                    D_l[d]= (D_ij[d])
                else:
                    pass
            D_l=sorted(D_l.items(),key=lambda x:x[1])
            if len(D_l)>L: # select L pairs
                D_l=D_l[0:L]
            # step 13 (cluster union)
            uni_centers=[] # list of union center index
            for i in range(len(D_l)):
                key_i=D_l[i][0][0]
                key_j=D_l[i][0][1]
                center_u=cluster_union(clusters[key_i],clusters[key_j],centers[key_i],centers[key_j])
                uni_centers.append(key_i)
                uni_centers.append(key_j)
                centers.append(center_u)
                N_c-=1
            centers=[item for i,item in enumerate(centers) if i not in uni_centers]

        iteration += 1

    return centers,clusters


if __name__ == '__main__':
    if len(sys.argv)!=2:
        print("error usage")
    else:
        print("K:max cluster number\nTHETA_N:for cluster elimination\nTHETA_S:for cluster division\nTHETA_C:for cluster union\nL:max number of the pairs of union points at one iteration\nI:max number of iterations\nN_c:number of primary cluster centers")
        print("input your parameter:")
        K=int(input("K:"))
        THETA_N=int(input("THETA_N:"))
        THETA_S=int(input("THETA_S:"))
        THETA_C= int(input("THETA_C:"))
        L = int(input("L:"))
        I = int(input("I:"))
        N_c = int(input("N_c:"))
        data=loadDataSet(sys.argv[1])
        centers,clusters = ISODATA(data,K,THETA_N,THETA_S,THETA_C,L,I,N_c)
        print(centers)
        for i in clusters:
            print(i)