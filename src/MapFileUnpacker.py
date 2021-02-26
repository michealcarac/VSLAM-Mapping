import csv
import msgpack
import numpy as np
from scipy.spatial.transform import Rotation as R


class Unpacker:
    def __init__(self, mapfile):
        # USAGE: Takes in map file in form of .msg
        with open(mapfile, "rb") as msg_pack_file:
            msg_pack_byte_data = msg_pack_file.read()

        self.data = msgpack.unpackb(msg_pack_byte_data)

    def extract_keyframe_data(self):
        # USAGE: Takes in zero arguments, and returns
        # the extracted keyframe data in the form (x,y,z)
        kfs_trans = []
        kfs_rot = []
        kfs_pos = []
        for kf in self.data['keyframes']:
            ktrans = self.data['keyframes'][kf]['trans_cw']
            kf_trans = [ktrans[0], ktrans[1], ktrans[2]]

            krot = self.data['keyframes'][kf]['rot_cw']
            kf_rot = [krot[0], krot[1], krot[2], krot[3]]

            kf_rot_mat = R.from_quat(kf_rot)
            kf_pos = np.matmul(-np.transpose(kf_rot_mat.as_matrix()), np.transpose(kf_trans))

            kfs_trans.append(kf_trans)
            kfs_rot.append(kf_rot)
            kfs_pos.append(kf_pos)

        self.keyframes_trans = np.array(kfs_trans)
        self.keyframes_rot = np.array(kfs_rot)
        self.keyframes_pos = np.array(kfs_pos)

        placeholderX = self.keyframes_pos[:, 0]  # Can't use numpy arrays in append
        placeholderY = self.keyframes_pos[:, 1]
        placeholderZ = self.keyframes_pos[:, 2]
        kf_pos = []
        for i in range(len(self.keyframes_pos[:, 0])):
            set = [placeholderX[i], placeholderZ[i], -placeholderY[i]]
            kf_pos.append(set)
        self.keyframes_pos = np.array(kf_pos)
        data = self.keyframes_pos

        return data

    def extract_landmark_data(self):
        # USAGE: Takes in zero arguments, and returns
        # the extracted landmark data in the form (x,y,z)
        lms_trans = []
        for lm in self.data['landmarks']:
            lmtrans = self.data['landmarks'][lm]['pos_w']
            lm_trans = [lmtrans[0], lmtrans[2], -lmtrans[1]]
            lms_trans.append(lm_trans)

        self.landmark_coords = np.array(lms_trans)
        # Get rid of outliers
        self.landmark_coords = self.delete_points(self.landmark_coords)
        data = self.landmark_coords

        return data

    def delete_points(self, data, m=2.5):
        # FOR LANDMARK DATA ONLY
        # Deletes the points that are outliers
        # X outliers
        boolsA = abs(data[:, 0] - np.mean(data[:, 0])) < m * np.std(data[:, 0])
        falseindexes = []
        for i in range(len(data)):
            if not boolsA[i]:
                falseindexes.append(i)
        new = np.delete(data, falseindexes, axis=0)

        # Y outliers
        boolsB = abs(new[:, 1] - np.mean(new[:, 1])) < m * np.std(new[:, 1])
        falseindexes = []
        for i in range(len(new)):
            if not boolsB[i]:
                falseindexes.append(i)
        newb = np.delete(new, falseindexes, axis=0)

        # Z outliers
        boolsC = abs(newb[:, 2] - np.mean(newb[:, 2])) < m * np.std(newb[:, 2])
        falseindexes = []
        for i in range(len(newb)):
            if not boolsC[i]:
                falseindexes.append(i)
        newc = np.delete(newb, falseindexes, axis=0)
        return newc

    def export(self):
        with open('mapdataKeyframes.txt', 'w') as csvfile:
            mapwriter = csv.writer(csvfile, delimiter=',')
            mapwriter.writerows(self.keyframes_pos)
        with open('mapdataLandmarks.txt', 'w') as csvfile:
            mapwriter = csv.writer(csvfile, delimiter=',')
            mapwriter.writerows(self.landmark_coords)


if __name__ == "__main__":
    unpack = Unpacker("/run/media/spixy/New Volume/Research/openvslam_occ_grid-master/map.msg")
    unpack.extract_landmark_data()
    unpack.extract_keyframe_data()
    unpack.export()
