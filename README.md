# OPL ISO Manager

A simple Python script to help manage PS2 ISO files for use with Open PS2 Loader (OPL).

## Features

*   Convert standard ISO files to OPL-compatible format.
*   Split large ISO files (> 4GB) into smaller parts for FAT32 file systems.

## Prerequisites

*   Python 3.x
*   OPL Toolkit: You need to have `iso2opl` and `opl-split` command-line tools installed and accessible in your system's PATH. You can find these tools as part of various OPL-related software packages online.

## How to Use

1.  **Clone or download the repository.**
2.  **Open a terminal or command prompt.**
3.  **Navigate to the directory where you saved the script.**
4.  **Run the script:**
    ```bash
    python opl_manager.py
    ```
5.  **Follow the on-screen menu:**
    *   Choose option `1` to convert ISOs. You'll be prompted for the input directory (where your ISOs are) and the output directory (where the converted files will be saved).
    *   Choose option `2` to split large ISOs. You'll be prompted for the input directory and the output directory for the split files.
    *   Choose option `3` to exit the program.

## Disclaimer

This script relies on external command-line tools (`iso2opl`, `opl-split`). The author of this script is not responsible for any damage or data loss that may occur from using this software. Always back up your important files.
