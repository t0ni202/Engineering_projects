"""
This module is designed to calculate the Madelung constant for a given lattice structure. 
The Madelung constant is an important parameter in solid-state physics and chemistry, representing 
the electrostatic sum of interactions in ionic crystals. This module likely includes functions to sum over
lattice points and calculate the Madelung constant for specific types of crystal structures. It's useful in 
the fields of crystallography, materials science, and condensed matter physics.
"""


def apply_madelung(Z: int) -> str:
    """
    Calculates the electronic configuration of an element based on the Madelung rule.

    Args:
        Z (int): Atomic number of the element.

    Returns:
        str: Electronic configuration string of the element.
    """

    azim = ["s", "p", "d", "f"]
    e_configuration_string = ""
    n_plus_ell = 1

    s_count = 1
    p_count = 2
    d_count = 3
    f_count = 4

    n = 1

    while 0 < Z < 105:
        for _ in range(2):
            l = len(azim[:n_plus_ell - 1])
            for orbital in reversed(azim[:n_plus_ell]):
                num_placed = 2 * (2 * l + 1)
                if orbital == "s":
                    n = s_count
                    s_count += 1
                elif orbital == "p":
                    n = p_count
                    p_count += 1
                elif orbital == "d":
                    n = d_count
                    d_count += 1
                elif orbital == "f":
                    n = f_count
                    f_count += 1

                if Z > num_placed:
                    Z -= num_placed
                    e_configuration_string += f"{n}{orbital}{num_placed}-"
                    l -= 1
                elif Z <= 0:
                    break
                else:
                    e_configuration_string += f"{n}{orbital}{Z}"
                    Z -= num_placed
                    break

        n_plus_ell += 1

    return e_configuration_string


if __name__ == "__main__":
    Z = 73
    print(f"The electronic configuration of tungsten (Z={Z:d}) is:\n {apply_madelung(Z)}")

