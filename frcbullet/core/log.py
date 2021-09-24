import asyncio
import pandas as pd
import numpy


class Log:

    def __init__(self, *log_headers):
        self.currentData = dict(zip(log_headers, [0 for i in range(len(log_headers))]))
        self.data = pd.DataFrame(columns=log_headers)

    async def schedule(self):
        await self.write_to_dataframe()

    def update_value(self, log_header, value):
        self.currentData[log_header] = value

    async def write_to_dataframe(self):
        while True:
            # dfappend = pd.DataFrame(self.currentData)
            self.data.loc[len(self.data.index)] = self.currentData.values()
            await asyncio.sleep(0.01)
