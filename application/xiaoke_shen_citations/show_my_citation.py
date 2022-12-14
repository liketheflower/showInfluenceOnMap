import collections

import pandas as pd
from utils import get_boundingbox_or_center_of_a_country
from vis_on_map import vis_on_map


def show_citations(df_fn: str):
    df = pd.read_csv(df_fn)
    for c in [
        "country",
        "num_institutions_cite_my_work",
        "num_researchers_cite_my_work",
    ]:
        assert c in df.columns, f"the df does not has {c} col"
    df["latitude_longitude"] = df["country"].apply(
        get_boundingbox_or_center_of_a_country
    )
    country_latitude_longitude = list(df["latitude_longitude"])
    num_researchers_cite_my_work = list(df["num_researchers_cite_my_work"])
    num_institutions_cite_my_work = list(df["num_institutions_cite_my_work"])
    vis_on_map(
        country_latitude_longitude,
        num_researchers_cite_my_work=num_researchers_cite_my_work,
        num_institutions_cite_my_work=num_institutions_cite_my_work,
        save_fn="xiaoke_shen_citation.html",
    )


def clean_up_data(raw_df_fn, cleanup_df_save_fn="cleanup.csv"):
    df = pd.read_csv(raw_df_fn)
    print(df.shape)
    required_cols = ["country", "researcher", "institution"]
    for c in required_cols:
        assert c in df.columns, f"the df does not has {c} col"
    unique_researchers_by_country = collections.defaultdict(set)
    unique_institutions_by_country = collections.defaultdict(set)
    for _, row in df.iterrows():
        country, researcher, institution = [row[c] for c in required_cols]
        unique_researchers_by_country[country].add(researcher)
        unique_institutions_by_country[country].add(institution)
    countries = sorted(unique_researchers_by_country.keys())
    df = pd.DataFrame(
        {
            "country": countries,
            "num_researchers_cite_my_work": [
                len(unique_researchers_by_country[c]) for c in countries
            ],
            "num_institutions_cite_my_work": [
                len(unique_institutions_by_country[c]) for c in countries
            ],
        }
    )
    df.to_csv(cleanup_df_save_fn, index=False)


if __name__ == "__main__":
    raw_df_fn = "./raw_data/xiaoke_shen_paper_citation.csv"
    cleanup_df_save_fn = "xiaoke_shen_citation_cleanup.csv"
    clean_up_data(raw_df_fn, cleanup_df_save_fn=cleanup_df_save_fn)
    show_citations(cleanup_df_save_fn)
