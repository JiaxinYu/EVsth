# readin
df = pd.read_csv('path/to/file')

# get indexs
df1 = pd.concat([df['__'], df['__.1'], df['CO'], df['dP/dt'], df['Eadyn'], df['HPI']], 1)

# clean dataframe
df1.dropna(inplace=True)
df1.reset_index(drop=True, inplace=True)
df1.columns = ['date', 'time', 'CO', 'dP/dt', 'Eadyn', 'HPI']

# visualization
fig, axes = plt.subplots(3, 1, figsize=(28, 12), dpi=600)
axes[0].set_title('HPI', fontsize=20)
axes[1].set_title('Eadyn', fontsize=20)
axes[2].set_title('CO', fontsize=20)
im = axes[0].plot(df1['HPI'].iloc[::3].astype('int').to_numpy(), label='HPI', color='b')
im = axes[1].plot(df1['Eadyn'].iloc[::3].astype('float').to_numpy(), label='Eadyn', color='r')
im = axes[2].plot(df1['CO'].iloc[::3].astype('float').to_numpy(), label='CO', color='g')
plt.show()
