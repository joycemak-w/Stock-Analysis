from stock import rsi_macd_chart

while True:
    symbols = ["2888.HK", "0005.HK", "2388.HK"]
    for i, s in enumerate(symbols):
        print(f'{i+1}. {s}')
    print('4. Exit')
    selected_option = input('Select Option: ')
    # selected_option = int(selected_option)
    if selected_option == '1' or selected_option == '2' or selected_option == '3':
        selected_option = int(selected_option)
        rsi_macd_chart(symbols[selected_option-1])
    elif selected_option == '4':
        break
    else:
        print('Wrong Option')