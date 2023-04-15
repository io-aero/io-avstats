# IO-AVSTATS - File Directory **`data/Countries_States`**

This file directory contains the necessary files for the processing step:

- `l_c_s` - Load country and state data into PostgreSQL

The following parameter in the file **`settings.io_avstats.toml`** is used to locate the file: 

- `download_file_countries_states_json` = "data/Countries_States/countries_states.json"

The data source can be found on the FAA website here:

- [geodatos](https://www.geodatos.net/en/countries/united-states)
- [opendatasoft: US State Boundaries](https://data.opendatasoft.com/explore/?q=us+states&sort=%23relevance&disjunctive.language&disjunctive.source_domain_title&disjunctive.theme&disjunctive.semantic.classes&disjunctive.semantic.properties)

The data found in  **geodatos** and **opendatasoft** was manually transferred to a JSON file.

```
      [
        {
          "type": "country",
          "country": "USA",
          "country_name": "United States",
          "dec_latitude": 37.09024,
          "dec_longitude": -95.712891
        },
        {
          "type": "state",
          "country": "USA",
          "state": "AK",
          "state_name": "Alaska",
          "dec_latitude": 63.7431630974,
          "dec_longitude": -151.594035116
        },
        {
          "type": "state",
          "country": "USA",
          "state": "AL",
          "state_name": "Alabama",
          "dec_latitude": 32.7570463396,
          "dec_longitude": -86.844525962
        },
      ...
      ]
```

The current version is dated 

- October 24, 2019.