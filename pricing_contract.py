from datetime import date
import math

def calculate_contract_value(injection_dates, injection_prices, extraction_dates, extraction_prices, gas_rate, storage_cost_rate, total_volume, injection_withdrawal_cost_rate):
    gas_volume = 0
    purchase_cost = 0
    cash_inflows = 0
    last_date = min(min(injection_dates), min(extraction_dates))
    
    # Ensure dates are in sequence
    all_dates = sorted(set(injection_dates + extraction_dates))
    
    for i in range(len(all_dates)):
        # Processing code for each date
        current_date = all_dates[i]

        if current_date in injection_dates:
            # Inject gas on these dates and sum up cash flows
            if gas_volume <= total_volume - gas_rate:
                gas_volume += gas_rate

                # Cost to purchase gas
                purchase_cost += gas_rate * injection_prices[injection_dates.index(current_date)]
                # Injection cost
                injection_cost = gas_rate * injection_withdrawal_cost_rate
                purchase_cost += injection_cost
                print(f'Injected gas on {current_date} at a price of {injection_prices[injection_dates.index(current_date)]}')

            else:
                # We do not want to inject when gas_rate is greater than total volume minus gas_volume
                print(f'Injection is not possible on date {current_date} as there is insufficient space in the storage facility')
        elif current_date in extraction_dates:
            # Withdraw gas on these dates and sum cash flows
            if gas_volume >= gas_rate:
                gas_volume -= gas_rate
                cash_inflows += gas_rate * extraction_prices[extraction_dates.index(current_date)]
                # Withdrawal cost
                withdrawal_cost = gas_rate * injection_withdrawal_cost_rate
                cash_inflows -= withdrawal_cost
                print(f'Extracted gas on {current_date} at a price of {extraction_prices[extraction_dates.index(current_date)]}')
            else:
                # We cannot withdraw more gas than is actually stored
                print(f'Extraction is not possible on date {current_date} as there is insufficient volume of gas stored')
                
    storage_cost = math.ceil((max(extraction_dates) - min(injection_dates)).days // 30) * storage_cost_rate
    return cash_inflows - storage_cost - purchase_cost

# Example usage of calculate_contract_value()
injection_dates = [date(2022, 1, 1), date(2022, 2, 1), date(2022, 2, 21), date(2022, 4, 1)] # Injection dates
injection_prices = [20, 21, 20.5, 22] # Prices on the injection days
extraction_dates = [date(2022, 1, 27), date(2022, 2, 15), date(2022, 3, 20), date(2022, 6, 1)] # Extraction dates
extraction_prices = [23, 19, 21, 25] # Prices on the extraction days
gas_rate = 100000  # Rate of gas in cubic feet per day
storage_cost_rate = 10000  # Total volume in cubic feet
injection_withdrawal_cost_rate = 0.0005  # $/cf
max_storage_volume = 500000 # Maximum storage capacity of the storage facility
result = calculate_contract_value(injection_dates, injection_prices, extraction_dates, extraction_prices, gas_rate, storage_cost_rate, max_storage_volume, injection_withdrawal_cost_rate)
print()
print(f"The value of the contract is: ${result}")
