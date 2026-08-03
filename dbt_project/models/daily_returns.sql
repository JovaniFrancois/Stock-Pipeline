select
    date,
    ticker,
    close,
    (close - lag(close) over (partition by ticker order by date)) / lag(close) over (partition by ticker order by date) as daily_return
from {{ source('raw', 'raw_prices') }}