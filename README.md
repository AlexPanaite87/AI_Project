# AI_Project - CSP Sudoku using the Forward Checking algorithm

A Sudoku solver will be implemented, treated as a Constraint Satisfaction Problem (CSP), using the Forward Checking algorithm. Each cell represents a variable with a specific domain, and when a cell is completed, the algorithm will eliminate incompatible values from the neighboring domains (row, column, block), performing backtracking if a domain becomes empty. The application will display the initial puzzle and the final solution.
