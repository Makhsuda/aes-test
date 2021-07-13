import pandas as pd


def change_col_name(filename):
    col_names = pd.read_csv(filename, nrows=1)
    print(col_names)



# reviews_df = pd. read_csv("IMDB Dataset.csv", nrows=100)
# print("Dataframe shape:", reviews_df.shape)

if __name__ == "__main__":
    change_col_name("")