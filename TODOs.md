## Docker

- Create a Makefile
- Handle different chip architectures
- Handle volume mounting correctly

## File Structure

- Use global settings or config for filepaths

## Pipeline

- Build so that there is a more standard "pipeline" structure with error handling
- Figure out when we need to copy the dataframe vs when we just need to return slices

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

## General Cleanup

- Run the pipeline fresh with the data folder downloaded from Google Drive
