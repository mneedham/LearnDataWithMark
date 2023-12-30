locations = [...]
date_range = create_date_range("20220101", "20231130")
pairs = itertools.product(locations, date_range)
lazy_results = []
for location, date in pairs:
    result = dask.delayed(process_pair)(location, date, file)
    lazy_results.append(result)

futures = dask.persist(*lazy_results) 
