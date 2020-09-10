# Purpose of this program is to provide a quick and easily accessible method to convert ISO 4406:1999 Cleanliness Codes to NAS 1683 Cleanliness Codes and SAE SA 4059 Classes
# Primarily only one customer uses the NAS 1683 and SAE SA 4059 Classes.
# However, the same input data is used to calculate the ISO 4406:1999 so the calculator can have a general use purpose outside of that customer. Even though it is designed for their reports.

import time

# ISO 4406:1999 Particle Count ISO Code dictionary
# Str(Code): [Minimum, Maximum]
# Number of particles per 1 ml
iso_4406 = {
    " 1": [0.01, 0.02],
    " 2": [0.02, 0.04],
    " 3": [0.04, 0.08],
    " 4": [0.08, 0.16],
    " 5": [0.16, 0.32],
    " 6": [0.32, 0.64],
    " 7": [0.64, 1.30],
    " 8": [1.30, 2.50],
    " 9": [2.50, 5.00],
    "10": [5.00, 10.00],
    "11": [10.00, 20.00],
    "12": [20.00, 40.00],
    "13": [40.00, 80.00],
    "14": [80.00, 160.00],
    "15": [160.00, 320.00],
    "16": [320.00, 640.00],
    "17": [640.00, 1300.00],
    "18": [1300.00, 2500.00],
    "19": [2500.00, 5000.00],
    "20": [5000.00, 10000.00],
    "21": [10000.00, 20000.00],
    "22": [20000.00, 40000.00],
    "23": [40000.00, 80000.00],
    "24": [80000.00, 160000.00],
    "25": [160000.00, 320000.00],
    "26": [320000.00, 640000.00],
    "27": [640000.00, 1300000.00],
    "28": [1300000.00, 2500000.00],
}

# HFDU Glycounter Micron Size Experimental Ranges
# The HFC/HFA Glycounter uses different ranges
micron_sizes = [' 4.0', ' 6.0', '10.0', '14.0', '21.0', '25.0', '30.0', '38.0', '70.0']

# NAS 1638 Particle Count Code Dictionary
# Str(Code) = [5-15 Micron, 15-25 Micron, 25-50 Micron, 50-100 Micron, >100 Micron]
# Number of particles per 100 mL
nas_1683 = {
    "N12": [1024000.00, 182400.00, 32400.00, 5760.00, 1024.00],
    "M11": [512000.00, 91200.00, 16200.00, 2880.00, 512.00],
    "L10": [256000.00, 45600.00, 8100.00, 1440.00, 256.00],
    "K 9": [128000.00, 22800.00, 4050.00, 720.00, 128.00],
    "J 8": [64000.00, 11400.00, 2025.00, 360.00, 64.00],
    "I 7": [32000.00, 5700.00, 1012.00, 190.00, 32.00],
    "H 6": [16000.00, 2850.00, 506.00, 90.00, 16.00],
    "G 5": [8000.00, 1425.00, 253.00, 45.00, 8.00],
    "F 4": [4000.00, 712.00, 126.00, 22.00, 4.00],
    "E 3": [2000.00, 356.00, 63.00, 11.00, 2.00],
    "D 2": [1000.00, 178.00, 32.00, 6.00, 1.00],
    "C 1": [500.00, 89.00, 16.00, 3.00, 1.00],
    "B 0": [250.00, 44.00, 8.00, 2.00, 0.00],
    "A00": [125.00, 22.00, 4.00, 1.00, 0.00],
}

# Designed for use in command line. Also provides background information for unfamiliar user
# Having contact in case of errors/issues is important to expedite corrections
calculator_header = """
------------------------------------------------------------------------------
//////////////////////////////////////////////////////////////////////////////
------------------------------------------------------------------------------

     *** Fluid Analysis HFDU Particle Count Calculator --- Version 1.0 ***
                 --- Generates ISO 4406 Cleanliness Codes ---
                 --- Generates NAS 1683 Cleanliness Codes ---
                 --- Generates SAE SA 4059 Classes ---

------------------------------------------------------------------------------

Programed by Jonathan Shamberg [Jonathan.Shamberg@quakerhoughton.com]
Developed for use by Quaker Houghton
Last Updated: 03/29/2020

-------------------------------------------------------------------------------
///////////////////////////////////////////////////////////////////////////////
-------------------------------------------------------------------------------
"""


# The same 9 experimental data points are used for all three calculations
def data_input(start=0):
    # There are a maximum of 9 inputs. This is a constant
    target_size = start
    input_avg_counts = []
    while target_size <= 8:
        try:
            exp_count = input(f"Average {micron_sizes[target_size]}\u03BCm count:  ")
            exp_count = float(exp_count)
        except ValueError:
            print(f"Input a numerical value.")
            continue
        else:
            input_avg_counts.append(exp_count)
            target_size += 1
    return input_avg_counts


