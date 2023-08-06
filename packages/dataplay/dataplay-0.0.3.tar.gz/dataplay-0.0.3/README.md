# Data Handling Guidebook
> The one stop shop to learn about data intake, processing, and visualization.


[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/) 
[![NPM License](https://img.shields.io/npm/l/all-contributors.svg?style=flat)](https://github.com/tterb/hyde/blob/master/LICENSE)
[![Active](http://img.shields.io/badge/Status-Active-green.svg)](https://karpatic.github.io) 
[![Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)
[![GitHub last commit](https://img.shields.io/github/last-commit/karpatic/dataplay.svg?style=flat)]() 
[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/) 

This homepage will show you just some of the things you can do with data.

[![GitHub stars](https://img.shields.io/github/stars/tterb/playmusic.svg?style=social&label=Star)](https://github.com/karpatic/dataplay) 
[![GitHub watchers](https://img.shields.io/github/watchers/tterb/playmusic.svg?style=social&label=Watch)](https://github.com/karpatic/dataplay) 
[![GitHub forks](https://img.shields.io/github/forks/tterb/playmusic.svg?style=social&label=Fork)](https://github.com/karpatic/dataplay) 
[![GitHub followers](https://img.shields.io/github/followers/tterb.svg?style=social&label=Follow)](https://github.com/karpatic/dataplay) 

[![Tweet](https://img.shields.io/twitter/url/https/github.com/karpatic/dataplay.svg?style=social)](https://twitter.com/intent/tweet?text=Check%20out%20this%20%E2%9C%A8%20colab%20by%20@bniajfi%20https://github.com/karpatic/dataplay%20%F0%9F%A4%97) 
[![Twitter Follow](https://img.shields.io/twitter/follow/bniajfi.svg?style=social)](https://twitter.com/bniajfi)

## Install

The code is on <a href="https://pypi.org/project/test-template/">PyPI</a> so you can just run:

```
pip install dataplay geopandas
```

From the terminal to install the code and its dependencies

## How to use

Import the installed module into your code and use like so:
``` 
from dataplay.acsDownload import retrieve_acs_data 
retrieve_acs_data(state, county, tract, tableId, year, saveAcs)
```

Heres an example:

```
# Define our download parameters.
# more information on these parameters can be found in the tutorials!
tract = '*'
county = '510'
state = '24'
tableId = 'B19001'
year = '17'
saveAcs = False
```

```
df = retrieve_acs_data(state, county, tract, tableId, year, saveAcs)
df.head()
```

    Number of Columns 17





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>B19001_001E_Total</th>
      <th>B19001_002E_Total_Less_than_$10_000</th>
      <th>B19001_003E_Total_$10_000_to_$14_999</th>
      <th>...</th>
      <th>state</th>
      <th>county</th>
      <th>tract</th>
    </tr>
    <tr>
      <th>NAME</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Census Tract 1901</th>
      <td>796</td>
      <td>237</td>
      <td>76</td>
      <td>...</td>
      <td>24</td>
      <td>510</td>
      <td>190100</td>
    </tr>
    <tr>
      <th>Census Tract 1902</th>
      <td>695</td>
      <td>63</td>
      <td>87</td>
      <td>...</td>
      <td>24</td>
      <td>510</td>
      <td>190200</td>
    </tr>
    <tr>
      <th>Census Tract 2201</th>
      <td>2208</td>
      <td>137</td>
      <td>229</td>
      <td>...</td>
      <td>24</td>
      <td>510</td>
      <td>220100</td>
    </tr>
    <tr>
      <th>Census Tract 2303</th>
      <td>632</td>
      <td>3</td>
      <td>20</td>
      <td>...</td>
      <td>24</td>
      <td>510</td>
      <td>230300</td>
    </tr>
    <tr>
      <th>Census Tract 2502.07</th>
      <td>836</td>
      <td>102</td>
      <td>28</td>
      <td>...</td>
      <td>24</td>
      <td>510</td>
      <td>250207</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 20 columns</p>
</div>



## Legal

__Disclaimer__

**Views Expressed**:
All views expressed in this tutorial are the authors own and do not represent the opinions of any entity whatsover with which they have been, are now, or will be affiliated.

**Responsibility, Errors and Ommissions**: 
The author makes no assurance about the reliability of the information. The author makes takes no responsibility for updating the tutorial nor maintaining it porformant status. Under no circumstances shall the Author or its affiliates be liable for any indirect incedental, consequential, or special and or exemplary damages arising out of or in connection with this tutorial. Information is provided 'as is' with distinct plausability of errors and ommitions. Information found within the contents is attached with an **MIT license**. Please refer to the License for more information. 

**Use at Risk**:
Any action you take upon the information on this Tutorial is strictly at your own risk, and the author will not be liable for any losses and damages in connection with the use of this tutorial and subsequent products.

**Fair Use**
this site contains copyrighted material the use of which has not always been specifically authorized by the copyright owner. While no intention is made to unlawfully use copyrighted work, circumstanes may arise in which such material is made available in effort to advance scientific literacy. We believe this constitutes a 'fair use' of any such copyrighted material as provided for in section 107 of the US Copyright Law. In accordance with Titile 17 U.S.C. Section 108, the material on this tutorial is distributed without profit to those who have expressed a prior interest in receiving the included information for research and education purposes. 

for more information go to: http://www.law.cornell.edu/uscode/17/107.shtml. If you wish to use copyrighted material from this site for purposes of your own that go beyond 'fair use', you must obtain permission from the copyright owner.

__License__

Copyright © 2019 BNIA-JFI

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

