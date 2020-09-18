import pandas as pd
import urllib
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def handler(event,context):
    
    # original_xl = urllib.request.urlopen(json.loads(event['body'])['url'])
    # df = pd.read_excel(original_xl, sheetname=None, header=3)
    
    result = {'worksheets': []}

    # Columns to retain/rename from IO export
    colsToRetain = ['Order', #convert to 'Internal Order'
                    'Val_in_rep_cur_', #convert to 'Settlement Amount'
                    'classification_names', #convert to 'Asset Class'
                    'Purchase_order_text', #convert to 'Asset description'
                    'CoCd', #convert to "Company Code"
                    'Site',
                    'Transaction_Grouping',
                    'Serial_number',
                    'Depreciation_Key___Area_01',
                    'Planned_useful_life_in_years_Book_01'
                   ]

    # Retain above and delete the rest
    df.drop(df.columns.difference(colsToRetain), 1, inplace=True)

    # Rename columns for ERP
    df.rename(columns={'Order':'Internal Order',
                       'Val_in_rep_cur_':'Settlement Amount',
                       'classification_names':'Asset Class',
                       'Purchase_order_text':'Asset description',
                       'CoCd':'Company Code',
                       'Transaction_Grouping':'Transaction Grouping',
                       'Serial_number':'Serial number',
                       'Depreciation_Key___Area_01':'Depreciation Key - Area 01',
                       'Planned_useful_life_in_years_Book_01':'Planned useful life in years Book 01'
                      },inplace=True)

    # Columns to add
    colsToAdd = ['Asset Main No.',
                'Asset Sub No.',
                'Main Asset No',
                'Create Sub Asset',
                'Inventory Number',
                #'Internal Order',
                #'Serial number',
                'Asset is Managed Historically',
                'Additional asset description',
                'Asset capitalisation date',
                'Cost Centre',
                #'Internal Order',
                'Number of Similar Assets',
                'Ev. 1',
                'Ev. 2',
                'Ev. 3',
                'Ev. 4',
                'Ev. 5',
                'Investment Order',
                'Vendor',
                'Supplier Name',
                'Manufacturer of asset',
                'License plate number',
                'Original asset that was transferred',
                'Original (Sub) asset that was transferred',
                'Inventory No.',
                'Original asset that was transferred',
                'Original (Sub) asset that was transferred',
                'Deactivate Dep Area 01',
                #'Depreciation Key - Area 01',
                #'Planned useful life in years Book 01',
                'Planned useful life in periods Book 01',
                'Deactivate Dep Area 15',
                'Depreciation Key - Area 15',
                'Planned useful life in years Book 15',
                'Planned useful life in periods Book 15',
                'Deactivate Dep Area 30',
                'Depreciation Key - Area 30',
                'Planned useful life in years Book 30',
                'Planned useful life in periods Book 30',
                ]


    # Add new columns
    df[colsToAdd] = pd.DataFrame([len(colsToAdd)*['']], index=df.index)

    # Update columns
    df['Number of Similar Assets']=1
    df['Cost Centre'] = df['Site']
    df['Asset is Managed Historically']='X'
    #df.insert(0,'Transaction Grouping',df.index)
    
    # Rearrange Columns
    cols = ['Transaction Grouping','Internal Order','Asset Main No.','Asset Sub No.','Settlement Amount','Main Asset No','Create Sub Asset','Asset Class','Company Code','Number of Similar Assets','Asset description','Additional asset description','Serial number','Inventory Number','Asset is Managed Historically','Asset capitalisation date','Cost Centre','Internal Order','Site','Ev. 1','Ev. 2','Ev. 3','Ev. 4','Ev. 5','Investment Order','Vendor','Supplier Name','Manufacturer of asset','License plate number','Original asset that was transferred','Original (Sub) asset that was transferred','Inventory No.','Original asset that was transferred','Original (Sub) asset that was transferred','Deactivate Dep Area 01','Depreciation Key - Area 01','Planned useful life in years Book 01','Planned useful life in periods Book 01','Deactivate Dep Area 15','Depreciation Key - Area 15','Planned useful life in years Book 15','Planned useful life in periods Book 15','Deactivate Dep Area 30','Depreciation Key - Area 30','Planned useful life in years Book 30','Planned useful life in periods Book 30']
    df = df[cols]

    # Clear NAs
    df = df.fillna(value='')

    # Prep output
    df_dict = df.to_dict('split')
    result['worksheets'].append({'name': 'seven_eleven_SAP', 'data': [df_dict['columns']] + df_dict['data']})

    return {
        'statusCode': 200,
        'body': json.dumps(result) if result else json.dumps({}),
        'headers': {
            'Content-Type': 'application/json',
        },
    }