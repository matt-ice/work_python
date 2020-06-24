# Python scripts used at work or in personal projects



## Daily sales 

Automating the execution of a stored procedure in SQL Server, running VBA scripts to refresh all the ODBC connected objects in Excel and creating and sending an email to a distribution
Had an additional bash script to create a virtual drive because of incompatibility with file address in shared drives

## Parkinson's classifier

Personal prject to test out XGBoost library for classification of patients suffering from Parkinson's disease

## Suicides overview

Personal prject to create a view into suicide rates per region, gender and age

## Sudoku solver

Solving a predetermined sudoku in a series of steps 
* checking the rows and columns for existing numbers
* pencil marking in the possible numbers for each cell
* collecting doubles (two cells in a row/column that can only be 2 identical numbers) and removing those from relevant cells in row/column
* entering the only possible number after elimination
* repeating the process until the puzzle is solved

## Excel file processing and sync
Working with 2 different folders, where one has the manually dumped reports and the other that gets synced to AWS S3
* check the number of files between the two folder, the difference is the number of times the main loop runs
* take the last excel upload based on date in filename, delete unneeded rows and columns, name the columns in database friendly way
* save as csv into target folder that gets synced with S3
* iteration over files happens one at a time, so as soon as a file newer than the newest in the target folder is identified, it gets processed
