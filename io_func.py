def io_xml(fname):
  xml_data = objectify.parse(fname)
  root = xml_data.getroot()
  data = []
  for i in root.getchildren()[5].getchildren()[0].getchildren():
      data.append([j.getchildren()[0].text for j in i.getchildren()])

  df = pd.DataFrame(data[2:], columns=data[0])
  df = df.loc[:,~df.columns.duplicated()]
  # get indexs
  df1 = pd.concat([df[df.columns[0]], df[df.columns[1]], df['PR'], df['SYS'], df['DIA'], df['SVR'], df['CO'], df['dP/dt'], df['Ea'], df['HPI']], 1)
  # clean dataframe
  df1.fillna(value=0, inplace=True)
  df1.reset_index(drop=True, inplace=True)
  df1.columns = ['date', 'time', 'HR', 'SBP', 'DBP', 'SVR', 'CO', 'dPdt', 'Eadyn', 'HPI']
  return df1
