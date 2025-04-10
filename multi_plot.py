import pandas as pd
import glob
import matplotlib.pyplot as plt
import re
import os
import datetime

# Define the directories containing CSV files for each algorithm
algorithm_dirs = ["working_ddpg", "working_ppo", "working_sac", "working_a2c", "working_td3", "working_old_2", "working_ours"]  # Add more as needed

# Initialize a dictionary to store data
data_dict = {}

start_date = datetime.datetime(2016, 1, 4)
end_date = datetime.datetime(2020, 7, 7)

trading_days = pd.date_range(start=start_date, end=end_date, freq="B") #supposed to be 2020-07-07

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

            df = pd.read_csv(file, header=None, names=["Step", "Reward"], skiprows=1)
            df["Step"] += start_step  # Adjust step values
            #df["Step"] = df["Step"].fillna(0).replace([float("inf"), float("-inf")], 0).astype(int)

            #df["Date"] = [trading_days[step] for step in df["Step"]]#start_date + pd.to_timedelta(df["Step"], unit="D")
            df["Date"] = df["Step"].fillna(0).replace([float("inf"), float("-inf")], 0).astype(int).apply(lambda x: trading_days[x] if x < len(trading_days) else trading_days[-1])
            df["Date"] = pd.to_datetime(df["Date"])

            df.sort_values("Step", inplace=True)
            df["Return"] = ((df["Reward"] - 1e6) / 1e6) * 100
            
            df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    #combined_df.loc[len(combined_df)] = [None, None, None, None]
    #combined_df.dropna(inplace=True)
    combined_df.sort_values("Step", inplace=True)

    #print(algo_dir + " :\n")
    #print(combined_df.tail(10))  # Check the final entries before plotting

    data_dict[algo_dir] = combined_df  # Store data per algorithm

# Load DJIA data
djia = pd.read_csv("djia.csv")  # Update filename
djia["Date"] = pd.to_datetime(djia["Date"])

actual_start = datetime.datetime(2016, 7, 1)
djia_final = djia[(djia["Date"] >= actual_start) & (djia["Date"] <= end_date)]

djia_final.sort_values("Date", inplace=True)

djia_final["Price"] = [float(price_value.replace(",", "")) for price_value in djia_final["Price"]]

# Compute DJIA cumulative return (assuming price column exists)
djia_final["Return"] = ((djia_final["Price"] - djia_final["Price"].iloc[0])/ djia_final["Price"].iloc[0]) * 100


# Plot multiple algorithms for comparison
plt.figure(figsize=(12, 6))

labels = ["DDPG", "PPO", "SAC", "A2C", "TD3", "Orig. Ensemble", "Our Ensemble"]
i = 0

for algo, df in data_dict.items():
    #plt.plot(df["Step"], df["Reward"] / 1e6, linestyle='-', linewidth=2, label=f"{labels[i]}")
    plt.plot(df["Date"], df["Return"], linestyle='-', linewidth=2, label=f"{labels[i]}", marker=None)
    i += 1

plt.plot(djia_final["Date"], djia_final["Return"], linestyle='-', linewidth=2, label=f"DJIA", marker=None)
#update these to be the lables that you want
plt.xlabel("Date")
plt.ylabel("Percent Increase")
plt.title("Comparison of Cumulative Return Values")
plt.legend()
plt.grid()
plt.show()

plt.savefig("value_comparison.png", dpi=300)

print(f"Successfully combined results for {len(algorithm_dirs)} algorithms and plotted the scaled rewards.")