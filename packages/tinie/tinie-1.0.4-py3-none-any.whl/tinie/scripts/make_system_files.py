#!/usr/bin/env python3
"""
A script for generating custom system couplings/hamiltonians.
"""
from typing import List, Text

import numpy as np


def ask_int(query: Text) -> int:
    """

    Parameters
    ----------
    query : Text
        Query-string

    Returns
    -------
    int
    """
    while True:
        try:
            return int(input(f"{query}: ").strip())
        except ValueError:
            print("Could not interpret the input as an integer.")


def ask_float_array(query: Text, expected_length: int) -> List[float]:
    """

    Parameters
    ----------
    query : Text
        Query-string
    expected_length : int
        Expected length of the array

    Returns
    -------
    List[float]
    """
    while True:
        try:
            user_input = input(f"{query}: ").strip()
            numbers = user_input.split(' ')
            if len(numbers) != expected_length:
                raise ValueError("Length of the input array not what was expected: {len(numbers)} vs {"
                                     "expected_length}")
            return [float(num) for num in numbers]

        except ValueError as e:
            print(e)

def ask_complex_array(query: Text, expected_length: int) -> List[np.complex]:
    """

    Parameters
    ----------
    query : Text
        Query-string
    expected_length : int
        Expected length of the array

    Returns
    -------
    List[float]
    """
    while True:
        try:
            user_input = input(f"{query}: ").strip()
            numbers = user_input.split(' ')
            if len(numbers) != expected_length:
                raise ValueError("Length of the input array not what was expected: {len(numbers)} vs {"
                                 "expected_length}")
            return [np.complex(c) for c in numbers]
        except ValueError as e:
            print(e)

def ask_complex_matrix(query: Text, expected_rowsize: int, expected_columnsize: int) -> np.ndarray:
    """

    Parameters
    ----------
    query :
    expected_rowsize :
    expected_columnsize :

    Returns
    -------

    """
    mat = np.empty((expected_rowsize, expected_columnsize), dtype=np.complex)
    for i in range(expected_rowsize):
        mat[i,:] = ask_complex_array(f"row {i}", expected_columnsize)
    return mat


def generate_custom_hamiltonian():
    """
    Generates a custom Hamiltonian and stores it in a .npy file.
    """

    state_num = ask_int("Enter the number of eigenenergies")

    hamiltonian = np.empty((state_num,), dtype=float)

    filename_default = "data/custom_hamiltonian"

    hamiltonian[:] = ask_float_array("Enter the eigenenenergy values separated by spaces", expected_length=state_num)

    print("Hamiltonian imported")

    filename = input(
        "Now specify the output file name, default is " + filename_default + ": ")

    if filename == "":
        np.save(filename_default, hamiltonian)
        print(
            "Hamiltonian successfully saved at " +
            filename_default + ".npy")

    else:
        np.save(filename, hamiltonian)
        print("Hamiltonian successfully saved at " + filename + ".npy")


def generate_custom_coupling():
    """
    Generates a custom coupling matrix and stores it in a .npy file.
    """

    state_num_ld = ask_int("Enter number of states in the lead")
    state_num_ctr = ask_int("Enter number of states in the central region")

    cpl_matrix = np.zeros((state_num_ld, state_num_ctr), dtype=np.complex128)
    filename_default = "data/custom_coupling"

    print("Here is a little tutorial:")
    print("Enter your matrix row-by-row space separated.")
    print("Complex values are allowed and can be typed in as e.g. "
          "1.+1.j, j is the complex unit")

    cpl_matrix = ask_complex_matrix("Input coupling matrix row-by-row", state_num_ld, state_num_ctr)

    print("Matrix imported")
    filename = input(
        "Now specify the file name, default is " + filename_default + ": ")

    if filename == "":
        np.save(filename_default, cpl_matrix)
        print("Coupling matrix successfully saved at " +
              filename_default + ".npy")

    else:
        np.save(filename, cpl_matrix)
        print("Coupling matrix successfully saved at " +
              filename + ".npy")


def user_interface():
    print("This script can be used to create custom Hamiltonians and custom")
    print("coupling matrices to be used in "
          "CustomCenter/CustomLead/CustomCoupling")
    print("classes.")
    print()

    while True:
        print("Would you like to generate a Hamiltonian ('h'), "
              "or a coupling matrix ('c')?")
        usr_input = input("Press 'q' to quit: ")

        if usr_input == 'h':
            generate_custom_hamiltonian()

        elif usr_input == 'c':
            generate_custom_coupling()

        elif usr_input == 'q':
            print("Goodbye!")
            break

        else:
            print("Invalid input! Type 'h' for Hamiltonian, "
                  "'c' for coupling matrix")
            print("and 'q' to quit.")


if __name__ == '__main__':
    user_interface()