def pulse_pressure(SBP, DBP):
  return (SBP - DBP)


def get_trend(df, date, idxname, t0, t1):
  if idxname == 'PP':
    var = df['SBP'][t0:t1].astype('float') - df['DBP'][t0:t1].astype('float')
  else:
    var = df[idxname][t0:t1].astype('float')
  
  trend_var = var - cal_ma(var)
  trend_var[trend_var > 0] = 1
  trend_var[trend_var < 0] = -1
  return trend_var


def pattern_recon(df, date, t0, t1):
  df_hpi = pd.DataFrame(get_trend(df, date, 'HPI', t0, t1), columns=['HPI'])
  for i in ['CO', 'dPdt', 'PP', 'SVR', 'Eadyn']:
    df_temp = pd.DataFrame(get_trend(df, date, i, t0, t1), columns=[i])
    df_hpi = df_hpi.join(df_temp)

  event_type = []
  for i in df_hpi.index:
    if df_hpi['HPI'][i] > 0:
      if all([(df_hpi['CO'][i] > 0), (df_hpi['dPdt'][i] > 0), (df_hpi['PP'][i] > 0)]):
        event_type.append(1) # CO reduced: CO, dPdt and PP reduced; HPI increased
      else:
        event_type.append(0)
    elif df_hpi['HPI'][i] < 0:
      if all([(df_hpi['CO'][i] < 0), (df_hpi['dPdt'][i] < 0), (df_hpi['PP'][i] < 0)]):
        event_type.append(2) # CO increased: CO, dPdt and PP increased; HPI reduced
      elif all([(df_hpi['SVR'][i] > 0), (df_hpi['Eadyn'][i] > 0)]):
        event_type.append(3) # vasoconstriction: SVR and Eadyn increased; HPI reduced
    else:
      event_type.append(0) # others
  return event_type
