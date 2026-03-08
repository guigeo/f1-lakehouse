# %%
import pandas as pd
pd.set_option('display.max_columns', None)

import fastf1
import time
import argparse
import os

# %%

class CollectResults:

    def __init__(self, years=[2021,2022,2023], modes=["R", "S"]):
        self.years = years
        self.modes = modes

        os.makedirs("data", exist_ok=True)
        
    def get_data(self, year, gp, mode)->pd.DataFrame:
        try:
            session = fastf1.get_session(year, gp, mode)
        except ValueError:
            return pd.DataFrame()
        
        session._load_drivers_results()
        df = session.results.copy()

        df["Year"] = session.date.year
        df["Date"] = session.date
        df["Mode"] = session.name
        df["RoundNumber"] = session.event["RoundNumber"]
        df["OfficialEventName"] = session.event["OfficialEventName"]
        df["EventName"] = session.event["EventName"]
        df["Country"] = session.event["Country"]
        df["Location"] = session.event["Location"]

        # ---------
        # Corrigir timestamps para Spark
        # ---------
        for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
            df[col] = df[col].astype("datetime64[us]")

        return df
    

    def save_data(self, df:pd.DataFrame, year:int, gp:int, mode:str):
        filename = f"data/{year}_{gp:02}_{mode}.parquet"

        df.to_parquet(
            filename,
            index=False,
            engine="pyarrow",
            coerce_timestamps="us"
        )


    def process(self, year, gp, mode):
        df = self.get_data(year, gp, mode)
        
        if df.empty:
            return False
        
        self.save_data(df, year, gp, mode)
        time.sleep(5)
        return True


    def process_year_modes(self, year):
        for i in range(1,50):
            for mode in self.modes:
                if not self.process(year, i, mode) and mode == "R":
                    return


    def process_years(self):
        for year in self.years:
            print(f"Coletando dados do ano {year}")
            self.process_year_modes(year)
            time.sleep(10)


# %%

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Coleta os resultados das corridas de F1 usando a biblioteca fastf1")
    parser.add_argument("--start",type=int)
    parser.add_argument("--stop",type=int)
    parser.add_argument("--years", "-y", nargs="+", type=int)
    parser.add_argument("--modes", "-m", nargs="+")

    args = parser.parse_args()

    if args.years:
        collect = CollectResults(args.years, args.modes)
    
    elif args.start and args.stop:
        years = [i for i in range(args.start, args.stop+1)]
        collect = CollectResults(years, args.modes)

    collect.process_years()