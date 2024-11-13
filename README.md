# Secure Erasure Code
## Overview

The Secure Erasure Code project is designed to securely erase data from storage devices, ensuring that sensitive information cannot be recovered. This tool utilizes cryptographic techniques and secure data wiping algorithms to make the erasure process both efficient and reliable. The project is aimed at ensuring compliance with data security standards and protecting sensitive data in various environments such as government, enterprise, and personal use.
Features

    Secure Data Erasure: Uses advanced algorithms to securely overwrite data, ensuring it cannot be recovered using standard data recovery tools.
    Multiple Erasure Algorithms: Implements a variety of cryptographic algorithms for secure erasure, including those recommended by security standards such as DoD 5220.22-M and NIST 800-88.
    File and Disk Erasure: Supports secure erasure of both individual files and entire disks, making it versatile for different use cases.
    Logging and Verification: Provides detailed logs of the erasure process and offers verification to ensure data has been successfully erased.
    Cross-Platform: Compatible with major operating systems, including Windows, macOS, and Linux.

## Installation
Prerequisites

Before installing Secure Erasure Code, make sure your system meets the following requirements:

    Python 3.6 or higher
    Administrator (root) access for disk operations

## Installing

    Clone this repository:

git clone https://github.com/somulo1/secure-erasure-code.git

cd secure-erasure-code

Install dependencies:


    pip install -r requirements.txt

    (Optional) If you wish to use the erasure tool for disk-level erasure, ensure you have administrator privileges:
        For Linux/macOS, use sudo for privileged commands.
        For Windows, run the command prompt as Administrator.

## Usage

Secure Erasure of Files

To securely erase a file, run the following command:

python secure_erasure.py --erase-file /path/to/file

This will securely overwrite the file at the specified location using a defined erasure algorithm.
Secure Erasure of Entire Disk

To securely erase a disk (all partitions and data), run:

python secure_erasure.py --erase-disk /dev/sdX

Replace /dev/sdX with the target disk identifier (e.g., /dev/sda for Linux or \\.\PhysicalDrive0 for Windows).
Available Algorithms

You can choose from the following erasure algorithms:

    DoD 5220.22-M: A U.S. Department of Defense standard for secure erasure.
    NIST 800-88: A standard for media sanitization.
    Random Overwrite: Random data overwrite to ensure irrecoverability.
    Cryptographic Erasure: Overwrites using a secure cryptographic method.

Specify the algorithm using the --algorithm flag:

python secure_erasure.py --erase-file /path/to/file --algorithm DoD5220

Verifying Erasure

After performing an erasure, you can verify it by running the verification tool:

python secure_erasure.py --verify /path/to/file

This will check the integrity and confirm that the data has been overwritten.
Security Considerations

    Data Integrity: After erasure, the original data is unrecoverable, making it suitable for compliance with privacy and security regulations.
    Multiple Overwrites: The project allows you to configure the number of overwrites, offering enhanced security for highly sensitive data.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository, create a feature branch, and submit a pull request. For larger changes, please open an issue to discuss the modifications.
Reporting Bugs

To report bugs or security vulnerabilities, please open an issue in the repository or contact the project maintainers directly.
License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgements

    This project is based on cryptographic standards and guidelines recommended by NIST and the DoD.
    Special thanks to the open-source community for providing tools and libraries used in the implementation of secure erasure algorithms.

Contact

For further inquiries or support, please contact:

    Email: mcomulosammy37@gmail.com
    GitHub: somulo1