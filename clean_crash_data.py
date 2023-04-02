# Script to clean crash data
import pandas as pd 

raw = pd.read_csv("Traffic_Crash_Reports__CPD_.csv")

data = raw 

## Convert data types
# Strings to dates
data.loc[:, 'CRASHDATE'] = pd.to_datetime(data.CRASHDATE)
data.loc[:, 'DATECRASHREPORTED'] = pd.to_datetime(data.DATECRASHREPORTED)

# Numbers to strings
data.loc[:, 'LOCALREPORTNO'] = data.LOCALREPORTNO.apply(str )
data.loc[:, 'CRASHSEVERITYID'] = data.CRASHSEVERITYID.apply(str)

# Stripping the trailing zeros from ZIP 
data.loc[:,'ZIP'] = data.ZIP.astype(str)
data.loc[:,'ZIP'] = data.ZIP.str[:5]

## Splitting fields - Separate scores from descriptions
data[['CRASHSEVERITY','CRASHSEVERITYDESCR']] = data.CRASHSEVERITY.str.split(pat=' - ', expand=True)
data.CRASHSEVERITY = data.CRASHSEVERITY.astype('Int64')

data[['ROADCONTOUR','ROADCONTOURDESCR']] = data.ROADCONTOUR.str.split(pat=' - ', expand=True)
data.ROADCONTOUR = data.ROADCONTOUR.astype('Int64')

data[['MANNEROFCRASH', 'MANNEROFCRASHDESCR']] = data.MANNEROFCRASH.str.split(pat=' - ', expand=True)
data.MANNEROFCRASH = data.MANNEROFCRASH.astype('Int64')

data[['TYPEOFPERSON','TYPEOFPERSONDESCR']] = data.TYPEOFPERSON.str.split(pat=' - ', expand=True)

data['LIGHTCONDITIONS'] = data.LIGHTCONDITIONSPRIMARY.str[0]
data.LIGHTCONDITIONS = data.LIGHTCONDITIONS.astype('Int64')
data['LIGHTCONDITIONSDESCR'] = data.LIGHTCONDITIONSPRIMARY.str[4:]
data.drop(columns='LIGHTCONDITIONSPRIMARY', inplace=True)

data['ROADCONDITIONS'] = data.ROADCONDITIONSPRIMARY.str[0:2]
data.ROADCONDITIONS = data.ROADCONDITIONS.astype('Int64')
data['ROADCONDITIONSDESCR'] = data.ROADCONDITIONSPRIMARY.str[5:]
data.drop(columns='ROADCONDITIONSPRIMARY', inplace=True)

data[['ROADSURFACE', 'ROADSURFACEDESCR']] = data.ROADSURFACE.str.split(pat=' - ', expand=True)
data.ROADSURFACE = data.ROADSURFACE.astype('Int64')

# Remove the score 
data.CRASHLOCATION = data.CRASHLOCATION.str.replace(r'\d\d - ', '')

data['GENDER'] = data.GENDER.str.replace('F - ', '')
data['GENDER'] = data.GENDER.str.replace('M - ', '')
data['GENDER'] = data.GENDER.str.replace('U - ', '')
data.GENDER.unique()

data[['INJURIES', 'INJURIESDESCR']] = data.INJURIES.str.split(pat=' - ', expand=True)
data.INJURIES = data.INJURIES.astype('Int64')


data.loc[data['INJURIESDESCR'] == 'NO APPARENTY INJURY', 'INJURIESDESCR'] = 'NO APPARENT INJURY'    # Fix the typo in `5 - NO APPARENTY INJURY`

data.UNITTYPE = data.UNITTYPE.str.replace(r'\d\d - ', '')