#-*-coding: UTF-8-*-
######################################################################################
#  Author: Junjun Guo
#  E-mail: guojj@tongji.edu.cn/guojj_ce@163.com
#    Date: 05/02/2020
#  Environemet: Successfully excucted in python 3.6
######################################################################################
######################################################################################
import numpy as np
import math
def is_in_2d_polygon(point, vertices):
    px = point[0]
    py = point[1]
    angle_sum = 0

    size = len(vertices)
    if size < 3:
        raise ValueError("len of vertices < 3")
    j = size - 1
    for i in range(0, size):
        sx = vertices[i][0]
        sy = vertices[i][1]
        tx = vertices[j][0]
        ty = vertices[j][1]

        # ͨ���жϵ㵽ͨ�������ֱ�ߵľ����Ƿ�Ϊ0���жϵ��Ƿ��ڱ���
        # y = kx + b, -y + kx + b = 0
        k = (sy - ty) / (sx - tx + 0.000000000001)  # �����0
        b = sy - k * sx
        dis = np.abs(k * px - 1 * py + b) / np.sqrt(k * k + 1)
        if dis < 0.000001:  # �õ���ֱ����
            if sx <= px <= tx or tx <= px <= sx:  # �õ��ڱߵ���������֮�䣬˵�������ڱ���
                return True

        # ����н�
        angle = math.atan2(sy - py, sx - px) - math.atan2(ty - py, tx - px)
        # angle��Ҫ��-�е���֮��
        if angle >= math.pi:
            angle = angle - math.pi * 2
        elif angle <= -math.pi:
            angle = angle + math.pi * 2

        # �ۻ�
        angle_sum += angle
        j = i

    # ����нǺ���2*pi֮���С��һ���ǳ�С����������Ϊ���
    return np.abs(angle_sum - math.pi * 2) < 0.00000000001
########################################################################################
#
# closedNodeValues=[[0,0],[2,0],[2,1],[1,1],[1,2],[2,2],[2,3],[0,3],[0,0]]
# print(is_in_2d_polygon([1.01,1.01], closedNodeValues))