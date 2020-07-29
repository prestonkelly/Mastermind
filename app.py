import warnings
warnings.simplefilter('ignore', UserWarning)
from binance.client import Client
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import requests
import sqlite3
from bs4 import BeautifulSoup
import webbrowser





def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    windowWidth = popup.winfo_reqwidth()
    windowHeight = popup.winfo_reqheight()
    positionRight = int(popup.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(popup.winfo_screenheight() / 2 - windowHeight / 2)
    popup.geometry("+{}+{}".format(positionRight, positionDown))
    label = ttk.Label(popup, text=msg, font=("Verdana", 12), takefocus=True, anchor='center', wraplength=400,
                      justify=tk.CENTER)
    label.pack(side="top", fill="x", pady=15, padx=50)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack(pady=10)
    popup.mainloop()



class LoginPage:
    def __init__(self, master):
        global client
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.configure(padx=60, pady=20)

        self.db = sqlite3.connect('UserKeys.db')
        self.cur = self.db.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS keys (api_key text, api_secret text)')
        self.db.commit()
        self.db.close()

        self.top_label = tk.Label(self.master, text='Please sign in!', padx=10, pady=10)
        self.api_key_label = tk.Label(self.master, text='Api Key: ', padx=7, pady=10)
        self.api_key_entry = ttk.Entry(self.master, width=30)
        self.api_secret_label = tk.Label(self.master, text='Api Secret: ', padx=10, pady=10)
        self.api_secret_entry = ttk.Entry(self.master, width=30, show='*')
        self.var = tk.IntVar()
        self.remember_checkmark = tk.Checkbutton(self.master, text='Remember me', pady=10, variable=self.var)
        self.submit_butt = tk.Button(self.master, text='Submit', width=10, padx=7, pady=5, relief='groove',
                                     command=lambda: [self.add_keys(), self.new_window()])

        self.db = sqlite3.connect('UserKeys.db')
        self.cur = self.db.cursor()
        self.cur.execute('SELECT * FROM keys')
        self.the_keys001 = self.cur.fetchall()
        for k in self.the_keys001:
            api_key22 = k[0]
            api_secret22 = k[1]
            self.api_key_entry.insert(0, api_key22)
            self.api_secret_entry.insert(0, api_secret22)
            client = Client(api_key22, api_secret22, {'timeout': 20})
        self.db.commit()
        self.db.close()
        self.layout()


    def layout(self):
        self.top_label.grid(row=0, columnspan=2)
        self.api_key_label.grid(row=1, column=0)
        self.api_key_entry.grid(row=1, column=1)
        self.api_secret_label.grid(row=2, column=0)
        self.api_secret_entry.grid(row=2, column=1)
        self.remember_checkmark.grid(row=3, columnspan=2)
        self.submit_butt.grid(row=4, columnspan=2)
        
    
    def exit_app(self):
        self.newWindow.destroy()
        self.newWindow.quit()
        
        
    def new_window(self):
        self.master.withdraw()
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.newWindow.resizable(width=False, height=False)
        bb = MainApplication(self.newWindow)


    def add_keys(self):
        global client
        db = sqlite3.connect('UserKeys.db')
        cur = db.cursor()
        if self.var.get() == 1:
            cur.execute('DELETE FROM keys')
            db.commit()

            cur.execute('INSERT INTO keys VALUES (:api_key, :api_secret)',
                        {
                            'api_key': self.api_key_entry.get(),
                            'api_secret': self.api_secret_entry.get()
                        })
            db.commit()
            cur.execute('SELECT * FROM keys')
            the_keys = cur.fetchall()
            for k in the_keys:
                api_key55 = k[0]
                api_secret55 = k[1]
                client = Client(api_key55, api_secret55, {'timeout': 20})
            db.commit()
        else:
            api_key77 = self.api_key_entry.get()
            api_secret77 = self.api_secret_entry.get()
            client = Client(api_key77, api_secret77, {'timeout': 20})
        db.close()




interval = '1m'
datetime_format = "%I:%M %p"
limit = 60
symbol = 'BTCUSDT'
buy_symbol_market = 'USDT'
sell_symbol_market = 'BTC'
style.use('custom_light_style.mpltstyle')



class Header(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.frame1 = tk.LabelFrame(self.parent)
        self.testing_data = client.get_ticker(symbol=symbol)
        self.last_price_header = tk.Label(self.frame1, text='Last Price')
        self.change_header = tk.Label(self.frame1, text='24h Change')
        self.high_price_header = tk.Label(self.frame1, text='24h High')
        self.low_price_header = tk.Label(self.frame1, text='24h Low')
        self.volume_header = tk.Label(self.frame1, text='24h Volume')
        self.last_price_data = tk.Label(self.frame1, text='{}'.format(self.testing_data['lastPrice']))
        self.change_data = tk.Label(self.frame1, text='{} / {}%'.format(self.testing_data['priceChange'],
                                                      self.testing_data['priceChangePercent']))
        self.high_price_data = tk.Label(self.frame1, text='{}'.format(self.testing_data['highPrice']))
        self.low_price_data = tk.Label(self.frame1, text='{}'.format(self.testing_data['lowPrice']))
        self.volume_price_data = tk.Label(self.frame1, text='{:,.2f}'.format(float(self.testing_data['volume'])))

        header_text_1 = [self.last_price_header, self.change_header, self.high_price_header, self.low_price_header,
                         self.volume_header]
        header_text_2 = [self.last_price_data, self.change_data, self.high_price_data, self.low_price_data,
                         self.volume_price_data]
        self.frame1.configure(bg='white')
        for f in header_text_1:
            f.configure(padx=20, font='Helvetica 8', bg='white', fg='#383838')
        for f in header_text_2:
            f.configure(font='Helvetica 9 bold', bg='#FFFFFF', fg='#000000')


        self.layout()


    def update_header_info(self):
        testing_data = client.get_ticker(symbol=symbol)
        if float(testing_data['lastPrice']) > 1:
            self.last_price_data['text'] = round(float(testing_data['lastPrice']), 4)
            self.change_data['text'] = '{} / {}%'.format(round(float(testing_data['priceChange']), 4),
                                                    testing_data['priceChangePercent'])
            self.high_price_data['text'] = round(float(testing_data['highPrice']), 4)
            self.low_price_data['text'] = round(float(testing_data['lowPrice']), 4)
        else:
            self.last_price_data['text'] = testing_data['lastPrice']
            self.change_data['text'] = '{} / {}%'.format(testing_data['priceChange'], testing_data['priceChangePercent'])
            self.high_price_data['text'] = testing_data['highPrice']
            self.low_price_data['text'] = testing_data['lowPrice']
        formatted_vol = '{:,.2f}'.format(float(testing_data['volume']))
        self.volume_price_data['text'] = formatted_vol
        self.parent.after(20000, self.update_header_info)


    def layout(self):
        self.parent.grid()
        self.frame1.grid(row=0, columnspan=3)
        self.last_price_header.grid(row=0, column=0)
        self.change_header.grid(row=0, column=1)
        self.high_price_header.grid(row=0, column=2)
        self.low_price_header.grid(row=0, column=3)
        self.volume_header.grid(row=0, column=4)
        self.last_price_data.grid(row=1, column=0)
        self.change_data.grid(row=1, column=1)
        self.high_price_data.grid(row=1, column=2)
        self.low_price_data.grid(row=1, column=3)
        self.volume_price_data.grid(row=1, column=4)




class Controls(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.main_frame = tk.Frame(self.parent)
        self.graph_frame = tk.LabelFrame(self.main_frame, borderwidth=5, text=' Graph Controls ', labelanchor='n', padx=5, pady=2)
        self.perf_frame = tk.LabelFrame(self.main_frame, borderwidth=5, text=' Top Performers ', labelanchor='n', pady=5, padx=11)
        self.news_frame = tk.LabelFrame(self.main_frame, borderwidth=5, text=' News ', labelanchor='n', pady=2, padx=6)
        self.btc_pairs = []
        self.eth_pairs = []
        self.usdt_pairs = []
        self.list_of_syms = []
        self.list_of_change = []
        self.list_of_vol = []
        self.learn_about = client.get_ticker()
        self.all_symbols = client.get_all_tickers()
        self.watch_list_list = sorted(self.learn_about, key=lambda i: float(i['priceChangePercent']), reverse=True)[0:7]


        for f in self.all_symbols:
            symbols = f['symbol']
            if symbols.endswith('BTC'):
                self.btc_pairs += [symbols]
            if symbols.endswith('ETH'):
                self.eth_pairs += [symbols]
            if symbols.endswith('USDT'):
                self.usdt_pairs += [symbols]

        for i in range(0, 6):
            watchlist_sym = self.watch_list_list[i]['symbol']
            self.list_of_syms += [watchlist_sym]
            watchlist_change = round(float(self.watch_list_list[i]['priceChangePercent']), 2)
            self.list_of_change += [watchlist_change]
            watchlist_vol = '{:,.0f}'.format(round(float(self.watch_list_list[i]['volume']), 0) / 1000)
            self.list_of_vol += [watchlist_vol]


        # Graph controls
        self.graph_controls_000 = ttk.Label(self.graph_frame, text="Interval:")
        self.graph_controls_001 = tk.Button(self.graph_frame, text="1h", command=lambda: self.button_changing(1))
        self.graph_controls_002 = tk.Button(self.graph_frame, text="5h", command=lambda: self.button_changing(2))
        self.graph_controls_003 = tk.Button(self.graph_frame, text="12h", command=lambda: self.button_changing(3))
        self.graph_controls_004 = tk.Button(self.graph_frame, text="24h", command=lambda: self.button_changing(4))
        self.graph_combobox1 = ttk.Combobox(self.graph_frame, values=['2h', '4h', '6h', '8h'], width=8,
                                       state='readonly')
        self.graph_combobox2 = ttk.Combobox(self.graph_frame, values=['7d', '30d', '3M', '6M', '1y'], width=8,
                                       state='readonly')
        self.graph_combobox1.set('2h')
        self.graph_combobox2.set('7d')
        self.graph_combobox1.bind('<<ComboboxSelected>>', self.changing_combobox)
        self.graph_combobox2.bind('<<ComboboxSelected>>', self.changing_combobox22)
        self.dark_mode_label = ttk.Label(self.graph_frame, text="Dark Mode:")
        self.dark_mode_button = tk.Button(self.graph_frame, text="ON", command=self.parent.dark_mode_on)
        self.dark_mode_button_off = tk.Button(self.graph_frame, text="OFF", command=self.parent.dark_mode_off)


        # Top Performers
        self.top_perf_button1 = tk.Button(self.perf_frame, text="{}   +{}%   {}k".format(self.list_of_syms[0], self.list_of_change[0],
                                                                   self.list_of_vol[0]), width=27,
                                     command=lambda: self.market_symbols(0), bg='#FFFFFF', fg='#000000', relief='raised')
        self.top_perf_button2 = tk.Button(self.perf_frame, text="{}   +{}%   {}k".format(self.list_of_syms[1], self.list_of_change[1],
                                                                   self.list_of_vol[1]), width=27,
                                     command=lambda: self.market_symbols(1), bg='#FFFFFF', fg='#000000', relief='raised')
        self.top_perf_button3 = tk.Button(self.perf_frame, text="{}   +{}%   {}k".format(self.list_of_syms[2], self.list_of_change[2],
                                                                   self.list_of_vol[2]), width=27,
                                     command=lambda: self.market_symbols(2), bg='#FFFFFF', fg='#000000', relief='raised')
        self.top_perf_button4 = tk.Button(self.perf_frame, text="{}   +{}%   {}k".format(self.list_of_syms[3], self.list_of_change[3],
                                                                   self.list_of_vol[3]), width=27,
                                     command=lambda: self.market_symbols(3), bg='#FFFFFF', fg='#000000', relief='raised')
        self.top_perf_button5 = tk.Button(self.perf_frame, text="{}   +{}%   {}k".format(self.list_of_syms[4], self.list_of_change[4],
                                                                   self.list_of_vol[4]), width=27,
                                     command=lambda: self.market_symbols(4), bg='#FFFFFF', fg='#000000', relief='raised')
        self.top_perf_button6 = tk.Button(self.perf_frame, text="{}   +{}%   {}k".format(self.list_of_syms[5], self.list_of_change[5],
                                                                   self.list_of_vol[5]), width=27,
                                     command=lambda: self.market_symbols(5), bg='#FFFFFF', fg='#000000', relief='raised')


        # News
        self.times = []
        self.links = []
        self.titles = []
        self.url = 'https://www.coindesk.com/news'
        self.base = 'https://www.coindesk.com'
        self.req = requests.get(self.url)
        self.soup = BeautifulSoup(self.req.content, 'html.parser')
        self.main_listbox = tk.Listbox(self.news_frame, height=9, width=32, bg='white', fg='#000000', selectbackground='gray',
                                  activestyle='none')

        sby = tk.Scrollbar(self.news_frame, width=13)
        sbx = tk.Scrollbar(self.news_frame, orient=tk.HORIZONTAL, width=13)
        sby.grid(column=1, sticky='ns')
        sbx.grid(row=1, sticky='ew')
        self.main_listbox.config(yscrollcommand=sby.set)
        self.main_listbox.config(xscrollcommand=sbx.set)
        sby.config(command=self.main_listbox.yview)
        sbx.config(command=self.main_listbox.xview)
        self.main_listbox.bind('<Double-Button-1>', self.news_article_open)
        for h_four in self.soup.find_all('h4', {'class': 'heading'}):
            self.titles.append(h_four.text)
        for time in self.soup.find_all('time', {'class': 'time'}):
            self.times.append(time.text)
        for div in self.soup.find_all('div', {'class': 'text-content'}):
            self.links.append(self.base + (div.find('a').next_sibling['href']))
        for i in range(9):
            for f in self.times, self.titles[10:19], self.links:
                self.main_listbox.insert(tk.END, f[i])
            self.main_listbox.insert(tk.END, '---')


        self.layout()




    def market_symbols(self, id):
        global symbol, buy_symbol_market, sell_symbol_market
        symbol = self.list_of_syms[id]

        if self.list_of_syms[id].endswith('BTC'):
            buy_symbol_market = 'BTC'
        if self.list_of_syms[id].endswith('ETH'):
            buy_symbol_market = 'ETH'
        if self.list_of_syms[id].endswith('USDT'):
            buy_symbol_market = 'USDT'

        if self.list_of_syms[id] in self.btc_pairs:
            sell_symbol_market = self.list_of_syms[id].replace('BTC', '')
        if self.list_of_syms[id] in self.eth_pairs:
            sell_symbol_market = self.list_of_syms[id].replace('ETH', '')
        if self.list_of_syms[id] in self.usdt_pairs:
            sell_symbol_market = self.list_of_syms[id].replace('USDT', '')


    def button_changing(self, id):
        global interval, datetime_format, limit
        if id == 1:
            interval = '1m'
            datetime_format = "%I:%M %p"
            limit = 60
        if id == 2:
            interval = '1m'
            datetime_format = "%I:%M %p"
            limit = 300
        if id == 3:
            interval = '5m'
            datetime_format = "%I:%M %p"
            limit = 144
        if id == 4:
            interval = '15m'
            datetime_format = "%I:%M %p"
            limit = 96


    def changing_combobox(self, event):
        global interval, datetime_format, limit
        if self.graph_combobox1.get() == '2h':
            interval = '1m'
            datetime_format = "%I:%M %p"
            limit = 120
        elif self.graph_combobox1.get() == '4h':
            interval = '1m'
            datetime_format = "%I:%M %p"
            limit = 240
        elif self.graph_combobox1.get() == '6h':
            interval = '5m'
            datetime_format = "%I:%M %p"
            limit = 72
        else:
            interval = '5m'
            datetime_format = "%I:%M %p"
            limit = 96


    def changing_combobox22(self, event):
        global interval, datetime_format, limit
        if self.graph_combobox2.get() == '7d':
            interval = '2h'
            datetime_format = "%m/%d"
            limit = 84
        elif self.graph_combobox2.get() == '30d':
            interval = '12h'
            datetime_format = "%m/%d"
            limit = 60
        elif self.graph_combobox2.get() == '3M':
            interval = '1d'
            datetime_format = "%m/%d/%y"
            limit = 91
        elif self.graph_combobox2.get() == '6M':
            interval = '3d'
            datetime_format = "%m/%d/%y"
            limit = 60
        else:
            interval = '1w'
            datetime_format = "%m/%Y"
            limit = 52


    def news_article_open(self, event):
        weblink = self.main_listbox.get(tk.ACTIVE)
        if weblink.startswith('https://'):
            webbrowser.open_new(weblink)


    def layout(self):
        self.parent.grid()
        self.main_frame.grid(row=1, column=0)
        self.graph_frame.grid()
        self.perf_frame.grid()
        self.news_frame.grid()

        # Graph controls layout
        self.graph_controls_000.grid(row=0)
        self.graph_controls_001.grid(row=0, column=1)
        self.graph_controls_002.grid(row=0, column=2)
        self.graph_controls_003.grid(row=1, column=1)
        self.graph_controls_004.grid(row=1, column=2)
        self.graph_combobox1.grid(row=2, column=1)
        self.graph_combobox2.grid(row=2, column=2)
        self.dark_mode_label.grid(row=3)
        self.dark_mode_button.grid(row=3, column=1)
        self.dark_mode_button_off.grid(row=3, column=2)

        # Top performers layout
        self.top_perf_button1.grid(row=1, columnspan=3)
        self.top_perf_button2.grid(row=2, columnspan=3)
        self.top_perf_button3.grid(row=3, columnspan=3)
        self.top_perf_button4.grid(row=4, columnspan=3)
        self.top_perf_button5.grid(row=5, columnspan=3)
        self.top_perf_button6.grid(row=6, columnspan=3)

        # News layout
        self.main_listbox.grid(row=0)




class GraphContainer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.draw_frame = tk.Frame(self.parent)
        self.fig = Figure(facecolor='#cccccc')
        self.a = self.fig.add_subplot(111)
        self.layout()


    def animate(self, i):
        kline_data = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        animate_df = pd.DataFrame(kline_data).drop([7, 9, 10, 11], axis=1)
        animate_df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Num of Trades']
        animate_df[['Open', 'High', 'Low', 'Close', 'Volume']] = animate_df[
            ['Open', 'High', 'Low', 'Close', 'Volume']].astype(
            float)
        animate_df['Open Time'] = pd.to_datetime(animate_df['Open Time'], unit='ms')
        animate_df['Close Time'] = pd.to_datetime(animate_df['Close Time'], unit='ms').dt.tz_localize(
            'UTC').dt.tz_convert(
            'US/Eastern').dt.strftime(datetime_format)
        animate_df['EMA7'] = animate_df['Close'].ewm(span=7, adjust=False).mean()
        animate_df['SMA7'] = animate_df['Close'].rolling(7).mean()
        # Reload graph
        self.a.clear()
        animate_df.plot(x='Close Time', y='Close', ax=self.a)
        animate_df.plot(x='Close Time', y='EMA7', ax=self.a)
        animate_df.plot(x='Close Time', y='SMA7', ax=self.a)
        self.a.set_xlabel('')
        self.a.set_title('Last Price of {}: {}'.format(symbol, str(animate_df['Close'][limit - 1])))


    def start(self):
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=6000)
        plt.show()


    def layout(self):
        self.parent.grid()
        canvas = FigureCanvasTkAgg(self.fig, self.parent)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=1)





class MarketPairs(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.main_frame = tk.Frame(self.parent)
        self.buy_wallet_amount = client.get_asset_balance(asset=buy_symbol_market)['free']
        self.sell_wallet_amount = client.get_asset_balance(asset=sell_symbol_market)['free']
        self.btc_pairs = []
        self.eth_pairs = []
        self.usdt_pairs = []
        self.all_symbols = client.get_all_tickers()
        for f in self.all_symbols:
            symbols = f['symbol']
            if symbols.endswith('BTC'):
                self.btc_pairs += [symbols]
            if symbols.endswith('ETH'):
                self.eth_pairs += [symbols]
            if symbols.endswith('USDT'):
                self.usdt_pairs += [symbols]


        # Market pairs
        self.market_frame = tk.LabelFrame(self.main_frame, borderwidth=5, text=' Market ', labelanchor='n', pady=5, padx=7)
        self.BTC_pair = tk.Button(self.market_frame, text="BTC", command=lambda: self.set_values(1))
        self.ETH_pair = tk.Button(self.market_frame, text="ETH", command=lambda: self.set_values(2))
        self.USDT_pair = tk.Button(self.market_frame, text="USDT", command=lambda: self.set_values(3))
        self.pair_entry = ttk.Entry(self.market_frame, width=11)
        self.pairs_combobox = ttk.Combobox(self.market_frame, width=20, height=10, exportselection=True)
        self.pair_entry.bind('<Any-KeyRelease>', self.filter0)
        self.pairs_combobox.bind('<<ComboboxSelected>>', self.selection_change)
        self.pair_list = self.btc_pairs + self.eth_pairs + self.usdt_pairs
        self.pair_list = list(dict.fromkeys(self.pair_list))


        # Buy buttons
        self.buy_frame = tk.LabelFrame(self.main_frame, borderwidth=5, text=' Buy {} '.format(sell_symbol_market), labelanchor='n', pady=5,
                                            padx=5)
        self.buy_wallet = ttk.Label(self.buy_frame, text="Wallet: ")
        self.buy_coin = ttk.Label(self.buy_frame,
                             text=client.get_asset_balance(asset=buy_symbol_market)['free'] + ' {}'.format(
                                 buy_symbol_market))
        self.buy_coin_button1 = ttk.Label(self.buy_frame, text="Price:")
        self.buy_coin_button2 = ttk.Entry(self.buy_frame, width=11, exportselection=True)
        self.buy_coin_button3 = tk.Button(self.buy_frame, text='Market', command=self.market_price_button)
        self.buy_coin_button4 = ttk.Label(self.buy_frame, text="Amount:")
        self.buy_coin_button5 = ttk.Entry(self.buy_frame, width=24, exportselection=True)
        self.buy_coin_button6 = tk.Button(self.buy_frame, text='25%', command=self.switch_to_25)
        self.buy_coin_button7 = tk.Button(self.buy_frame, text='50%', command=self.switch_to_50)
        self.buy_coin_button8 = tk.Button(self.buy_frame, text='100%', command=self.switch_to_100)
        self.buy_coin_button9 = ttk.Label(self.buy_frame, text="Total {}:".format(buy_symbol_market))
        self.buy_coin_button10 = ttk.Entry(self.buy_frame, width=24, exportselection=True)
        self.buy_button = tk.Button(self.buy_frame, text='Buy', width=13, command=self.send_buy_to_binance, bg='#3aa636',
                               fg='white', relief='groove', font='calibri 10 bold')
        self.buy_coin_button2.bind('<Any-KeyRelease>', self.update_buy_coin)
        self.buy_coin_button5.bind('<Any-KeyRelease>', self.update_buy_coin)


        # Sell buttons
        self.sell_frame = tk.LabelFrame(self.main_frame, borderwidth=5, text=' Sell {} '.format(sell_symbol_market), labelanchor='n', pady=5,
                                        padx=5)
        self.sell_wallet = ttk.Label(self.sell_frame, text="Wallet: ")
        self.sell_coin = ttk.Label(self.sell_frame,
                              text=client.get_asset_balance(asset=sell_symbol_market)['free'] + ' {}'.format(
                                  sell_symbol_market))
        self.sell_coin_button1 = ttk.Label(self.sell_frame, text="Price:")
        self.sell_coin_button2 = ttk.Entry(self.sell_frame, width=11)
        self.sell_coin_button3 = tk.Button(self.sell_frame, text='Market', command=self.market_price_button2)
        self.sell_coin_button4 = ttk.Label(self.sell_frame, text="Amount:")
        self.sell_coin_button5 = ttk.Entry(self.sell_frame, width=24)
        self.sell_coin_button6 = tk.Button(self.sell_frame, text='25%', command=self.switch_to_250)
        self.sell_coin_button7 = tk.Button(self.sell_frame, text='50%', command=self.switch_to_500)
        self.sell_coin_button8 = tk.Button(self.sell_frame, text='100%', command=self.switch_to_1000)
        self.sell_coin_button9 = ttk.Label(self.sell_frame, text="Total {}:".format(buy_symbol_market))
        self.sell_coin_button10 = ttk.Entry(self.sell_frame, width=24, exportselection=True)
        self.sell_button = tk.Button(self.sell_frame, text='Sell', width=13, command=self.send_sell_to_binance, bg='#db2a21',
                                fg='white',
                                relief='groove', font='calibri 10 bold')
        self.sell_coin_button2.bind('<Any-KeyRelease>', self.update_sell_coin)
        self.sell_coin_button5.bind('<Any-KeyRelease>', self.update_sell_coin)


        # Cancel order
        self.values01 = client.get_open_orders(symbol=symbol)
        keys_to_remove = ["symbol", "clientOrderId", "executedQty", "status", "timeInForce",
                          "type", "stopPrice", "icebergQty", "time", "orderListId", "cummulativeQuoteQty",
                          "updateTime", "isWorking", "origQuoteOrderQty"]
        for f in self.values01:
            for key in keys_to_remove:
                del f[key]
        self.res = [list(sub.values()) for sub in self.values01]
        self.reversed_res = [item[::-1] for item in self.res]
        self.order_frame = tk.LabelFrame(self.main_frame, borderwidth=5, text=' ' + symbol + ' - Open Orders ',
                                      labelanchor='n',
                                      pady=5)
        self.cancel_combobox = ttk.Combobox(self.order_frame, height=5, exportselection=True, state='readonly', width=24,
                                       values=self.reversed_res)
        self.cancel_combobox.set('Side / Amount / Price ($)')
        self.cancel_order_button = tk.Button(self.order_frame, text='Cancel', command=self.cancel_order)


        self.layout()




    def filter0(self, event):
        pattern = self.pair_entry.get().lower()
        upper_pattern = self.pair_entry.get().upper()
        self.pairs_combobox.delete(0, tk.END)
        self.buy_coin_button2.delete(0, '')
        self.buy_coin_button5.delete(0, '')
        self.buy_coin_button10.delete(0, '')
        self.sell_coin_button2.delete(0, '')
        self.sell_coin_button5.delete(0, '')
        self.sell_coin_button10.delete(0, '')
        for item in self.pair_list:
            if pattern in item.lower():
                self.pairs_combobox.insert(tk.END, item)
                global symbol, buy_symbol_market, sell_symbol_market
                symbol = item
                if pattern.endswith('btc'):
                    buy_symbol_market = 'BTC'
                if pattern.endswith('eth'):
                    buy_symbol_market = 'ETH'
                if pattern.endswith('usdt'):
                    buy_symbol_market = 'USDT'

                if upper_pattern in self.btc_pairs:
                    sell_symbol_market = upper_pattern.replace('BTC', '')
                if upper_pattern in self.eth_pairs:
                    sell_symbol_market = upper_pattern.replace('ETH', '')
                if upper_pattern in self.usdt_pairs:
                    sell_symbol_market = upper_pattern.replace('USDT', '')
            if pattern == '':
                self.pairs_combobox.delete(0, tk.END)


    def selection_change(self, event):
        global symbol, buy_symbol_market, sell_symbol_market
        selection = self.pairs_combobox.selection_get()
        self.buy_coin_button2.delete(0, '')
        self.buy_coin_button5.delete(0, '')
        self.buy_coin_button10.delete(0, '')
        self.sell_coin_button2.delete(0, '')
        self.sell_coin_button5.delete(0, '')
        self.sell_coin_button10.delete(0, '')
        if selection.endswith('BTC'):
            buy_symbol_market = 'BTC'
        if selection.endswith('ETH'):
            buy_symbol_market = 'ETH'
        if selection.endswith('USDT'):
            buy_symbol_market = 'USDT'

        if selection in self.btc_pairs:
            sell_symbol_market = selection.replace('BTC', '')
        if selection in self.eth_pairs:
            sell_symbol_market = selection.replace('ETH', '')
        if selection in self.usdt_pairs:
            sell_symbol_market = selection.replace('USDT', '')
        symbol = selection


    def set_values(self, id):
        if id == 1:
            self.pairs_combobox.delete(0, '')
            self.pairs_combobox['values'] = sorted(self.btc_pairs)
            self.pairs_combobox.insert(0, self.pairs_combobox['values'][0])
        if id == 2:
            self.pairs_combobox.delete(0, '')
            self.pairs_combobox['values'] = sorted(self.eth_pairs)
            self.pairs_combobox.insert(0, self.pairs_combobox['values'][0])
        if id == 3:
            self.pairs_combobox.delete(0, '')
            self.pairs_combobox['values'] = sorted(self.usdt_pairs)
            self.pairs_combobox.insert(0, self.pairs_combobox['values'][0])


    def update_buy_coin(self, event):
        if self.buy_coin_button2.get() or self.buy_coin_button5.get() == '':
            price = float(self.buy_coin_button2.get())
            amount = round(float(self.buy_coin_button5.get()), 5)
            total_usd = round(float(price * amount), 8)
            self.buy_coin_button10.delete(0, '')
            self.buy_coin_button10.insert(0, total_usd)


    def switch_to_25(self):
        personal_coin_asset_data = client.get_asset_balance(asset=buy_symbol_market)['free']
        twentyfive_percent = float(personal_coin_asset_data) * 0.25
        price = float(self.buy_coin_button2.get())
        amount = round(twentyfive_percent / float(self.buy_coin_button2.get()), 6)
        total_usd = round(float(price * amount), 8)
        self.buy_coin_button5.delete(0, '')
        self.buy_coin_button5.insert(0, round(amount, 6))
        self.buy_coin_button10.delete(0, '')
        self.buy_coin_button10.insert(0, total_usd)


    def switch_to_50(self):
        personal_coin_asset_data = client.get_asset_balance(asset=buy_symbol_market)['free']
        fifty_percent = float(personal_coin_asset_data) * 0.50
        price = float(self.buy_coin_button2.get())
        amount = round(fifty_percent / float(self.buy_coin_button2.get()), 6)
        total_usd = round(float(price * amount), 8)
        self.buy_coin_button5.delete(0, '')
        self.buy_coin_button5.insert(0, round(amount, 6))
        self.buy_coin_button10.delete(0, '')
        self.buy_coin_button10.insert(0, total_usd)


    def switch_to_100(self):
        personal_coin_asset_data = client.get_asset_balance(asset=buy_symbol_market)['free']
        total_amount = float(personal_coin_asset_data)
        price = float(self.buy_coin_button2.get())
        amount = round(total_amount / float(self.buy_coin_button2.get()), 6)
        total_usd = round(float(price * amount), 8)
        self.buy_coin_button5.delete(0, '')
        self.buy_coin_button5.insert(0, round(amount, 6))
        self.buy_coin_button10.delete(0, '')
        self.buy_coin_button10.insert(0, total_usd)


    def market_price_button(self):
        bitcoin_market_price = client.get_ticker(symbol=symbol)['lastPrice']
        market_price = float(bitcoin_market_price)
        self.buy_coin_button2.delete(0, '')
        self.buy_coin_button2.insert(0, market_price)


    def send_buy_to_binance(self):
        entered_price = float(self.buy_coin_button2.get())
        entered_amount = float(self.buy_coin_button5.get())
        entered_total = float(self.buy_coin_button10.get())
        if symbol.endswith('BTC'):
            first_price = client.get_ticker(symbol='BTCUSDT')['lastPrice']
            first_step = float(entered_price) * float(first_price)
            second_step = first_step * float(entered_amount)
            final_total = round(second_step, 4)
        elif symbol.endswith('ETH'):
            first_price = client.get_ticker(symbol='ETHUSDT')['lastPrice']
            first_step = float(entered_price) * float(first_price)
            second_step = first_step * float(entered_amount)
            final_total = round(second_step, 4)
        else:
            final_total = float(entered_price * entered_amount)
        if final_total > 10:
            if entered_total <= float(client.get_asset_balance(asset=buy_symbol_market)['free']):
                try:
                    for i in reversed(range(10)):
                        amount5 = round(float(self.buy_coin_button5.get()), i)
                        try:
                            buy_order = client.create_order(symbol=symbol, side='buy', type='LIMIT',
                                                                 price=entered_price,
                                                                 quantity=amount5,
                                                                 timeInForce="GTC")
                            self.buy_coin_button2.delete(0, '')
                            self.buy_coin_button5.delete(0, '')
                            self.buy_coin_button10.delete(0, '')
                            return buy_order, popupmsg(
                                '(Buy Order) Success!\n\n\nPrice: {}\n\nAmount: {} {}\n\nTotal: ~ {} {}'.format(
                                    entered_price, amount5, sell_symbol_market, entered_total, buy_symbol_market))
                        except:
                            i -= 1
                except:
                    pass
            else:
                popupmsg('Not enough funds!')
        else:
            popupmsg('Total (USD) cannot be smaller than $10')




    def update_sell_coin(self, event):
        if self.sell_coin_button2.get() or self.sell_coin_button5.get() == '':
            price = float(self.sell_coin_button2.get())
            amount = round(float(self.sell_coin_button5.get()), 5)
            total_usd = round(float(price * amount), 8)
            self.sell_coin_button10.delete(0, '')
            self.sell_coin_button10.insert(0, total_usd)


    def switch_to_250(self):
        personal_coin_asset_data2 = client.get_asset_balance(asset=sell_symbol_market)['free']
        twentyfive_percent = float(personal_coin_asset_data2) * 0.25
        self.sell_coin_button5.delete(0, '')
        self.sell_coin_button5.insert(0, twentyfive_percent)
        price = float(self.sell_coin_button2.get())
        amount = float(self.sell_coin_button5.get())
        total_usd = round(float(price * amount), 8)
        self.sell_coin_button10.delete(0, '')
        self.sell_coin_button10.insert(0, total_usd)


    def switch_to_500(self):
        personal_coin_asset_data2 = client.get_asset_balance(asset=sell_symbol_market)['free']
        fifty_percent = float(personal_coin_asset_data2) * 0.50
        self.sell_coin_button5.delete(0, '')
        self.sell_coin_button5.insert(0, fifty_percent)
        price = float(self.sell_coin_button2.get())
        amount = float(self.sell_coin_button5.get())
        total_usd = round(float(price * amount), 8)
        self.sell_coin_button10.delete(0, '')
        self.sell_coin_button10.insert(0, total_usd)


    def switch_to_1000(self):
        personal_coin_asset_data2 = client.get_asset_balance(asset=sell_symbol_market)['free']
        total_amount = float(personal_coin_asset_data2)
        self.sell_coin_button5.delete(0, '')
        self.sell_coin_button5.insert(0, total_amount)
        price = float(self.sell_coin_button2.get())
        amount = float(self.sell_coin_button5.get())
        total_usd = round(float(price * amount), 8)
        self.sell_coin_button10.delete(0, '')
        self.sell_coin_button10.insert(0, total_usd)


    def market_price_button2(self):
        bitcoin_market_price = client.get_ticker(symbol=symbol)['lastPrice']
        market_price = float(bitcoin_market_price)
        self.sell_coin_button2.delete(0, '')
        self.sell_coin_button2.insert(0, market_price)


    def send_sell_to_binance(self):
        entered_price = float(self.sell_coin_button2.get())
        entered_amount = float(self.sell_coin_button5.get())
        entered_total = float(self.sell_coin_button10.get())
        if symbol.endswith('BTC'):
            first_price = client.get_ticker(symbol='BTCUSDT')['lastPrice']
            first_step = float(entered_price) * float(first_price)
            second_step = first_step * float(entered_amount)
            final_total = round(second_step, 4)
        elif symbol.endswith('ETH'):
            first_price = client.get_ticker(symbol='ETHUSDT')['lastPrice']
            first_step = float(entered_price) * float(first_price)
            second_step = first_step * float(entered_amount)
            final_total = round(second_step, 4)
        else:
            final_total = float(entered_price * entered_amount)
        if final_total > 10:
            if entered_amount <= float(client.get_asset_balance(asset=sell_symbol_market)['free']):
                try:
                    for i in reversed(range(10)):
                        amount5 = round(float(self.sell_coin_button5.get()), i)
                        try:
                            sell_order = client.create_order(symbol=symbol, side='sell', type='LIMIT',
                                                                 price=entered_price,
                                                                 quantity=amount5,
                                                                 timeInForce="GTC")
                            self.sell_coin_button2.delete(0, '')
                            self.sell_coin_button5.delete(0, '')
                            self.sell_coin_button10.delete(0, '')
                            return sell_order, popupmsg(
                                '(Sell Order) Success!\n\n\nPrice: {}\n\nAmount: {} {}\n\nTotal: ~ {} {}'.format(
                                    entered_price, amount5, sell_symbol_market, entered_total, buy_symbol_market))
                        except:
                            i -= 1
                except:
                    pass
            else:
                popupmsg('Not enough funds!')
        else:
            popupmsg('Total (USD) cannot be smaller than $10')


    def update_wallet(self):
        global buy_symbol_market, sell_symbol_market, values01
        buy_symbol_market = buy_symbol_market
        sell_symbol_market = sell_symbol_market
        self.buy_wallet_amount = client.get_asset_balance(asset=buy_symbol_market)['free']
        self.buy_coin['text'] = self.buy_wallet_amount + ' {}'.format(buy_symbol_market)
        self.buy_coin_button9['text'] = "Total {}:".format(buy_symbol_market)
        self.buy_frame['text'] = ' Buy {} '.format(sell_symbol_market)
        self.sell_wallet_amount = client.get_asset_balance(asset=sell_symbol_market)['free']
        self.sell_coin['text'] = self.sell_wallet_amount + ' {}'.format(sell_symbol_market)
        self.sell_coin_button9['text'] = "Total {}:".format(buy_symbol_market)
        self.sell_frame['text'] = ' Sell {} '.format(sell_symbol_market)
        self.order_frame['text'] = ' ' + symbol + ' - Open Orders '
        self.values01 = client.get_open_orders(symbol=symbol)
        keys_to_remove = ["symbol", "clientOrderId", "executedQty", "status", "timeInForce",
                          "type", "stopPrice", "icebergQty", "time", "orderListId", "cummulativeQuoteQty",
                          "updateTime", "isWorking", "origQuoteOrderQty"]
        for f in self.values01:
            for key in keys_to_remove:
                del f[key]
        self.res = [list(sub.values()) for sub in self.values01]
        self.reversed_res = [item[::-1] for item in self.res]
        self.cancel_combobox['values'] = self.reversed_res
        self.parent.after(12000, self.update_wallet)


    def cancel_order(self):
        for f in self.values01:
            order_ids = f['orderId']
            if str(order_ids) in str(self.cancel_combobox.selection_get()):
                send_to_cancel = client.cancel_order(symbol=symbol, orderId=order_ids)
                order_symbol = send_to_cancel['symbol']
                order_qty = send_to_cancel['origQty']
                order_price = send_to_cancel['price']
                order_status = send_to_cancel['status']
                return send_to_cancel, self.cancel_combobox.set('Side / Amount / Price ($)'), popupmsg(
                    'Success!\n\n\nSymbol: {}\n\nAmount: {}\n\nPrice: {}\n\nStatus: {}'.format(order_symbol,
                                                                                               order_qty, order_price,
                                                                                               order_status))


    def layout(self):
        self.parent.grid()
        self.main_frame.grid(row=1, column=2)
        self.market_frame.grid()
        self.buy_frame.grid()
        self.sell_frame.grid()
        self.order_frame.grid()

        # Market layout
        self.BTC_pair.grid(row=0)
        self.ETH_pair.grid(row=0, column=1)
        self.USDT_pair.grid(row=0, column=2)
        self.pair_entry.grid(row=1, columnspan=1)
        self.pairs_combobox.grid(row=2, columnspan=3)

        # Buy coin layout
        self.buy_wallet.grid(row=0)
        self.buy_coin.grid(row=0, column=1, columnspan=2)
        self.buy_coin_button1.grid(row=1)
        self.buy_coin_button2.grid(row=1, column=1)
        self.buy_coin_button3.grid(row=1, column=2)
        self.buy_coin_button4.grid(row=2)
        self.buy_coin_button5.grid(row=2, column=1, columnspan=2)
        self.buy_coin_button6.grid(row=3)
        self.buy_coin_button7.grid(row=3, column=1)
        self.buy_coin_button8.grid(row=3, column=2)
        self.buy_coin_button9.grid(row=4)
        self.buy_coin_button10.grid(row=4, column=1, columnspan=2)
        self.buy_button.grid(row=5, columnspan=3)

        # Sell coin layout
        self.sell_wallet.grid(row=0)
        self.sell_coin.grid(row=0, column=1, columnspan=2)
        self.sell_coin_button1.grid(row=1)
        self.sell_coin_button2.grid(row=1, column=1)
        self.sell_coin_button3.grid(row=1, column=2)
        self.sell_coin_button4.grid(row=2)
        self.sell_coin_button5.grid(row=2, column=1, columnspan=2)
        self.sell_coin_button6.grid(row=3)
        self.sell_coin_button7.grid(row=3, column=1)
        self.sell_coin_button8.grid(row=3, column=2)
        self.sell_coin_button9.grid(row=4)
        self.sell_coin_button10.grid(row=4, column=1, columnspan=2)
        self.sell_button.grid(row=5, columnspan=3)

        # Cancel order layout
        self.cancel_combobox.grid(row=1, column=0, columnspan=2)
        self.cancel_order_button.grid(row=1, column=3)




class Footer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.frame = tk.LabelFrame(self.parent)
        ready = float(client.get_ticker(symbol='BTCUSDT')['volume'])
        footer_volume_1 = '{:,.2f}'.format(ready)
        ready2 = float(client.get_ticker(symbol='LTCUSDT')['volume'])
        footer_volume_2 = '{:,.2f}'.format(ready2)
        ready3 = float(client.get_ticker(symbol='ETHUSDT')['volume'])
        footer_volume_3 = '{:,.2f}'.format(ready3)
        ready4 = float(client.get_ticker(symbol='BNBUSDT')['volume'])
        footer_volume_4 = '{:,.2f}'.format(ready4)
        ready5 = float(client.get_ticker(symbol='XRPUSDT')['volume'])
        footer_volume_5 = '{:,.2f}'.format(ready5)
        self.footer_text = tk.Label(self.frame,
                               text='24 Quote Volume (USDT): BTC {} // LTC {} // ETH {} // BNB {} // XRP {}'.format(
                                   footer_volume_1, footer_volume_2, footer_volume_3, footer_volume_4, footer_volume_5))
        self.footer_text.configure(font='Helvetica 8 bold', bg='white', fg='#000000')
        self.frame.configure(padx=5, pady=5, bg='white')
        self.layout()


    def update_footer_info(self):
        ready = float(client.get_ticker(symbol='BTCUSDT')['volume'])
        footer_volume_1 = '{:,.2f}'.format(ready)
        ready2 = float(client.get_ticker(symbol='LTCUSDT')['volume'])
        footer_volume_2 = '{:,.2f}'.format(ready2)
        ready3 = float(client.get_ticker(symbol='ETHUSDT')['volume'])
        footer_volume_3 = '{:,.2f}'.format(ready3)
        ready4 = float(client.get_ticker(symbol='BNBUSDT')['volume'])
        footer_volume_4 = '{:,.2f}'.format(ready4)
        ready5 = float(client.get_ticker(symbol='XRPUSDT')['volume'])
        footer_volume_5 = '{:,.2f}'.format(ready5)
        formatted_footer = '24 Quote Volume (USDT): BTC {} // LTC {} // ETH {} // BNB {} // XRP {}'.format(
            footer_volume_1, footer_volume_2, footer_volume_3, footer_volume_4, footer_volume_5)
        self.footer_text['text'] = formatted_footer
        self.parent.after(900000, self.update_footer_info)


    def layout(self):
        self.parent.grid()
        self.frame.grid(row=2, columnspan=3)
        self.footer_text.grid()




class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.header = Header(self)
        self.controls = Controls(self)
        self.graph_container = GraphContainer(self)
        self.market_pairs = MarketPairs(self)
        self.footer = Footer(self)


        self.graph_container.start()
        self.market_pairs.after(0, self.market_pairs.update_wallet())
        self.header.after(0, self.header.update_header_info())
        self.footer.after(0, self.footer.update_footer_info())


        # Style configure for entire app
        self.buttons = [self.controls.graph_controls_001, self.controls.graph_controls_002, self.controls.graph_controls_003,
                   self.controls.graph_controls_004, self.controls.dark_mode_button, self.controls.dark_mode_button_off,
                   self.market_pairs.BTC_pair, self.market_pairs.ETH_pair, self.market_pairs.USDT_pair,
                   self.market_pairs.buy_coin_button3, self.market_pairs.buy_coin_button6,
                    self.market_pairs.buy_coin_button7, self.market_pairs.buy_coin_button8,
                        self.market_pairs.sell_coin_button3, self.market_pairs.sell_coin_button6,
                        self.market_pairs.sell_coin_button7, self.market_pairs.sell_coin_button8]
        self.label_frames = [self.controls.graph_frame, self.controls.perf_frame, self.controls.news_frame,
                             self.market_pairs.market_frame,
                        self.market_pairs.buy_frame, self.market_pairs.sell_frame, self.market_pairs.order_frame]
        self.labels = [self.controls.graph_controls_000, self.controls.dark_mode_label,
                       self.market_pairs.buy_wallet, self.market_pairs.buy_coin, self.market_pairs.buy_coin_button1,
                       self.market_pairs.buy_coin_button4, self.market_pairs.buy_coin_button9,
                       self.market_pairs.sell_wallet, self.market_pairs.sell_coin, self.market_pairs.sell_coin_button1,
                       self.market_pairs.sell_coin_button4, self.market_pairs.sell_coin_button9]
        for f in self.buttons:
            f.configure(bg='#FFFFFF', fg='#000000', relief='groove', width=9, font='calibri 10 bold')
        for f in self.label_frames:
            f.config(bg='#cccccc', fg='#000000', relief='ridge', font=('calibri', 10))
        for f in self.labels:
            f.config(background='#cccccc', foreground='#2b2b2b')

        self.configure(background='#FFFFFF')
        self.market_pairs.cancel_order_button.configure(bg='#FFFFFF', fg='#000000', relief='groove', width=8,
                                                        font='calibri 10 bold')


    def dark_mode_on(self):
        style.use('custom_dark_style.mpltstyle')
        self.buttons = [self.controls.graph_controls_001, self.controls.graph_controls_002,
                        self.controls.graph_controls_003,
                        self.controls.graph_controls_004, self.controls.dark_mode_button,
                        self.controls.dark_mode_button_off,
                        self.market_pairs.BTC_pair, self.market_pairs.ETH_pair, self.market_pairs.USDT_pair,
                        self.market_pairs.buy_coin_button3, self.market_pairs.buy_coin_button6,
                        self.market_pairs.buy_coin_button7, self.market_pairs.buy_coin_button8,
                        self.market_pairs.sell_coin_button3, self.market_pairs.sell_coin_button6,
                        self.market_pairs.sell_coin_button7, self.market_pairs.sell_coin_button8]
        self.label_frames = [self.controls.graph_frame, self.controls.perf_frame, self.controls.news_frame,
                             self.market_pairs.market_frame,
                             self.market_pairs.buy_frame, self.market_pairs.sell_frame, self.market_pairs.order_frame]
        self.labels = [self.controls.graph_controls_000, self.controls.dark_mode_label,
                       self.market_pairs.buy_wallet, self.market_pairs.buy_coin, self.market_pairs.buy_coin_button1,
                       self.market_pairs.buy_coin_button4, self.market_pairs.buy_coin_button9,
                       self.market_pairs.sell_wallet, self.market_pairs.sell_coin, self.market_pairs.sell_coin_button1,
                       self.market_pairs.sell_coin_button4, self.market_pairs.sell_coin_button9]
        self.top_perf_buttons = [self.controls.top_perf_button1, self.controls.top_perf_button2,
                            self.controls.top_perf_button3, self.controls.top_perf_button4,
                            self.controls.top_perf_button5, self.controls.top_perf_button6]
        self.header_text_1 = [self.header.last_price_header, self.header.change_header, self.header.high_price_header,
                         self.header.low_price_header, self.header.volume_header]
        self.header_text_2 = [self.header.last_price_data, self.header.change_data, self.header.high_price_data,
                         self.header.low_price_data, self.header.volume_price_data]

        for f in self.buttons:
            f.configure(bg='#2b2b2b', fg='white', relief='groove', width=9, font='calibri 10 bold')
        for f in self.top_perf_buttons:
            f.configure(bg='#2b2b2b', fg='#FFFFFF', relief='raised', width=27)
        for f in self.label_frames:
            f.config(bg='#2b2b2b', fg='#b5b5b5', relief='ridge', font=('calibri', 10))
        for f in self.labels:
            f.config(background='#2b2b2b', foreground='white')
        for f in self.header_text_1:
            f.configure(padx=20, font='Helvetica 8', bg='#2b2b2b', fg='#b5b5b5')
        for f in self.header_text_2:
            f.configure(font='Helvetica 9 bold', bg='#2b2b2b', fg='white')

        self.configure(background='#121212')
        self.market_pairs.cancel_order_button.configure(bg='#2b2b2b', fg='white', relief='groove', width=8, font='calibri 10 bold')
        self.controls.main_listbox.configure(height=9, width=32, bg='#2b2b2b', fg='white', selectbackground='gray',
                               activestyle='none')
        self.footer.footer_text.configure(font='Helvetica 8 bold', bg='#2b2b2b', fg='white')
        self.graph_container.fig.set_facecolor('#2b2b2b')
        self.graph_container.a.tick_params(axis='both', colors='white')
        self.header.frame1.configure(bg='#2b2b2b')
        self.footer.frame.configure(padx=5, pady=5, bg='#2b2b2b')


    def dark_mode_off(self):
        style.use('custom_light_style.mpltstyle')
        self.buttons = [self.controls.graph_controls_001, self.controls.graph_controls_002,
                        self.controls.graph_controls_003,
                        self.controls.graph_controls_004, self.controls.dark_mode_button,
                        self.controls.dark_mode_button_off,
                        self.market_pairs.BTC_pair, self.market_pairs.ETH_pair, self.market_pairs.USDT_pair,
                        self.market_pairs.buy_coin_button3, self.market_pairs.buy_coin_button6,
                        self.market_pairs.buy_coin_button7, self.market_pairs.buy_coin_button8,
                        self.market_pairs.sell_coin_button3, self.market_pairs.sell_coin_button6,
                        self.market_pairs.sell_coin_button7, self.market_pairs.sell_coin_button8]
        self.label_frames = [self.controls.graph_frame, self.controls.perf_frame, self.controls.news_frame,
                             self.market_pairs.market_frame,
                             self.market_pairs.buy_frame, self.market_pairs.sell_frame, self.market_pairs.order_frame]
        self.labels = [self.controls.graph_controls_000, self.controls.dark_mode_label,
                       self.market_pairs.buy_wallet, self.market_pairs.buy_coin, self.market_pairs.buy_coin_button1,
                       self.market_pairs.buy_coin_button4, self.market_pairs.buy_coin_button9,
                       self.market_pairs.sell_wallet, self.market_pairs.sell_coin, self.market_pairs.sell_coin_button1,
                       self.market_pairs.sell_coin_button4, self.market_pairs.sell_coin_button9]
        self.top_perf_buttons = [self.controls.top_perf_button1, self.controls.top_perf_button2,
                                 self.controls.top_perf_button3, self.controls.top_perf_button4,
                                 self.controls.top_perf_button5, self.controls.top_perf_button6]
        self.header_text_1 = [self.header.last_price_header, self.header.change_header, self.header.high_price_header,
                              self.header.low_price_header, self.header.volume_header]
        self.header_text_2 = [self.header.last_price_data, self.header.change_data, self.header.high_price_data,
                              self.header.low_price_data, self.header.volume_price_data]

        for f in self.buttons:
            f.configure(bg='#FFFFFF', fg='#000000', relief='groove', width=9, font='calibri 10 bold')
        for f in self.top_perf_buttons:
            f.configure(bg='#FFFFFF', fg='#000000', relief='raised', width=27)
        for f in self.label_frames:
            f.config(bg='#cccccc', fg='#000000', relief='ridge', font=('calibri', 10))
        for f in self.labels:
            f.config(background='#cccccc', foreground='#2b2b2b')
        for f in self.header_text_1:
            f.configure(padx=20, font='Helvetica 8', bg='white', fg='#383838')
        for f in self.header_text_2:
            f.configure(font='Helvetica 9 bold', bg='#FFFFFF', fg='#000000')

        self.configure(background='#FFFFFF')
        self.market_pairs.cancel_order_button.configure(bg='#FFFFFF', fg='#000000', relief='groove', width=8, font='calibri 10 bold')
        self.controls.main_listbox.configure(height=9, width=32, bg='white', fg='#000000', selectbackground='gray',
                               activestyle='none')
        self.footer.footer_text.configure(font='Helvetica 8 bold', bg='white', fg='#000000')
        self.graph_container.fig.set_facecolor('#cccccc')
        self.graph_container.a.tick_params(axis='both', colors='#404040')
        self.header.frame1.configure(bg='white')
        self.footer.frame.configure(padx=5, pady=5, bg='white')






if __name__ == "__main__":
    root = tk.Tk()
    root.title('Mastermind')
    root.iconbitmap(default='favicon.ico')
    root.resizable(width=False, height=False)
    b = LoginPage(root)
    root.mainloop()
