## Docker

- Create a Makefile
- Handle different chip architectures
- Handle volume mounting correctly
  `docker run -v $(pwd)/notebooks:/app/notebooks -v $(pwd)/data:/app/data -p 8888:8888 -t ukraine`

## File Structure

- Use global settings or config for filepaths

## Pipeline

- Build so that there is a more standard "pipeline" structure with error handling
- Figure out when we need to copy the dataframe vs when we just need to return slices
- Use standard python logger to keep track of where you are

## Pipeline Pseudocode

```from settings import FILPATHS

# could honestly even do this as an ABC if we really wanted to...

def pipeline_ig(country, write=True, **kwargs):
    try:
        ig_read_path = FILEPATHS['ig'][country][['read']]
    except Exception as e:
        raise Exception("You did it wrong, dummy")
    try:
        df_ig = pd.read_csv(ig_path)
    except:
        raise Exception("You did it wrong, dummy")
    try:
        df_ig = clean_commodities(df_ig)
    except:
        raise Exception("You did it wrong, dummy")
    try:
        df_ig = handle_companies(df_ig)
    except:
        raise Exception("You did it wrong, dummy")
    try:
        ig_write_path = FILEPATHS['ig][country]['write]
    except:
        raise Exception("You did it wrong, dummy")

    return df_ig
```

Ok, after going through this in a bit more detail, I do think that creating an ABC is probably the best way to do this since we have some pretty consistent actions that we are taking for all data sources, then we are doing some idiosyncratic things for them based upon which datasource we have.

If we really start pulling this apart, it would be good to have some tests that we can run as well.

## Overall flow

Here's how I think this should be set up — it's kind of like this already, but I think it would be good to more explicitly create each of these parts.

1. Pipeline: read and clean data from each data source » returns cleaned dataframes for each data source
2. Merging and filtering: match and merge dataframes from different sources with options to filter on date, commodity, etc. » returns a dataframe ready for analysis
3. Plotting and analysis: take the cleaned, merged and filtered data and display plots and/or tables

## General Cleanup

- Run the pipeline fresh with the data folder downloaded from Google Drive
