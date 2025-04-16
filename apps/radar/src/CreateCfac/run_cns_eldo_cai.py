
import read_input_parameters
import cns_eldo_cai

param_file = 'DATA_cns.txt'

print("before input_parameters")
input_parameters = read_input_parameters.read_input_parameters(param_file)

cns_eldo_cai.cns_eldo(input_parameters)
