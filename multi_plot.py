import pandas as pd
import glob
import matplotlib.pyplot as plt
import re
import os
import datetime

# Define the directories containing CSV files for each algorithm
algorithm_dirs = ["working_ddpg", "working_ppo", "working_sac", "working_a2c", "working_td3"]#, "working_old_2", "working_ours"]  # Add more as needed

# Initialize a dictionary to store data
data_dict = {}

start_date = datetime.datetime(2016, 1, 4)

trading_days = pd.date_range(start=start_date, end="2020-07-07", freq="B")
print(type(trading_days[1]))

# Process each algorithm's directory
for algo_dir in algorithm_dirs:
    #change this to be for the value or the rewards (i recommend value since reward is really volitle)
    file_pattern = os.path.join(algo_dir, "account_value_trade_ensemble_*.csv")
    file_list = sorted(glob.glob(file_pattern))

    df_list = []
    #df_list.append(pd.DataFrame([[0, 1000000]], columns=["Step", "Reward"]))  # Ensure first row

    for file in file_list:
        #change this to match the other path
        match = re.search(r"account_value_trade_ensemble_(\d+)\.csv", file)
        if match:
            start_step = int(match.group(1))

            df = pd.read_csv(file, header=None, names=["Step", "Reward"])
            df["Step"] += start_step  # Adjust step values

            #df["Date"] = start_date + pd.to_timedelta(df["Step"], unit="D")

            
            df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    data_dict[algo_dir] = combined_df  # Store data per algorithm

# Plot multiple algorithms for comparison
plt.figure(figsize=(12, 6))

labels = ["DDPG", "PPO", "SAC", "A2C", "TD3", "Orig. Ensemble", "Our Ensemble"]
i = 0

for algo, df in data_dict.items():
    plt.plot(df["Step"], df["Reward"] / 1e6, linestyle='-', linewidth=2, label=f"{labels[i]}")
    i += 1

#update these to be the lables that you want
plt.xlabel("Days")
plt.ylabel("Value (Millions)")
plt.title("Comparison of Ensemble RL Algorithmic Trading Portfolio Values")
plt.legend()
plt.grid()
plt.show()

plt.savefig("value_comparison.png", dpi=300)

print(f"Successfully combined results for {len(algorithm_dirs)} algorithms and plotted the scaled rewards.")