def iso_cleanliness_code(exp_data=[]):
    codes = []
    modified_counts = []
    if input_data_check(exp_data, 9) is True:

        # micron_sizes = [' 4.0', ' 6.0', ' 10.0', ' 14.0', '21.0', '25.0', '30.0', '38.0', '70.0']
        four_micron = exp_data[0]
        modified_counts.append(four_micron)

        six_micron = exp_data[1]
        modified_counts.append(six_micron)

        fourteen_micron = exp_data[3]
        modified_counts.append(fourteen_micron)

        for count in modified_counts:
            for key in iso_4406:
                if iso_4406[key][0] < count <= iso_4406[key][1]:
                    codes.append(key)
        return codes

    else:
        codes = ["N/A", "N/A", "N/A"]
        return codes


def nas_cleanliness_codes(exp_data=[], qty_codes=4):
    code = []
    for num in range(0, qty_codes):
        code.append('N')
    combined_counts = []
    previous_max = 0
    if input_data_check(exp_data, 9) is True:
        # micron_sizes = [' 4.0', ' 6.0', ' 10.0', ' 14.0', '21.0', '25.0', '30.0', '38.0', '70.0']
        # NAS 1683 starts at 5um, so the 4.0um can be ignored for this calculation
        # 5-15um
        segment1 = exp_data[1] + exp_data[2] + exp_data[3]
        combined_counts.append(segment1)

        # 12-25um
        segment2 = exp_data[4] + exp_data[5]
        combined_counts.append(segment2)

        # 25-50um
        segment3 = exp_data[6] + exp_data[7]
        combined_counts.append(segment3)

        # 50-100um
        segment4 = exp_data[8]
        combined_counts.append(segment4)

        # >100um
        # doesn't exist in our ISO experimental data

        for size in range(0,4):
            for key in nas_1683:
                nas_100ml = combined_counts[size] * 100
                if nas_100ml < nas_1683[key][size]:
                    code[size] = key

        return max(code)

    else:
        codes = [" N/A"]
        return codes


def sae_cleanliness_codes(exp_data=[], qty_codes=5):
    sae_codes = []
    combined_counts = []
    nas_range = []
    for num in range(0, qty_codes):
        sae_codes.append('S')

    if input_data_check(exp_data, 9) is True:
        # micron_sizes = [' 4.0', ' 6.0', ' 10.0', ' 14.0', '21.0', '25.0', '30.0', '38.0', '70.0']
        # NAS 1683 starts at 5um, so the 4.0um can be ignored for this calculation
        # >  4um

        # >  6um
        segment2 = exp_data[1] + exp_data[2]
        combined_counts.append(segment2)
        nas_range.append(0)  # 5 - 15 um
        # > 14um
        segment3 = exp_data[3]
        combined_counts.append(segment3)
        nas_range.append(0)  # 5 - 15 um
        # > 21um
        segment4 = exp_data[4] + exp_data[5] + exp_data[6]
        combined_counts.append(segment4)
        nas_range.append(1)  # 15 - 25 um
        # > 38um
        segment5 = exp_data[7]
        combined_counts.append(segment5)
        nas_range.append(2)  # 25 - 50 um
        # > 70um
        segment6 = exp_data[8]
        combined_counts.append(segment6)
        nas_range.append(3)  # 50 - 100 um

        for num in range(0, len(sae_codes)):
            nas_100ml = combined_counts[num] * 100
            micron_range = nas_range[num]
            for key in nas_1683:
                if nas_100ml < nas_1683[key][micron_range]:
                    sae_codes[num] = key

        return sae_codes


def input_data_check(exp_data=[], qty_data_points=0, data_type=type(0.0)):
    if len(exp_data) < qty_data_points:
        print("No Data to work with")
        return False

    for value in exp_data:
        if isinstance(value, data_type) is True:
            continue
        else:
            return False

    return True


def calculator():
    avg_counts = data_input()
    iso_codes = iso_cleanliness_code(exp_data=avg_counts)
    nas_code = nas_cleanliness_codes(exp_data=avg_counts)
    sae_codes = sae_cleanliness_codes(exp_data=avg_counts)
    print("\nCalculating... ...\n")
    time.sleep(1)  # Because I can, no real purpose
    # Result display formatted to represent report layout.
    print("SAE Cleanliness SAE SA 4059")
    print("> 4\u03BCm  Class: N/A")  # Report leaves a blank, but is not used
    print(f"> 6\u03BCm  Class: {sae_codes[0][1:]}")
    print(f"> 14\u03BCm Class: {sae_codes[1][1:]}")
    print(f"> 21\u03BCm Class: {sae_codes[2][1:]}")
    print(f"> 38\u03BCm Class: {sae_codes[3][1:]}")
    print(f"> 70\u03BCm Class: {sae_codes[4][1:]}")
    print(f"ISO 4406 Cleanliness Codes: {iso_codes[0]}/{iso_codes[1]}/{iso_codes[2]} (4.0\u03BCm/6.0\u03BCm/14.0\u03BCm)")
    print(f"NAS 1683 Cleanliness Code: {nas_code[1:]}")
    print("---------------------------------------------------------------------------")


if __name__ == "__main__":
    print(calculator_header)
    print("Starting Calculator. Follow prompts and Hit enter to submit values")
    print("Round the Average counts to the nearest whole number and input as is.\n")
    time.sleep(1)
    calculator()
    while True:
        n = input("Do you want to input another sample? [y/n]  ")
        if n == "y":
            print("")
            calculator()
        elif n == "n":
            break
    print("goodbye")
    # nsa_codes = iso_cleanliness_code()
