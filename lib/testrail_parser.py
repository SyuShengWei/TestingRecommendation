import pandas as pd

class TestrailParser():

    def __init__(self, referenced_field):
        self.referenced_field = referenced_field
        self._data_frame = pd.DataFrame(columns=self.referenced_field)
        self._data_frame = self._data_frame.set_index(self.referenced_field[0])
        pass

    def read_csv(self, file_path):
        df = pd.read_csv(file_path)
        selected_df = df[self.referenced_field]
        selected_df.set_index(self.referenced_field[0], drop=True, inplace=True)
        self._data_frame = self._data_frame.append(selected_df)

    def get_json(self):
        return self._data_frame.to_dict(orient="index")
