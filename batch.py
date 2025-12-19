import pandas as pd
import os


input_file = 'D:\proo1\pro1\data\products-0-200000.csv'
output_directory = 'D:\proo1\pro1'
batch_size =10

all_product_id = pd.read_csv(input_file)

total_row = len(all_product_id)
num_batches = ((total_row)//batch_size) + 1

for i in range(num_batches):
    start_index = i * batch_size
    end_index = min((i+1)*batch_size,total_row)

    batch_df = all_product_id.iloc[start_index:end_index]

    output_filename = f'batch_{i+1:03d}.csv'

    full_output_path = os.path.join(output_directory,output_filename)

    batch_df.to_csv(full_output_path,index=False)

