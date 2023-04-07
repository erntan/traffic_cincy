# Script to clean crash data
import pandas as pd 

crash_raw = pd.read_csv("Traffic_Crash_Reports__CPD_.csv", dtype={'CRASHLOCATION':'string', 'ZIP':'string'})

crash_data = crash_raw 

## Convert data types
# Strings to dates
crash_data.loc[:, 'CRASHDATE'] = pd.to_datetime(crash_data.CRASHDATE)
crash_data.loc[:, 'DATECRASHREPORTED'] = pd.to_datetime(crash_data.DATECRASHREPORTED)

# Numbers to strings
crash_data.loc[:, 'LOCALREPORTNO'] = crash_data.LOCALREPORTNO.apply(str )
crash_data.loc[:, 'CRASHSEVERITYID'] = crash_data.CRASHSEVERITYID.apply(str)

# Stripping the trailing zeros from ZIP 
crash_data.loc[:,'ZIP'] = crash_data.ZIP.astype(str)
crash_data.loc[:,'ZIP'] = crash_data.ZIP.str[:5]

## Splitting fields - Separate scores from descriptions
crash_data[['CRASHSEVERITY','CRASHSEVERITYDESCR']] = crash_data.CRASHSEVERITY.str.split(pat=' - ', expand=True)
crash_data.CRASHSEVERITY = crash_data.CRASHSEVERITY.astype('Int64')

crash_data[['ROADCONTOUR','ROADCONTOURDESCR']] = crash_data.ROADCONTOUR.str.split(pat=' - ', expand=True)
crash_data.ROADCONTOUR = crash_data.ROADCONTOUR.astype('Int64')

crash_data[['MANNEROFCRASH', 'MANNEROFCRASHDESCR']] = crash_data.MANNEROFCRASH.str.split(pat=' - ', expand=True)
crash_data.MANNEROFCRASH = crash_data.MANNEROFCRASH.astype('Int64')

crash_data[['TYPEOFPERSON','TYPEOFPERSONDESCR']] = crash_data.TYPEOFPERSON.str.split(pat=' - ', expand=True)

crash_data['LIGHTCONDITIONS'] = crash_data.LIGHTCONDITIONSPRIMARY.str[0]
crash_data.LIGHTCONDITIONS = crash_data.LIGHTCONDITIONS.astype('Int64')
crash_data['LIGHTCONDITIONSDESCR'] = crash_data.LIGHTCONDITIONSPRIMARY.str[4:]
crash_data.drop(columns='LIGHTCONDITIONSPRIMARY', inplace=True)

crash_data['ROADCONDITIONS'] = crash_data.ROADCONDITIONSPRIMARY.str[0:2]
crash_data.ROADCONDITIONS = crash_data.ROADCONDITIONS.astype('Int64')
crash_data['ROADCONDITIONSDESCR'] = crash_data.ROADCONDITIONSPRIMARY.str[5:]
crash_data.drop(columns='ROADCONDITIONSPRIMARY', inplace=True)

crash_data[['ROADSURFACE', 'ROADSURFACEDESCR']] = crash_data.ROADSURFACE.str.split(pat=' - ', expand=True)
crash_data.ROADSURFACE = crash_data.ROADSURFACE.astype('Int64')

# Remove the score 
crash_data.CRASHLOCATION = crash_data.CRASHLOCATION.str.replace(r'\d\d - ', '')

crash_data['GENDER'] = crash_data.GENDER.str.replace('F - ', '')
crash_data['GENDER'] = crash_data.GENDER.str.replace('M - ', '')
crash_data['GENDER'] = crash_data.GENDER.str.replace('U - ', '')
crash_data.GENDER.unique()

crash_data[['INJURIES', 'INJURIESDESCR']] = crash_data.INJURIES.str.split(pat=' - ', expand=True)
crash_data.INJURIES = crash_data.INJURIES.astype('Int64')


crash_data.loc[crash_data['INJURIESDESCR'] == 'NO APPARENTY INJURY', 'INJURIESDESCR'] = 'NO APPARENT INJURY'    # Fix the typo in `5 - NO APPARENTY INJURY`

crash_data.UNITTYPE = crash_data.UNITTYPE.str.replace(r'\d\d - ', '')

## Cleaning 
# Standardizing street names 
crash_data.ADDRESS_X = crash_data.ADDRESS_X.str.replace('AVENUE$|AV$', 'AVE', regex=True)

crash_data.ADDRESS_X = crash_data.ADDRESS_X.str.replace('RD.$', 'RD', regex=True)

# Add AVE to streets missing it 
crash_data.loc[crash_data['ADDRESS_X'].str.contains('W MITCHELL$|GLENWAY$', regex=True, na=False), 'ADDRESS_X'] = 'W MITCHELL AVE'

crash_data.loc[crash_data['ADDRESS_X'].str.contains('GLENWAY$', regex=True, na=False), 'ADDRESS_X'] = 'GLENWAY AVE'

# Add RD to the streets missing it
crash_data.loc[crash_data['ADDRESS_X'].str.contains('READING$', regex=True, na=False), 'ADDRESS_X'] = 'READING RD'

## USEFUL ADDITIONS
# Add column STREET 
crash_data['STREET'] = crash_data.ADDRESS_X.str.replace('^\d+X+ ', '', regex=True)