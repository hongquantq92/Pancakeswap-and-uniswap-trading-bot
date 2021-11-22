@codzign

# Pancakeswap and Uniswap trading client


A Pancakeswap and Uniswap trading client (and bot) with market orders, limit orders, stop-loss, custom gas strategies, a GUI and much more.



<H3>If you have any questions or inquiries, or want the full version of this bot, you can contact my support via Discord: AviddotSupport#8131 OR telegram: <a href="https://t.me/aviddotsupports">@aviddotsupports</a> or <a href="https://t.me/aviddotsupport2">@aviddotsupport2</a> <b>(please note: these are not the makers of the bot, they deliver the support)</b>. Also check out the website: www.aviddot.us or www.aviddot.com </H3>



<H2>Changelog v2.0</h2>

- Added multiple DEXs (Pcs v1, Uniswap v2)
- Force Buy and Force Sell buttons, when clicked it will buy or sell with your chosen settings (excluding limit price)
- Speed improvements
- Many, many bug fixes (no more force closes or not working tokens)
- Added USDT as maincoin option
- The program now determines the name and decimals of the token automatically






![alt text](https://github.com/aviddot/Pancakeswap-and-uniswap-trading-bot/blob/main/v2gif.gif?raw=true "GIF application")

<H2>Prerequisites</H2>

- An ethereum/bsc address
- A Windows machine (adding support for Mac OS and Linux soon) 
- When trading on Uniswap: infura.io
- <i>Not sure whether needed anymore: Visual C++ build tools (www.visualstudio.microsoft.com/visual-cpp-build-tools/)</i>

<br> </br>
<H2>Getting started</H2>

0. Read prerequisites

1. Download the latest release or download "configfile.py" and "tradingbot.exe" from the repository.


2. Open "configfile.py" (with notepad for instance) and add your ethereum address and personal key at the bottom of the file between the quotation marks('').

<pre>...
my_address = ''
my_pk = ''</pre>


3. Run "tradingbot.exe"

- Make sure configfile.py and bot.exe are in the same folder.


5. Edit settings according to choice.


<br> </br>
<H2>Functions</H2>


<b>Main coin/token</b>: The token or coin you want to trade tokens for and with

<b>Token address</b>: Fill the token address of the token you want to trade (such as 0x0000000000000000000000000000000000000000)

<b>Notes</b>: A place to fill in notes, such as the name of the token

<b>Sell($)</b>: The price you want the trader to sell the token for (0.01 = 1 dollar cent)

<b>Buy($)</b>: The price you want the trader to buy the token for (0.01 = 1 dollar cent)

<b>Trade w/ main</b>: Toggle if you want to activate trading with your main-coin/token

<b>Trade w/ token (Experimental!)</b>: Toggle if you want to trade the token with other BEP20 tokens of which this option is activated (see tokentokennumerator)

<b>Stoploss</b>: Toggle to activate stoploss (0.01 = 1 dollar cent)


<b>Second(s) between checking price</b>: Standard is 4 seconds. With a infura server with max 100.000tx/day 4 seconds is good for 2 activated token 24hr/day


<b>Seconds waiting between trades</b>: depends on how fast transactions finalize

<b>Max slippage</b>: The maximum slippage you want to allow while trading (3 = 3%)

<b>$ to keep in ETH/BNB after trade</b>: The amount of ETH/BNB you want to keep after each trade (excluding transaction fees) in terms of $.

<b>GWEI</b>: The amount of gas you want to use for each trade (5 GWEI is fine for PCS). When trading on uniswap, This becomes the max GWEI you want to pay on the eth network, the GWEI will be determined from ethgasstation.com

<b>Different deposit address</b>: Use this if you want the swap output to go to a different address (without extra fees).

<b>Tokentokennumerator (Experimental!)</b>: This value lets you trade ERC tokens with each other. The code to create the value is as followed:

<pre>if pricetoken1usd > ((token1high + token1low) / 2) and pricetoken2usd < ((token2high + token2low) / 2):
  token1totoken2 = ((pricetoken1usd - token1low) / (token1high - token1low)) / ((pricetoken2usd - token2low) / (token2high - token2low))</pre>
  
  If you dont want to wait till the token1 is sold for the maincoinoption, because you are uncertain whether token2 will still be at this price level or think that token1 will     drop, you can use this function. To use this function, "Trade with ERC" should be activated for at least 2 tokens, and the highs and lows should be set seriously.
    
  As an example, if the current price of token1 is $0.9 and its set "high"=$1 and "low"=$0, the value of this token is seen as "90%". Token2 also has a high of $1, but the         current price is 0.2$, value of this token is seen as 20%. The tokentokenmnumerator is set at 3.3. If we divide the 90% by the 20%, we get 4.5, which is higher than 3.3, which   means that token1 gets traded for token2 instantly. If the tokentokennumerator was set to 5, the swap would not happen.
  
<br> </br>
<H2>Changelog v2.0</h2>

- Added multiple DEXs (Pcs v1, Uniswap v2)
- Force Buy and Force Sell buttons, when clicked it will buy or sell with your chosen settings (excluding limit price)
- Speed improvements
- Many, many bug fixes (no more force closes or not working tokens)
- Added USDT as maincoin option
- The program now determines the name and decimals of the token automatically


<br> </br>
<H2>Current bugs</h2>

- Let me know!

<br> </br>
<H2>To do</H2>

- Add uniswap V3 support
- Add Linux and Mac OS executables
- Create manual and update github text
- Let me know what other DEX's should be added (solidity based ones only)

(Depends on whether the application is used)

<br> </br>
<H2>Author</H2>

<br> </br>
Contact: aviddotgithub@gmail.com
Donations: 0x6B1CeA1c27Bbb1428978dC3C0423642fDa404367



<br> </br>
<H2>Disclosure</H2>
I own some of the tokens portayed in the gif. These tokens are used only for example purposes and are not meant to be an endorsement. I am not affiliated with these tokens or any subsidiaries. Use the application at your own risk, I am not in any way responsible for losses.

  
job solar baby improve leg orange grace rural inquiry pitch glove page

