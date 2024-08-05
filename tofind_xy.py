import pandas as pd
import matplotlib.pyplot as plt

combined_0_75 = pd.read_csv("combined_2_(speed 0.75).csv")

plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
plt.plot(
    combined_0_75["times(seconds)"], combined_0_75["tof1"], label="speed 0.75 : TOF1"
)
plt.xlabel("Time (seconds)")
plt.ylabel("df_distance")
plt.title("distance")
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(combined_0_75["times(seconds)"], combined_0_75["x"], label="speed 0.75 : x")
plt.plot(combined_0_75["times(seconds)"], combined_0_75["y"], label="speed 0.75 : y")
plt.xlabel("Time (seconds)")
plt.ylabel("df_position")
plt.title("df_position")
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(
    combined_0_75["times(seconds)"], combined_0_75["acc_x"], label="speed 0.75 : acc_x"
)
plt.xlabel("Time (seconds)")
plt.ylabel("acc_x")
plt.title("acc_x")
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(
    combined_0_75["times(seconds)"], combined_0_75["acc_y"], label="speed 0.75 : acc_y"
)
plt.xlabel("Time (seconds)")
plt.ylabel("acc_y")
plt.title("acc_y")
plt.legend()

plt.tight_layout()
plt.show()
print(1)
