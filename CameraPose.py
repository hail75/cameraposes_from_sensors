import pandas as pd
import numpy as np


class CameraPose:  
    def __init__(self, acc_path, gyro_path):
        self.acc_path = acc_path
        self.gyro_path = gyro_path

        self.acc_df = self._pre_process(acc_path)
        self.gyro_df = self._pre_process(gyro_path)

        self.initial_orientation = np.array([0.0, 0.0, 0.0])
        self.initial_position = np.array([0.0, 0.0, 0.0])

        self._transform_acc_data()



    def _pre_process(self, path):
        df = pd.read_csv(path)

        # Add the first row for the initial time
        df = pd.concat([pd.DataFrame({'seconds_elapsed': [0.0], 'x': [0.0], 'y': [0.0], 'z': [0.0]}), df], ignore_index=True)

        return df        
    
    def _validate_time(self, t):
        assert t >= 0, "Time must be greater than or equal to 0"
        assert t <= self.acc_df.iloc[-1]['seconds_elapsed'], "Time must be less than or equal to the last timestamp"
        assert t <= self.gyro_df.iloc[-1]['seconds_elapsed'], "Time must be less than or equal to the last timestamp"
    
    def _transform_acc_data(self):
        # Convert the accelerometer data to initial orientation perspective

        pass
    def get_orientation(self, t):
        self._validate_time(t)
        
        current_orientation = self.initial_orientation

        i = 1

        # Calculate the orientation at time t using integration
        while self.gyro_df.iloc[i]['seconds_elapsed'] < t:
            d_t = self.gyro_df.iloc[i]['seconds_elapsed'] - self.gyro_df.iloc[i-1]['seconds_elapsed']
            
            current_angular_velocity = np.array([
                self.gyro_df.iloc[i]['x'],
                self.gyro_df.iloc[i]['y'],
                self.gyro_df.iloc[i]['z']
            ])
            
            prev_angular_velocity = np.array([
                self.gyro_df.iloc[i-1]['x'],
                self.gyro_df.iloc[i-1]['y'],
                self.gyro_df.iloc[i-1]['z']
            ])

            d_orientation = 0.5 * (current_angular_velocity + prev_angular_velocity) * d_t
            current_orientation += d_orientation

            current_orientation = np.mod(current_orientation + np.pi, 2 * np.pi) - np.pi
            i += 1
        
        return current_orientation

    def get_position(self, t):
        self._validate_time(t)

        # TODO
        pass


if  __name__ == "__main__":
    acc_path = "/home/long-nguyen/Downloads/2025-03-03_04-38-57/Accelerometer.csv"
    gyro_path = "/home/long-nguyen/Downloads/2025-03-03_04-38-57/Gyroscope.csv"

    camera_pose = CameraPose(acc_path, gyro_path)

    import matplotlib.pyplot as plt

    # Plot the x-axis orientation with rate 0.1s
    x = np.arange(0, 7, 0.1)
    theta_x = [camera_pose.get_orientation(t)[0] for t in x]
    theta_x = [theta * 180 / np.pi for theta in theta_x]
    plt.plot(x, theta_x)
    plt.show()

