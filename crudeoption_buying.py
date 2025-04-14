import pandas as pd
crude_price = 5500  # current crude oil price in INR (for MCX)
strike_range = [5500, 5550, 5600, 5650, 5700]

option_chain = pd.DataFrame({
    'strike': strike_range,
    'call_price': [120, 90, 60, 40, 25],
    'put_price': [25, 40, 60, 90, 120],
    'call_oi': [1000, 1200, 1500, 900, 800],
    'put_oi': [800, 900, 1600, 1300, 1000]
})

# --- Step 1: Enter Long Strangle ---
atm_strike = min(strike_range, key=lambda x: abs(x - crude_price))
otm_call = atm_strike + 100
otm_put = atm_strike - 100

entry_positions = {
    'call_strike': otm_call,
    'call_price': option_chain.loc[option_chain['strike'] == otm_call, 'call_price'].values[0],
    'put_strike': otm_put,
    'put_price': option_chain.loc[option_chain['strike'] == otm_put, 'put_price'].values[0]
}

print("Entered Long Strangle:")
print(entry_positions)

# --- Step 2: Breakout Check ---

new_price = 7150  # mock breakout

if new_price > (atm_strike + 100):
    print("\nBreakout Up! Adding Calls:")
    directional_call = atm_strike + 200
    directional_call_price = option_chain.loc[option_chain['strike'] == directional_call, 'call_price'].values[0]
    print(f"Buy extra CALL at {directional_call} for ₹{directional_call_price}")
elif new_price < (atm_strike - 100):
    print("\nBreakdown! Adding Puts:")
    directional_put = atm_strike - 200
    directional_put_price = option_chain.loc[option_chain['strike'] == directional_put, 'put_price'].values[0]
    print(f"Buy extra PUT at {directional_put} for ₹{directional_put_price}")



current_price = 7250

if current_price > directional_call:
    print("\nPrice Extended. Locking Profit:")
    print(f"Square off part of CALL at {directional_call}")
    print(f"Buy hedge PUT at {current_price - 100}")

