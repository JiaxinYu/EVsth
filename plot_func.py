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


def cal_ma(seq):
  wsize = 3

  n_series = pd.Series(seq)
  windows = n_series.rolling(wsize)
  ma = windows.mean()

  ma_list = ma.tolist()
  return ma_list[wsize - 1:]


def plot_index(df, date, idxname, cmap='b'):
  # plot with 3 shifts
  fig, axes = plt.subplots(3, 1, figsize=(28, 12), dpi=300)
  swt = getshiftwork(df, date)
  axes[0].set_title(date+'_'+idxname, fontsize=20)
  
  if idxname == 'BP':
    for i in range(3):
      # im = axes[i].plot(df['SBP'][swt[i]:swt[i+1]].astype('float').to_numpy(), color='b')
      # im = axes[i].plot(df['DBP'][swt[i]:swt[i+1]].astype('float').to_numpy(), color='g')
      im = axes[i].plot(cal_ma(df['SBP'][swt[i]:swt[i+1]].astype('float')), color='b')
      im = axes[i].plot(cal_ma(df['DBP'][swt[i]:swt[i+1]].astype('float')), color='g')
      plt.sca(axes[i])
      plt.xticks(fontsize=14)
      plt.xticks(np.array(range(0, 180*8, 180)), np.array(range(i*8, (i+1)*8)))
  else:
    for i in range(3):
      # im = axes[i].plot(df[idxname][swt[i]:swt[i+1]].astype('float').to_numpy(), color=cmap)
      im = axes[i].plot(cal_ma(df[idxname][swt[i]:swt[i+1]].astype('float')), color=cmap)
      plt.sca(axes[i])
      plt.xticks(fontsize=14)
      plt.xticks(np.array(range(0, 180*8, 180)), np.array(range(i*8, (i+1)*8)))

  plt.savefig(rootpath/'{}_{}.png'.format(idxname, date), dpi=300)


def plot_index(df, date, idxname, cmap='b'):
  # plot with 3 shifts
  fig, axes = plt.subplots(3, 1, figsize=(28, 12), dpi=300)
  swt = getshiftwork(df, date)
  axes[0].set_title(date+'_'+idxname, fontsize=20)
  
  if idxname == 'BP':
    for i in range(3):
      im = axes[i].plot(df['SBP'][swt[i]:swt[i+1]].astype('int').to_numpy(), color='r')
      im = axes[i].plot(df['DBP'][swt[i]:swt[i+1]].astype('int').to_numpy(), color='b')
      plt.sca(axes[i])
      plt.xticks(fontsize=14)
      plt.xticks(np.array(range(0, 180*8, 180)), np.array(range(i*8, (i+1)*8)))
  else:
    for i in range(3):
      im = axes[i].plot(df[idxname][swt[i]:swt[i+1]].astype('int').to_numpy(), color=cmap)
      plt.sca(axes[i])
      plt.xticks(fontsize=14)
      plt.xticks(np.array(range(0, 180*8, 180)), np.array(range(i*8, (i+1)*8)))

  plt.savefig(rootpath/'{}_{}.png'.format(idxname, date), dpi=300)

  
def plot_EventIndex(eventname, df, date, tpoint, idxname, cmap='b'):
  # get event time point
  temp = df[df['date'].str.contains(date, na=False)]
  t0 = temp[temp['time'].str.contains(tpoint, na=False)].index[0]
  dt = np.array(range(-90, 45*7, 45))
  
  fig, axes = plt.subplots(figsize=(28, 4), dpi=300)
  axes.set_title(eventname, fontsize=20)
  axes.plot(df[idxname].iloc[(t0-90):(t0+270)].astype('int').to_numpy(), label=idxname, color=cmap)
  plt.xticks(fontsize=14)
  plt.xticks(np.array(range(0, 360, 45)), [df['time'][dt[i]+t0][:5] for i in range(9)])
  plt.legend(loc='upper right', prop={'size': 24})
  plt.savefig(rootpath/'{}_{}_{}.png'.format(eventname, idxname, date), dpi=300)
