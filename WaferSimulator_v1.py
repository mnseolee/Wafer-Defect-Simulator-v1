import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#--Making Wafer Geometry--
grid = np.zeros((20,20))
center_y, center_x = (9.5, 9.5)
y_grid, x_grid = np.indices(grid.shape)
distance = np.sqrt((x_grid - center_x)**2 + (y_grid - center_y)**2)
distance_limit = 9
is_valid = np.where(distance < distance_limit, True, False)
near_edge = (distance_limit - distance) < 0.75

#--Applying Defects and Performance Score--
rows = []
cols = []
die_ids = []
defect_types = []
performance_score = []
for row in range(20):
    for col in range(20):
        if is_valid[row, col]:
            rows.append(row)
            cols.append(col)
            die_ids.append(row * 20 + col)
            base_defect = np.random.choice(["none", "particle", "lithography"], p=[0.8, 0.11, 0.09])
            if near_edge[row, col]:
                final_defect = np.random.choice([base_defect, "edge"], p=[0.15, 0.85])
            else:
                final_defect = base_defect
            defect_types.append(final_defect)
            if final_defect == "none":
                score = np.random.uniform(90, 100)
            elif final_defect == "particle":
                score = np.random.uniform(40, 87)
            elif final_defect == "lithography":
                score = np.random.uniform(50, 90)
            elif final_defect == "edge":
                score = np.random.uniform(0,85)
            performance_score.append(score)
df = pd.DataFrame({
    "die_ids" : die_ids,
    "rows" : rows,
    "cols" : cols,
    "defect_types" : defect_types,
    "performance_score" : performance_score
})

#--Wafer Statistics--
valid_count = len(df[df["performance_score"] >= 80])
overall_yield = valid_count / len(df)
defects_count = df["defect_types"].value_counts()
print(f"Dies with performance >= 80: {valid_count}")
print(f"Overall yield: {overall_yield:.2%}")
print(defects_count)

#--Matplotlib for Visuals--
plt.scatter(df["cols"], df["rows"], c=df["performance_score"])
plt.colorbar()

color_map = {
    "none" : "green",
    "particle" : "orange",
    "lithography" : "pink",
    "edge" : "purple"
}
plt.figure()
for defect in df["defect_types"].unique():
    subset = df[df["defect_types"] == defect]
    plt.scatter(subset["cols"], subset["rows"], label=defect, color=color_map[defect])
plt.legend()
plt.show()