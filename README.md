# npmemory
NumPy memory editing for efficient array calculations.

Results for sample routine:

| Box Averaging | Pure Python (ms) | Python with memory editing (ms) | Speed factor |
|---|---|---|---|
| Windows 10 | 2015 ms | 18 ms | 112x |
| Linux | 1422 ms | 13 ms | 107x |

Note: Tested on Intel i9-9880

Graph showing speed increase

## Windows Setup

Step 1: Install the 64-bit TDM GCC compiler from the following link:
https://jmeubank.github.io/tdm-gcc/ Ensure that you select 'TDM GCC MinGW w64'

Step 2: git clone https://github.com/Fletcher-Climate-Group/npmemory

Step 3: Run 'python cross_compile.py'

## Linux Setup

Step 1: Install the latest version of *gcc* for your distribution

Step 2: git clone https://github.com/Fletcher-Climate-Group/npmemory

Step 3: Run 'python cross_compile.py'


## Mac OSX Setup

Step 1: Install the latest version of *gcc* using Homebrew

Step 2: git clone https://github.com/Fletcher-Climate-Group/npmemory

Step 3: Run 'python cross_compile.py'


## Quick Start (all operating systems)

Once you have compiled the npmemory module for your OS, run the following example report
to ensure the memory editing works correctly.

```sh
cd examples
python report.py
```

This should return a report which compares the speed differential between a pure
Python routine and the C-augmented memory editing routine.
