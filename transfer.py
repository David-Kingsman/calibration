input_file = "data_collection_d435_win/images/poses.txt"
output_file = "poses_m.txt"

with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
    for line in f_in:
        values = line.strip().split(",")
        if len(values) >= 3:
            # 前三个除以 1000
            values[:3] = [str(float(v) / 1000) for v in values[:3]]
        f_out.write(",".join(values) + "\n")
