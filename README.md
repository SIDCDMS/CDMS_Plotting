# CDMS_Plotting
Python algorithm used to directly plot the resulting m/z values in 2D against the resulting charge and mass from Orbitrap-based Charge Detection Mass Spectrometry (CDMS) Data.

Please cite us if you use CDMS_Ploting in your research. It was originally published in: Du, C.; Cleary, S. P.; Kostelic, M. M.; Jones, B. J.; Kafader, J. O.; Wysocki, V. H. Combining Surface-Induced Dissociation and Charge Detection Mass Spectrometry to Reveal the Native Topology of Heterogeneous Protein Complexes. Analytical Chemistry 2023, 95 (37), 13889-13896. DOI: 10.1021/acs.analchem.3c02185.

Please contact mseanpatcleary@gmail.com and chendu.9mail@gmail.com for questions, suggestions, or with any bugs.

Instructions:

1.	Open the DMT raw file in an SQLite database browser. Various open-source tools are available.
   
2.	Browse ion table and export it to CSV file. Specify the options for the CSV file (such as the delimiter and quote character) and choose a location to save the file.
Note: the data filters in STORIboard affect the exported ion CSVs.

3.	Input charge calibration coefficient in plotting scripts
Note: Charge calibration coefficient is instrument dependent and calibrated using protein standards.

4.	Adjust the bins of mz, mass and charge accordingly in scripts
Note: RSquared and TimeofBirth filters can also be custom defined in scripts to be narrower windows in addition to the filers in STORIboard.

5.	Run file with custom configuration and input CSV file name
Note: Scripts and CSV files need to be in the root location otherwise the file location needs to be configured additionally.

