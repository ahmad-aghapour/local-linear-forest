import math
from typing import List, Tuple, Optional, Set

class Data:

    def __init__(self, data: List[float], num_rows: int, num_cols: int):
        if not data:
            raise ValueError("Invalid data storage: None")
        
        self.data_ptr = data
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.outcome_index = None
        self.treatment_index = None
        self.instrument_index = None
        self.weight_index = None
        self.causal_survival_numerator_index = None
        self.causal_survival_denominator_index = None
        self.censor_index = None
        self.disallowed_split_variables = set()

    # This assumes the data to be in a 2D list. Adjust accordingly.
    def get(self, row: int, col: int) -> float:
        return self.data_ptr[row * self.num_cols + col]

    def set_outcome_index(self, index: List[int]):
        self.outcome_index = index
        self.disallowed_split_variables.update(index)

    def set_treatment_index(self, index: List[int]):
        self.treatment_index = index
        self.disallowed_split_variables.update(index)

    def set_instrument_index(self, index: int):
        self.instrument_index = index
        self.disallowed_split_variables.add(index)

    def set_weight_index(self, index: int):
        self.weight_index = index
        self.disallowed_split_variables.add(index)

    def set_causal_survival_numerator_index(self, index: int):
        self.causal_survival_numerator_index = index
        self.disallowed_split_variables.add(index)

    def set_causal_survival_denominator_index(self, index: int):
        self.causal_survival_denominator_index = index
        self.disallowed_split_variables.add(index)

    def set_censor_index(self, index: int):
        self.censor_index = index
        self.disallowed_split_variables.add(index)

    def get_all_values(self, all_values: List[float], sorted_samples: List[int], samples: List[int], var: int) -> List[int]:
        all_values.clear()
        all_values.extend([self.get(sample, var) for sample in samples])

        index = sorted(range(len(samples)), key=lambda i: all_values[i])

        sorted_samples.clear()
        sorted_samples.extend([samples[i] for i in index])
        all_values[:] = [self.get(sorted_samples[i], var) for i in range(len(samples))]

        unique_values = []
        for val in all_values:
            if val not in unique_values or math.isnan(val):
                unique_values.append(val)
        all_values[:] = unique_values
        
        return index

    def get_num_cols(self) -> int:
        return self.num_cols

    def get_num_rows(self) -> int:
        return self.num_rows

    def get_num_outcomes(self) -> int:
        return len(self.outcome_index) if self.outcome_index else 1

    def get_num_treatments(self) -> int:
        return len(self.treatment_index) if self.treatment_index else 1

    def get_disallowed_split_variables(self) -> Set[int]:
        return self.disallowed_split_variables
