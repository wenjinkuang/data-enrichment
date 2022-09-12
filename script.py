import pandas as pd 

## loading the CSV datasets 
sparcs = pd.read_csv(r'data\Hospital_Inpatient_Discharges__SPARCS_De-Identified___2015.csv')
neighborhood = pd.read_csv(r'data\NY_2015_ADI_9 Digit Zip Code_v3.1.csv')

## confirming the datasets has been loaded 
print(sparcs,'/n',neighborhood)

## looking at the amount of rows and columns within the datasets 
sparcs.shape
neighborhood.shape

## looking at what columns are within the different datasets
sparcs.columns
neighborhood.columns 

###############  Data Cleaning  ###############

## removing all special characters and whitespaces 
sparcs.columns = sparcs.columns.str.replace('[^A-Za-z0-9]+', '_')
neighborhood.columns = neighborhood.columns.str.replace('[^A-Za-z0-9]+', '_')

## turning all column names into lowercase for easy coding
sparcs.columns = sparcs.columns.str.lower()
neighborhood.columns = neighborhood.columns.str.lower()

## testing if code worked 
sparcs.columns
neighborhood.columns 

## making a new column where the values are the first 3 digits of 'zipid' after 'G' of neighborhood for a successful merge later on
neighborhood['zip_3'] = neighborhood['zipid'].str.slice(1, 4)
neighborhood

###############  Data Enrichment  ###############

## selecting the needed columns of the datasets to lessen confnusion and confirming the command has worked 
sparcs_small = sparcs[[
    'zip_code_3_digits',
    'facility_id',
    'hospital_county',
    'age_group',
    'total_charges',
    'total_costs',
    'apr_severity_of_illness_code',
    'type_of_admission',
    'ccs_diagnosis_code',
    'ccs_diagnosis_description',
]]
neighborhood_small = neighborhood[['zip_3','adi_natrank','adi_staternk']]
sparcs_small
neighborhood_small

## code to use for merging the two tables 
### enriched = sparcs_small.merge(neighborhood_small, how='left', left_on='zip_code_3_digits', right_on='zip_3') ###
## code is written in notes is due to the larger size of the tables, thus a smaller version of the merge is below 

sparcs_small_small = sparcs_small.sample(50)
neighborhood_small_small = neighborhood_small.sample(50)

enriched_small = sparcs_small_small.merge(neighborhood_small_small, how='left', left_on='zip_code_3_digits', right_on='zip_3')
enriched_small

enriched_small.to_csv(r'data/enriched_small.csv')