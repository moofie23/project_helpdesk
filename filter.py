import pandas as pd
df = pd.DataFrame({
    'date': pd.to_datetime(['2023-01-11', '2023-01-15', '2023-02-01']),
    'status': ['open', 'close', 'open']
})
date_filter_start = pd.to_datetime('2023-01-10')
date_filter_end = pd.to_datetime('2023-01-31')
status_request = 'open'
filtered_df = 0
if date_filter_start and date_filter_end and status_request is not None:
  filtered_df = df.query("date >= @date_filter_start and date <= @date_filter_end and status == @status_request")
elif date_filter_start and date_filter_end is not None:
 filtered_df = df.query("date >= @date_filter_start and date <= @date_filter_end")
elif status_request is not None:
  filtered_df = df.query("status == @status_request")
print(filtered_df)