from lxml import objectify

def io_xml(fname):
  xml_data = objectify.parse(fname)
  root = xml_data.getroot()
  data = []
  for i in root.getchildren()[5].getchildren()[0].getchildren():
      data.append([j.getchildren()[0].text for j in i.getchildren()])

  return pd.DataFrame(data[2:], columns=data[0])
