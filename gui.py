import streamlit as st
import pandas as pd


def load_dataset_description():
	with open('data\\data_scientist.txt','r', encoding='utf-8') as f:
		info = f.readlines()
		info = '\n'.join(info)
		info = info.split('|----------|')
		info = info[1:]
	return info


def load_labels():
	with open('labels\\data_scientist.txt','r', encoding='utf-8') as f:
		labels = f.readlines()
	return labels



def get_offers_dataframe_description(info):
	urls = []
	titles = []
	companies = []
	locations = []
	basic_info = []
	descriptions = []

	for tmp in info:
	    tmp_information = tmp.split('\n')
	    
	    url = tmp_information[4]
	    title = tmp_information[6]
	    company = tmp_information[8]
	    location = tmp_information[10]
	    
	    basic_info.append([title, company, location, url])
	    urls.append(url)
	    titles.append(title)
	    companies.append(company)
	    locations.append(location)
	    descriptions.append('\n'.join(tmp_information[12:]))
	    

	df_offers = pd.DataFrame(basic_info, columns = ['title','company','location','url'])
	df_offers['title'] = df_offers['title'].str.lower()

	df_offers['description'] = [d[:500] for d in descriptions]
	df_offers['title_company description'] = df_offers.apply(lambda x: x['title'] + '_' + x['company'] + ' ' + x['description'], axis = 1)

	return df_offers['title_company description'].unique()


def get_next_job_offer(df_offers, desc):
	for j, d in enumerate(desc):
	    i = df_offers[df_offers['title_company description'] == d].index[0]
	    if pd.isna(df_offers.iloc[i]['labels']):
	    	return i, d
	return -1

@st.cache(allow_output_mutation=True)
def ini():
	vals = {'r': 0}
	vals['dataframe'] = pd.read_csv('df_offers.csv')
	vals['info'] = load_dataset_description()
	vals['desc'] = get_offers_dataframe_description(vals['info'])
	vals['i'], vals['d'] = get_next_job_offer(vals['dataframe'], vals['desc'])
	return vals



st.title('Label your data')

vals = ini()
df_offers = vals['dataframe']
info = vals['info']
desc = vals['desc']
i, d = vals['i'], vals['d']


submit_button = False
with st.sidebar.form(key='my_form'):
	new_label = st.selectbox('Would you apply for this job?', ('no','yes'), index = 0)
	submit_button = st.form_submit_button(label='Submit')
	if submit_button:
		df_offers.loc[df_offers['title_company description'] == d, 'labels'] = 0 if new_label=='no' else 1
		vals['i'], vals['d'] = get_next_job_offer(df_offers, desc)
		vals['r'] += 1

info = vals['info']
desc = vals['desc']
i, d = vals['i'], vals['d']

st.write(info[i])
st.write(new_label, vals['r'], vals['i'])

save_button = False
save_button = st.button('Save')
if save_button:
	'saved!'
	df_offers.to_csv('df_offers.csv', index = False)
else:
	'not saved!'