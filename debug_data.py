import data_manager
import pandas as pd

print("Generating mock trades...")
df = data_manager.generate_mock_trades(5)
print("\nCOLUMNS:", df.columns.tolist())
print("\nFIRST ROW:\n", df.iloc[0].to_dict())
print("\nTYPES:\n", df.dtypes)
