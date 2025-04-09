import pandas as pd
import glob
import matplotlib.pyplot as plt
import re

#I recommend doing value but this will work for value, rewards, and validation
# Define the path to your CSV files - change this to rewards or value depending on the graph
file_pattern = "./working_ours/account_value_trade_ensemble_*.csv"#"./all_tests/working_theirs_25000/account_rewards_trade_ensemble_*.csv" 

# Get all matching file names
file_list = sorted(glob.glob(file_pattern))

print(file_list)

# Initialize a list for data storage
df_list = []

# Add the first row manually
#df_list.append(pd.DataFrame([[0, 1000000]], columns=["Step", "Reward"]))

# Process each file
for file in file_list:
    # Extract the <start_step> from the filename - change this depending on if you are doing rewards or value
    match = re.search(r"account_value_trade_ensemble_(\d+)\.csv", file)
    if match:
        start_step = int(match.group(1))

        # Read the CSV file
        df = pd.read_csv(file, header=None, names=["Step", "Reward"])

        # Adjust step values by adding start_step
        df["Step"] += start_step

        # Store the modified DataFrame
        df_list.append(df)

# Combine all DataFrames
combined_df = pd.concat(df_list, ignore_index=True)

# Save to a new CSV file
combined_df.to_csv("combined_rewards.csv", index=False)


# Plot the rewards over time with a clean line
plt.figure(figsize=(12, 6))
plt.plot(combined_df["Step"], combined_df["Reward"], linestyle='-', linewidth=2, label="Value (scaled by 1e6)")
plt.xlabel("Time Step")
plt.ylabel("Value (Millions)")
plt.title("Ensemble RL Algorithmic Trading Value")
plt.legend()
plt.grid()
plt.show()

print(f"Successfully combined {len(file_list)} files into 'combined_rewards.csv' and plotted the scaled rewards.")
