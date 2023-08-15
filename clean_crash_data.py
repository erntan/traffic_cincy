import warnings 
warnings.filterwarnings('ignore', ".*`df\.iloc\[:, i\] = newvals`.*", FutureWarning)
# Script to clean crash data
import pandas as pd 

crash_raw = pd.read_csv("Traffic_Crash_Reports__CPD_.csv", dtype={'CRASHLOCATION':'string', 'ZIP':'string', 'LOCALREPORTNO':'string', 'CRASHSEVERITYID':'string'})
print("CSV has been read.")

crash_data = crash_raw.copy()

crash_data.columns = crash_data.columns.str.lower()

## Convert data types
# Strings to dates
crash_data.loc[:, 'crashdate'] = pd.to_datetime(crash_data.crashdate)
crash_data.loc[:, 'datecrashreported'] = pd.to_datetime(crash_data.datecrashreported)

print("Data types have been converted.")

# Numbers to strings
crash_data.loc[:, 'localreportno'] = crash_data.localreportno.apply(str )
crash_data.loc[:, 'crashseverityid'] = crash_data.crashseverityid.apply(str)

# Stripping the trailing zeros from ZIP 
# crash_data.loc[:,'zip'] = crash_data.zip.astype(str)
crash_data.loc[:,'zip'] = crash_data.zip.str[:5]

## Splitting fields - Separate scores from descriptions
crash_data[['crashseverity','crashseveritydescr']] = crash_data.crashseverity.str.split(pat=' - ', expand=True)
crash_data.crashseverity = crash_data.crashseverity.astype('Int64')

crash_data[['roadcontour','roadcontourdescr']] = crash_data.roadcontour.str.split(pat=' - ', expand=True)
crash_data.roadcontour = crash_data.roadcontour.astype('Int64')

crash_data[['mannerofcrash', 'mannerofcrashdescr']] = crash_data.mannerofcrash.str.split(pat=' - ', expand=True)
crash_data.mannerofcrash = crash_data.mannerofcrash.astype('Int64')

crash_data[['typeofperson','typeofpersondescr']] = crash_data.typeofperson.str.split(pat=' - ', expand=True)

crash_data['lightconditions'] = crash_data.lightconditionsprimary.str[0]
crash_data.lightconditions = crash_data.lightconditions.astype('Int64')
crash_data['lightconditionsdescr'] = crash_data.lightconditionsprimary.str[4:]
crash_data.drop(columns='lightconditionsprimary', inplace=True)

crash_data['roadconditions'] = crash_data.roadconditionsprimary.str[0:2]
crash_data.roadconditions = crash_data.roadconditions.astype('Int64')
crash_data['roadconditionsdescr'] = crash_data.roadconditionsprimary.str[5:]
crash_data.drop(columns='roadconditionsprimary', inplace=True)

crash_data[['roadsurface', 'roadsurfacedescr']] = crash_data.roadsurface.str.split(pat=' - ', expand=True)
crash_data.roadsurface = crash_data.roadsurface.astype('Int64')

# Remove the score 
crash_data.crashlocation = crash_data.crashlocation.str.replace(r'\d\d - ', '')

crash_data['gender'] = crash_data.gender.str.replace('F - ', '')
crash_data['gender'] = crash_data.gender.str.replace('M - ', '')
crash_data['gender'] = crash_data.gender.str.replace('U - ', '')
crash_data.gender.unique()

crash_data[['injuries', 'injuriesdescr']] = crash_data.injuries.str.split(pat=' - ', expand=True)
crash_data.injuries = crash_data.injuries.astype('Int64')


crash_data.loc[crash_data['injuriesdescr'] == 'NO APPARENTY INJURY', 'injuriesdescr'] = 'NO APPARENT INJURY'    # Fix the typo in `5 - NO APPARENTY INJURY`

crash_data.unittype = crash_data.unittype.str.replace(r'\d\d - ', '')

## Strings to categorical
crash_data.injuriesdescr = crash_data.injuriesdescr.astype('category')

## Cleaning 
# Standardizing street names 
crash_data.address_x = crash_data.address_x.str.replace('AVENUE$|AV$', 'AVE', regex=True)

crash_data.address_x = crash_data.address_x.str.replace('RD.$', 'RD', regex=True)

# Add AVE to streets missing it 
crash_data.loc[crash_data['address_x'].str.contains('W MITCHELL$|GLENWAY$', regex=True, na=False), 'address_x'] = 'W MITCHELL AVE'

crash_data.loc[crash_data['address_x'].str.contains('GLENWAY$', regex=True, na=False), 'address_x'] = 'GLENWAY AVE'

# Add RD to the streets missing it
crash_data.loc[crash_data['address_x'].str.contains('READING$', regex=True, na=False), 'address_x'] = 'READING RD'

## USEFUL ADDITIONS
# Add column STREET 
crash_data['street'] = crash_data.address_x.str.replace('^\d+X+ ', '', regex=True)