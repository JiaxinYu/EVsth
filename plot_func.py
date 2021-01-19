def getdata(fname):
  df = pd.read_csv(fname, encoding='big5')
  # get indexs
  df1 = pd.concat([df[df.columns[0]], df[df.columns[1]], df['PR'], df['SYSART'], df['DIAART'], df['SVR'], df['CO'], df['dP/dt'], df['Eadyn'], df['HPI']], 1)
  # clean dataframe
  # df1.dropna(how='all', inplace=True)
  df1.fillna(value=0, inplace=True)
  df1.reset_index(drop=True, inplace=True)
  df1.columns = ['date', 'time', 'HR', 'SBP', 'DBP', 'SVR', 'CO', 'dPdt', 'Eadyn', 'HPI']
  return df1


def getshiftwork(df, date):
  # work shift in 3 different time slots
  temp = df[df['date'].str.contains(date, na=False)]
  t0 = temp[temp['time'].str.contains('00:00', na=False)].index[0]
  t1 = temp[temp['time'].str.contains('08:00', na=False)].index[0]
  t2 = temp[temp['time'].str.contains('16:00', na=False)].index[0]
  t3 = temp[temp['time'].str.contains('23:59', na=False)].index[2]
  return [t0, t1, t2, t3]


def plot_alltime(df):
  # plot 3 days
  fig, axes = plt.subplots(3, 1, figsize=(28, 12), dpi=300)
  axes[0].set_title('HPI', fontsize=20)
  axes[1].set_title('Eadyn', fontsize=20)
  axes[2].set_title('CO', fontsize=20)

  time0 = df['time'][0] + '  ' + df['date'][0]
  timet = df['time'][len(df)-1] + '  ' + df['date'][len(df)-1]

  im = axes[0].plot(df['HPI'].astype('int').to_numpy(), label='HPI', color='b')
  plt.sca(axes[0])
  plt.xticks(fontsize=16)
  plt.xticks([0, len(df1)], [time0, timet])
  
  im = axes[1].plot(df['Eadyn'].astype('float').to_numpy(), label='Eadyn', color='r', alpha=0.6)
  im = axes[1].plot(np.ones(len(df)) - 0.1, color='r', linestyle='--', lw=3)
  
  im = axes[2].plot(df['CO'].astype('float').to_numpy(), label='CO', color='g')
  plt.show()


def plot_index(df, date, idxname, cmap):
  # plot with 3 shifts
  fig, axes = plt.subplots(3, 1, figsize=(28, 12), dpi=300)
  swt = getshiftwork(df, date)
  axes[0].set_title(date+'_'+idxname, fontsize=20)
  # set x-axis
  for i in range(3):
    im = axes[i].plot(df[idxname][swt[i]:swt[i+1]].astype('int').to_numpy(), color=cmap)
    plt.sca(axes[i])
    plt.xticks(fontsize=14)
    plt.xticks(np.array(range(0, 180*8, 180)), np.array(range(i*8, (i+1)*8)))

  plt.savefig(rootpath/'{}_{}.png'.format(idxname, date), dpi=300)
