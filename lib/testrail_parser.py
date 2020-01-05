import pandas as pd

class TestrailParser():

    def __init__(self, referenced_field):
        self.referenced_field = referenced_field
        self.data_frame = pd.DataFrame(columns=self.referenced_field)
        self.data_frame = self.data_frame.set_index(self.referenced_field[0])
        pass

    def read_csv(self, file_path):
        df = pd.read_csv(file_path)
        selected_df = df[self.referenced_field]
        selected_df.set_index(self.referenced_field[0], drop=True, inplace=True)
        self.data_frame = self.data_frame.append(selected_df)

    def get_json(self):
        return self.data_frame.to_dict(orient="index")