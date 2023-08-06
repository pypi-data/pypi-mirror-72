# SECFE

Python module to download SEC filings from the EDGAR Database and extract sections of filings to perform keyword searches. 

## Brief Overview
### What each module does
**SEFD** or **SEC EDGAR Filing Downloader** is a collection of functions to download filings from EDGAR from a CSV input file.<br />
**FSE** or **Filing Section Extractor** is a collection of functions to search filings for a specific section and extract the entire section to an *rtf* file. *Please note that funcionality may be limtied or broken for Mac users due to limited LXML capabilities.*<br /> 
**SKiS** or **Section Keyword Search** is a collection of functions to search filings sections for a list of keywords and output relevant paragraphs to an *rtf* file. 

## Install

From PyPI with pip:

```bash
$ pip install SECFE
```

<!-- TODO: Add Code Examples and update avaialable methods for each module
## Code Examples

### Example: Simple API -- Apple Inc. (``AAPL``)

``` python   
import invain

#Create Simple API object
api = invain.Simple('HD') 
#Get market price
print(api.get_price())
###################
'173.07'
```

## Available methods

### SEFD

- ``add_ticker(ticker)``
- ``add_tickers(tickers)`` -- takes argument as array (['ticker1', 'ticker2', ...]) or individual parameters (ticker1, ticker2, ...)
- ``remove_ticker(tickers)``

### FSE
- ``change_ticker(ticker)``
- ``get_ticker()``
- ``get_price()``

### SKiS
- ``get_customData()``
- ``add_ticker(ticker)``
- ``add_tickers(tickers)`` -- takes list of tickers as argument (or add_tickers(ticker1,ticker2,...))


### utils
- ``get_customData()``
- ``add_ticker(ticker)``
- ``add_tickers(tickers)`` -- takes list of tickers as argument (or add_tickers(ticker1,ticker2,...))


## TODO/Future Updates
- ``Historical Data - In Progress (install from clone to use pre-alpha version)``
- ``Better Error Handling - After Historical Data is in package release``
- ``Add Documentation - Will attempt to do this periodically untill full docs are complete. Any assistance on this would be great :)``
-->

## Requirements

    requests, bs4, lxml

## Feedback, Issues, and Features:
### Feedback
I'd love to get some feedback from users. I want to know how you are using InVaIN so I can focus on updating it in ways that improve your experience. If you'd like to do so you can email me at *invainapi@gmail.com* **(NOTE: Email abuse will result in your email address being BLOCKED)** <br/>
In that vein, I just wanted to outline some guidelines for submitting issues on github.

### Bugs
If you experience any bugs when running the package please submit an issue with a description of the issue. Bugs will take priority over all other issues. 

### Bad Data
If you experience any problems with returned data please create an issue and include:
- ``Code related to SECFE download or data extraction``
- ``Data Returned``
- ``Day and Approximate Time of Access``

This will allow me to better identify what is causing the issue. If you'd rather not post this information on github, please email it to the email listed in the feedback section.

### New Features
Please don't hesitate to ask for new features you'd like to see or make suggestions for improvements. You can open an issue here on github and I'll take a look at it as soon as I can.