# Blacktip

Easy-to-use large scale analysis tool for SEC edgar information.
Examine any company filing with the SEC in seconds without having 
to download data from edgar. Register [here](http://blacktipresearch.com/accounts/signup)
before use to be able to use Angler.


## Angler
This is the main SEC analysis tool. After registering your account on the
[Blacktip Research website](http://blacktipresearch.com/accounts/signup), use your **username** and 
**password** to interface with Angler.

### Documentation
The workflow is the following:

**import**
```
from blacktip.angler import Angler
```

**initialize**
```
instance = Angler(username, password)
```

**get data**
```
form10K = instance.query10K("AAPL", 2019)
```

**create data sheet**
```
assets = form10K.asset_sheet()
```

For explicit documentation, visit the [Angler Documentation](http://blacktipresearch.com/Angler).