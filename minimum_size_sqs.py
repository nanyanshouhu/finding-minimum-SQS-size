import numpy as np
from math import gcd
from fractions import Fraction
from itertools import combinations

def read_atomic_positions_v4(file_lines):
    atomic_positions = []
    for line in file_lines[4:]:
        parts = line.strip().split()
        if len(parts) >= 4:
            position = list(map(float, parts[:3]))
            species_info = ' '.join(parts[3:]).strip()
            atomic_positions.append((position, species_info))
    return atomic_positions

def extract_mixed_info_v8(atomic_positions):
    mixed_count = 0
    mix_fractions = []
    mixed_species_indicator = []

    for _, species in atomic_positions:
        if "=" in species and "," in species:
            species_parts = [part.strip() for part in species.split(',')]
            fractions = []

            for part in species_parts:
                if '=' in part:
                    split_part = part.split('=')
                    if len(split_part) == 2:
                        try:
                            fraction_value = float(split_part[1].strip())
                            fractions.append(fraction_value)
                        except ValueError:
                            continue

            if fractions and abs(sum(fractions) - 1.0) < 1e-6:
                mixed_count += 1
                mix_fractions.append(fractions)
                mixed_species_indicator.append(species)

    return mixed_count, mix_fractions, mixed_species_indicator

def lcm(x, y):
    return (x * y) // gcd(x, y)

def calculate_lcm_multiple(numbers):
    current_lcm = numbers[0]
    for number in numbers[1:]:
        current_lcm = lcm(current_lcm, number)
    return current_lcm

def calculate_min_denominator_custom(fractions, combination_size=2):
    min_denominators = []

    for combo in combinations(fractions, combination_size):
        product_fraction = np.prod(combo)
        min_denominator = Fraction(product_fraction).limit_denominator().denominator
        min_denominators.append(min_denominator)

    overall_min_denominator = calculate_lcm_multiple(min_denominators)
    return overall_min_denominator

def calculate_target_mixed_atoms_individual(mixed_count, mix_fractions, combination_size=2):
    target_mixed_atoms_list = []
    min_denominator_list = []

    for fractions in mix_fractions:
        min_denominator = calculate_min_denominator_custom(fractions, combination_size)
        target_mixed_atoms = min_denominator

        min_denominator_list.append(min_denominator)
        target_mixed_atoms_list.append(target_mixed_atoms)

    return target_mixed_atoms_list, min_denominator_list

def generate_scaled_supercell(atomic_positions, lcm_target_atoms):
    scaling_factor = lcm_target_atoms
    supercell_atoms = []

    for pos, species in atomic_positions:
        for i in range(scaling_factor):
            scaled_pos = np.mod(np.array(pos) + i / scaling_factor, 1.0)
            supercell_atoms.append((scaled_pos, species))

    return supercell_atoms, scaling_factor

def count_species(atomic_positions):
    species_count = {}
    for _, species in atomic_positions:
        if species not in species_count:
            species_count[species] = 0
        species_count[species] += 1
    return species_count

def generate_general_supercell_individual(file_path, combination_size=2):
    with open(file_path, 'r') as file:
        file_lines = file.readlines()

    atomic_positions = read_atomic_positions_v4(file_lines)
    original_mixed_count, mix_fractions, mixed_species_indicator = extract_mixed_info_v8(atomic_positions)

    target_mixed_atoms_list, min_denominator_list = calculate_target_mixed_atoms_individual(original_mixed_count, mix_fractions, combination_size)

    # Calculate the LCM of target mixed atoms for all mixed sites
    lcm_target_atoms = calculate_lcm_multiple(target_mixed_atoms_list)

    # Generate the scaled supercell using the LCM of target mixed atoms
    supercell_atoms, scaling_factor = generate_scaled_supercell(atomic_positions, lcm_target_atoms)

    species_count = count_species(supercell_atoms)
    total_atoms = len(supercell_atoms)

    return supercell_atoms, species_count, total_atoms, scaling_factor, lcm_target_atoms, original_mixed_count, mix_fractions, min_denominator_list, target_mixed_atoms_list

# Example usage: Replace 'file_path' with the actual path to your input file
file_path = "rndstr.in"
combination_size = 2

# Generate supercell and get results
(supercell_atoms, species_count, total_atoms, scaling_factor, 
 lcm_target_atoms, original_mixed_count, mix_fractions, 
 min_denominator_list, target_mixed_atoms_list) = generate_general_supercell_individual(file_path, combination_size)

# Display the results
print("Original Mixed Count:", original_mixed_count)
print("Mix Fractions:", mix_fractions)
print("Combination Size:", combination_size)
print("Minimum Denominators (per site):", min_denominator_list)
print("Target Mixed Atoms (per site):", target_mixed_atoms_list)
print("LCM of Target Mixed Atoms:", lcm_target_atoms)
print("Species Count:", species_count)
print("Total Atoms:", total_atoms)
print("Scaling Factor (LCM):", scaling_factor)
