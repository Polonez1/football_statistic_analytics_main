from scripts import MainData


data = MainData.GeneralData(seasons=[2020, 2021, 2022])
df = data.fixture_data()
print(df)
