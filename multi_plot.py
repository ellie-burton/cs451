import pandas as pd
import glob
import matplotlib.pyplot as plt
import re
import os

# Define the directories containing CSV files for each algorithm
algorithm_dirs = ["working_ours", "all_tests/working_theirs_25000"]  # Add more as needed

# Initialize a dictionary to store data
data_dict = {}

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
            
            df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    data_dict[algo_dir] = combined_df  # Store data per algorithm

# Plot multiple algorithms for comparison
plt.figure(figsize=(12, 6))

for algo, df in data_dict.items():
    plt.plot(df["Step"], df["Reward"] / 1e6, linestyle='-', linewidth=2, label=f"{algo} Rewards")

#update these to be the lables that you want
plt.xlabel("Time Step")
plt.ylabel("Reward (Millions)")
plt.title("Comparison of Ensemble RL Algorithmic Trading Rewards")
plt.legend()
plt.grid()
plt.show()

plt.savefig("value_comparison.png", dpi=300)

print(f"Successfully combined results for {len(algorithm_dirs)} algorithms and plotted the scaled rewards.")