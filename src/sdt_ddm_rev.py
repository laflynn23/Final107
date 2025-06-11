import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Simulated posterior summary (replace with: az.summary(trace, var_names=[...]) in real use)
summary_data = {
    "mean_d_prime[0]": {"mean": 1.2},
    "mean_d_prime[1]": {"mean": 0.9},
    "mean_d_prime[2]": {"mean": 0.5},
    "mean_d_prime[3]": {"mean": 0.3},
    "mean_criterion[0]": {"mean": 0.1},
    "mean_criterion[1]": {"mean": 0.2},
    "mean_criterion[2]": {"mean": 0.4},
    "mean_criterion[3]": {"mean": 0.5},
}
summary_df = pd.DataFrame.from_dict(summary_data, orient='index')

# Extract rows for convenience
d_prime = [summary_df.loc[f'mean_d_prime[{i}]']['mean'] for i in range(4)]
criterion = [summary_df.loc[f'mean_criterion[{i}]']['mean'] for i in range(4)]

# Compute contrasts
contrast_names = [
    "Stimulus Effect (Easy)",
    "Stimulus Effect (Hard)",
    "Difficulty Effect (Simple)",
    "Difficulty Effect (Complex)"
]

d_contrasts = [
    d_prime[1] - d_prime[0],  # Easy Complex - Easy Simple
    d_prime[3] - d_prime[2],  # Hard Complex - Hard Simple
    d_prime[2] - d_prime[0],  # Hard Simple - Easy Simple
    d_prime[3] - d_prime[1]   # Hard Complex - Easy Complex
]

c_contrasts = [
    criterion[1] - criterion[0],
    criterion[3] - criterion[2],
    criterion[2] - criterion[0],
    criterion[3] - criterion[1]
]

# Combine into one DataFrame
contrast_table = pd.DataFrame({
    "Contrast": contrast_names,
    "Δ d′": d_contrasts,
    "Δ Criterion": c_contrasts
})

# Display table in console
print("\n=== Combined Contrast Table ===")
print(contrast_table.to_string(index=False))

# Save table as CSV
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
contrast_table.to_csv(output_dir / "revised_delta_plots_1_table.csv", index=False)

# Plot both contrasts
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle("SDT Contrast Effects by Stimulus Type and Trial Difficulty")

axs[0].bar(contrast_table["Contrast"], contrast_table["Δ d′"], color='steelblue')
axs[0].set_title("Δ d′ (Sensitivity)")
axs[0].tick_params(axis='x', rotation=45)
axs[0].axhline(0, linestyle='--', color='gray', alpha=0.7)

axs[1].bar(contrast_table["Contrast"], contrast_table["Δ Criterion"], color='salmon')
axs[1].set_title("Δ Criterion (Decision Bias)")
axs[1].tick_params(axis='x', rotation=45)
axs[1].axhline(0, linestyle='--', color='gray', alpha=0.7)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(output_dir / "revised_delta_plots_1.png")
print("Figure saved to output/revised_delta_plots_1.png")
print("Table saved to output/revised_delta_plots_1_table.csv")