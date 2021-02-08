def pulse_pressure(SBP, DBP):
  return (SBP - DBP)


def pattern_recon(df):
  ## 1. CO down: CO, dPdt, PP down; HPI up
  ## 2. CO up: CO, dPdt, PP up; HPI down
  ## 3. vasoconstriction: SVR, Eadyn up; HPI down

  event_type = []
  if HPI[i] > HPI_ma[i]:
    if all(CO[i] > CO_ma[i], dPdt[i] > dPdt_ma[i], PP[i] > PP_ma[i]):
      event_type.append(1)
    else:
      event_type.append(0)
  elif HPI[i] < HPI_ma[i]:
    if all(CO[i] < CO_ma[i], dPdt[i] < dPdt_ma[i], PP[i] < PP_ma[i]):
      event_type.append(2)
    elif all(SVR[i] > SVR_ma[i], Eadyn[i] > Eadyn_ma[i]):
      vent_type.append(3)
    else:
      event_type.append(0)
  return event_type
