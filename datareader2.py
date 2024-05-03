import pandas as pd

# Load the CSV file
df = pd.read_csv('withengraver-csv.csv')

# Get the top 10 most common values in the first column
top_10_values = df.iloc[:, 0].value_counts().head(10)

# Print the results
print(top_10_values)

# assume 'df' is your pandas dataframe and 'names' is your list of names
names = top_10_values.index.to_list()  # your list of names
print(names)

# create an empty dataframe to store the extracted rows
extracted_rows = pd.DataFrame()

# iterate over the names in your list
for name in names:
    # filter the dataframe to get rows where the first column matches the current name
    name_rows = df[df.iloc[:, 0] == name]
    
    
    # randomly sample 10 rows from the filtered dataframe (or fewer if there aren't 10)
    sampled_rows = name_rows.sample(min(100, len(name_rows)))
    
    # append the sampled rows to the extracted_rows dataframe
    extracted_rows = pd.concat([extracted_rows, sampled_rows])
    print(extracted_rows)

# reset the index of the extracted_rows dataframe
extracted_rows.reset_index(drop=True, inplace=True)
print(extracted_rows)
extracted_rows.to_csv('out.csv', index=False) 