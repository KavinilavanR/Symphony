import os
import openai
import pandas as pd
from pyathena import connect
import sys,json

question = query = sys.argv[1]
conn = connect(s3_staging_dir='',
               region_name='',
               aws_access_key_id='',
               aws_secret_access_key='')
openai.api_key = ''

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=f"Hi GPT! I need your help in generating an ANSI/Presto SQL query. I am going to give you the schema associated with an AWS Athena database. After this, I will give you some example inputs and ouputs and I expect you to give me ANSI SQL queries that will generate answers to any additional queries on top of the database whose schema I will have described at the start. \n\nNote: for some queries, I expect you to create intermediate tables or nested (in-memory queries) to answer. You are encouraged to use CTEs to ensure readability in your generated queries. Name of the table is \"rx_claims_master_data_revamp\". Schema Description:\\n \n\nField Name | Field Type | Data Definition \nNPI | varchar | 10 digit HCP identifier\nPhysician_Availability_Flag | varchar(21) | Physician present in latest data\nClaim_ID | varchar | Unique claim identifier \nPatient_ID | varchar | Unique patient identifier \nPatient_Gender | varchar(8) | Patient Gender\nPatient_State | varchar | State in which prescription was filled\nRegion | varchar(9) | Region info of state\nDivision | varchar(18) | Division info of region\nSource | varchar | Source of data (Rx or Px)\nplan_type_description | varchar | Payor type (COMMERCIAL, MEDICARE, MEDICAID, etc.) in capital letters\nPlan_Name | varchar | Specific payor name\nDrug_name | varchar | Brand or Drug name\nBrand_Name | varchar | Specific Manufacturer or Company Name\nPrescribed_Drug_Indication | varchar(2922) | Drug indication (based on prescribed drug)\nDrug_Flag | varchar(12) | Focused or other drugs\nPrescription_Fill_Year_Month | date | Date when prescription was filled\nquantity | double | total quantity of drugs prescribed in each prescription\nTotal_Patient_Responsibility | double | Out of Pocket expense borne by patient\nTotal_Payer_Responsibility | double | Expense borne by payor\npatient_age | integer | numeric age of patient in years\nindication | string | indication\nUnknown_Flag | varchar(3) | If no disease detected, this would be Yes\n\nA few definitions, are important to know - \nMarket share of a drug = Drug claims volume *100 / Overall market claims for the selected indication\nGrowth = Current time period claims volume / Previous time period claims volume - 1\n\nLearn from my examples, and build the steps needed to solve any questions been asked to you based on this information and your intelligence, and use your chain of thought to create an ANSI SQL query to answer my question.\n\n\nWhat is Velcade's market share in last 3 months?\n\nwith num as\n(select count(distinct(Claim_ID)) as num_data from \"symphony-data\".\"rx_claim_master_data_revamp\" where Drug_Name like '%VELCADE%' and Prescription_Fill_Year_Month >= (select max(Prescription_Fill_Year_Month)\nfrom \"symphony-data\".\"rx_claim_master_data_revamp\") - interval '90' day\n),\nden as\n(\nselect count(distinct(Claim_ID)) as den_data from \"symphony-data\".\"rx_claim_master_data_revamp\" where indication in (SELECT distinct(indication) FROM \"symphony-data\".\"rx_claim_master_data_revamp\" where Drug_Name like '%VELCADE%'\n)and Prescription_Fill_Year_Month >= (select max(Prescription_Fill_Year_Month)\nfrom \"symphony-data\".\"rx_claim_master_data_revamp\") - interval '90' day\n)\nselect ROUND(100.0 * num_data / den_data, 2) as market_share from num,den;\n\nWhat is the growth of Velcade in the last 3 months compared to the previous year?\n\nWITH\nnumerator AS (\n    select count(Distinct(claim_ID)) as total_claims from  \"symphony-data\".\"rx_claim_master_data_revamp\" where Prescription_Fill_Year_Month >= (select max(Prescription_Fill_Year_Month)\nfrom  \"symphony-data\".\"rx_claim_master_data_revamp\") - interval '90' day and Drug_Name like '%VELCADE%'\n),\ndenominator AS(\n    select count(distinct(claim_ID)) as total_claims from  \"symphony-data\".\"rx_claim_master_data_revamp\" where Prescription_Fill_Year_Month >= (select max(Prescription_Fill_Year_Month)\nfrom  \"symphony-data\".\"rx_claim_master_data_revamp\") - interval '1' year - interval '3' month and Prescription_Fill_Year_Month <= (select max(Prescription_Fill_Year_Month)\nfrom  \"symphony-data\".\"rx_claim_master_data_revamp\") - interval '1' year and Drug_Name like '%GLAXOSMITHKLINE%'\n)\nSELECT (cast(numerator.total_claims as double) / (denominator.total_claims - 1))*100 as share from numerator, denominator;\n{question}\n",
  temperature=0,
  max_tokens=512,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
query = str(response['choices'][0]['text'])
# print( "Query generated : \n" + str(response['choices'][0]['text']))

cursor = conn.cursor()


cursor.execute(str(response['choices'][0]['text']))
rows = cursor.fetchall()

df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])


# print("Result table : ")
# print(df)

cursor.close()
conn.close()

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=f"summarize the following question and answer\nquestion:{question}\nanswer:\n{str(df)} even if the answer count is 0 ",
  temperature=0,
  max_tokens=60,
  top_p=1,
  frequency_penalty=0.5,
  presence_penalty=0
)
print(json.dumps({"query" : query,"result_table" : str(df),"answer" : str(response['choices'][0].text)}))