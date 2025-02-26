import pandas as pd
import numpy as np


class CameraPose():
    def __init__(self, acc_path, gyro_path):
        self.acc_path = acc_path
        self.gyro_path = gyro_path

        self.acc_df = self.pre_process(acc_path)
        self.gyro_df = self.pre_process(gyro_path, gyro=True)

        self.initial_position = np.array([0, 0, 0])
        self.initial_orientation = np.array([0, 0, 0])

    def pre_process(self, path, gyro=False):
        df = pd.read_csv(path)

        # Add the first row for the initial time
        df = pd.concat([pd.DataFrame({'seconds_elapsed': [0], 'x': [0], 'y': [0], 'z': [0]}), df], ignore_index=True)

        # Convert angular velocity to radian per second
        if gyro:
            df['x'] = df['x'] * np.pi / 180
            df['y'] = df['y'] * np.pi / 180
            df['z'] = df['z'] * np.pi / 180

        return df


    
        
